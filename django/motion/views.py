from .filter import MotionFrameFilter, MotionRepresentationFilter
from django_filters.rest_framework import DjangoFilterBackend
from google.protobuf.json_format import MessageToDict
from core.pagination import LargeResultsSetPagination, CursorPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from django.db import transaction
from django.db import connection
from contextlib import ExitStack
from .models import MotionFrame
from naoth.log import Parser
from django.apps import apps
from . import serializers
from pathlib import Path
from . import schema
import mmap


class DynamicModelMixin:
    my_parser = Parser()

    def get_model(self):
        model_name = self.kwargs.get("model_name")
        return apps.get_model("motion", model_name)

    def get_serializer_class(self):
        model = self.get_model()
        serializer_class_name = f"{model.__name__}Serializer"
        return getattr(serializers, serializer_class_name)

    def get_queryset(self):
        """Strictly returns the base queryset for the model."""
        model = self.get_model()
        query_params = self.request.query_params.copy()

        qs = model.objects.select_related("frame__log").order_by("id")
        filterset = MotionRepresentationFilter(data=query_params, queryset=qs)

        return filterset.qs

    def list(self, request, *args, **kwargs):
        """Handle the binary data injection during the listing process."""
        queryset = self.get_queryset()

        # Paginate
        page = self.paginate_queryset(queryset)
        if page is not None:
            self._inject_binary_data(page)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Non-paginated fallback
        self._inject_binary_data(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def _inject_binary_data(self, items):
        """Helper to attach binary data to the instances in memory."""
        model_name = self.get_model().__name__
        with ExitStack() as stack:
            cache = {}
            for item in items:
                # skip motion representations that don't have the required fields set for mmap to work
                if not (item.start_pos and item.size):
                    continue

                # Use select_related to make this a local attribute access
                path = Path("/mnt/logs") / item.frame.log.sensor_log_path

                if path not in cache:
                    f = stack.enter_context(open(path, "rb"))
                    cache[path] = stack.enter_context(
                        mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                    )

                mm = cache[path]
                # Slicing mmap is nearly instant; MessageToDict is the heavy part.
                raw_blob = mm[item.start_pos : item.start_pos + item.size]
                msg = self.my_parser.parse(model_name, raw_blob)
                item.representation_data = MessageToDict(msg)
        """
        file_cache = {}
        try:
            for item in items:
                try:
                    # Optimize: use select_related('frame__log') in get_queryset to avoid N+1 queries here
                    log_path = str(Path("/mnt/logs") / item.frame.log.sensor_log_path)

                    if log_path not in file_cache:
                        f = open(log_path, "rb")
                        # mmap the file
                        file_cache[log_path] = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

                    start = item.start_pos
                    end = item.start_pos + item.size
                    message = self.my_parser.parse(self.get_queryset().model.__name__, file_cache[log_path][start:end])

                    item.representation_data = MessageToDict(message)

                    #item.binary_data = file_cache[log_path][start:end]
                    
                except Exception as e:
                    print(f"Error processing item {item.id}: {str(e)}")
        finally:
            for mmap_obj in file_cache.values():
                mmap_obj.close()
        """


@schema.motion_repr_viewset_schema
class DynamicModelViewSet(DynamicModelMixin, viewsets.ModelViewSet):
    pagination_class = CursorPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MotionRepresentationFilter
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)
        if not is_many:
            print("error: input not a list")
            return Response({}, status=status.HTTP_411_LENGTH_REQUIRED)

        # Dynamically get the model
        model = self.get_model()

        # Prepare the data for bulk insert
        rows_tuples = [
            (row["frame"], row["start_pos"], row["size"]) for row in request.data
        ]

        with connection.cursor() as cursor:
            query = f"""
            INSERT INTO motion_{model.__name__.lower()} (frame_id, start_pos, size)
            VALUES (%s, %s, %s)
            ON CONFLICT (frame_id) DO UPDATE SET start_pos = EXCLUDED.start_pos, size = EXCLUDED.size;
            """
            # rows is a list of tuples containing the data
            cursor.executemany(query, rows_tuples)

        return Response({}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)

        if is_many:
            data = self.request.data
            try:
                rows_updated = self.bulk_update(data)

                return Response(
                    {
                        "success": True,
                        "rows_updated": rows_updated,
                        "message": f"Successfully updated {rows_updated} images",
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {"success": False, "rows_updated": 0, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return super().update(request, *args, **kwargs)

    @action(detail=False, methods=["patch"], url_path="bulk-update")
    def bulk_update_endpoint(self, request, *args, **kwargs):
        # DRF expects the data to come from request.data
        data = request.data

        if not isinstance(data, list):
            return Response(
                {"detail": "Expected a list of items."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Call your custom SQL logic
        rows_updated = self.bulk_update(data)

        return Response(
            {"detail": f"Successfully updated {rows_updated} rows."},
            status=status.HTTP_200_OK,
        )

    def bulk_update(self, data):
        model = self.get_queryset().model

        # 1. Gather all IDs from the payload
        ids = [item["id"] for item in data if "id" in item]
        if not ids:
            return 0

        # 2. Fetch existing instances to avoid overwriting omitted fields
        # and to ensure we are only updating records that actually exist.
        queryset = model.objects.filter(id__in=ids)
        instance_map = {instance.id: instance for instance in queryset}

        updated_instances = []
        fields_to_update = set()

        # 3. Populate instances with the incoming data safely
        for item in data:
            obj_id = item.get("id")
            instance = instance_map.get(obj_id)

            if not instance:
                continue  # Skip IDs that don't exist in the DB

            for field, value in item.items():
                if field == "id":
                    continue

                # Check if the field is a foreign key by looking for its concrete DB column name
                target_field = field
                if hasattr(instance, f"{field}_id"):
                    target_field = f"{field}_id"

                # Check if the field actually exists on the model
                if hasattr(instance, target_field):
                    setattr(instance, target_field, value)
                    fields_to_update.add(target_field)

            updated_instances.append(instance)

        if not updated_instances or not fields_to_update:
            return 0

        # 4. Perform the bulk update inside a transaction safely
        with transaction.atomic():
            # Django automatically converts Python dicts to JSON strings here
            model.objects.bulk_update(updated_instances, fields_to_update)

        return len(updated_instances)

    @action(detail=False, methods=["get"], url_path="count")
    def count(self, request, *args, **kwargs):
        """
        Custom action to count records in the dynamic model.
        Accessible at /api/motion/<modelname>/count/
        """
        model = self.get_model()
        base_queryset = model.objects.all()
        queryset = self.filter_queryset(base_queryset)

        count = queryset.count()

        return Response({"count": count})


@schema.motion_frame_viewset_schema
class MotionFrameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MotionFrameSerializer
    queryset = MotionFrame.objects.all()
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MotionFrameFilter
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        queryset = MotionFrame.objects.all()

        return queryset

    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)
        if not is_many:
            print("error: input not a list")
            return Response({}, status=status.HTTP_411_LENGTH_REQUIRED)

        rows_tuples = [
            (row["log"], row["frame_number"], row["frame_time"]) for row in request.data
        ]

        with connection.cursor() as cursor:
            query = """
            INSERT INTO motion_motionframe (log_id, frame_number, frame_time)
            VALUES (%s, %s, %s)
            ON CONFLICT (log_id, frame_number) DO NOTHING;
            """
            # rows is a list of tuples containing the data
            cursor.executemany(query, rows_tuples)

        return Response({}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="bulk-update")
    def bulk_update_endpoint(self, request):
        # DRF expects the data to come from request.data
        data = request.data

        if not isinstance(data, list):
            return Response(
                {"detail": "Expected a list of items."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rows_updated = self.bulk_update(data)

        return Response(
            {"detail": f"Successfully updated {rows_updated} rows."},
            status=status.HTTP_200_OK,
        )

    def bulk_update(self, data):
        update_fields = set()

        # since closest_cognition_frame is a foreign key and therefore has not the same name in the db
        # as it has in django we need to take care of the transformation manually here
        transformed_data = []

        for item in data:
            new_item = {}
            for key, value in item.items():
                if key == "closest_cognition_frame":
                    new_item["closest_cognition_frame_id"] = value
                else:
                    new_item[key] = value
            transformed_data.append(new_item)

        for item in transformed_data:
            update_fields.update(key for key in item.keys() if key != "id")

        # Build the case statements for each field
        case_statements = []
        for field in update_fields:
            case_when_parts = []
            for item in transformed_data:
                print("item", item)
                if field in item and item[field] is not None:
                    case_when_parts.append(f"WHEN id = {item['id']} THEN %s")

            if case_when_parts:
                case_stmt = (
                    f"""{field} = (CASE {" ".join(case_when_parts)} ELSE {field} END)"""
                )
                case_statements.append(case_stmt)

        # Collect all values for the parameterized query
        update_values = []
        for field in update_fields:
            for item in transformed_data:
                if field in item and item[field] is not None:
                    update_values.append(item[field])

        # Build the complete SQL query
        ids = [str(item["id"]) for item in transformed_data]
        sql = f"""
            UPDATE motion_motionframe
            SET {", ".join(case_statements)}
            WHERE id IN ({",".join(ids)})
        """
        print(sql)

        with connection.cursor() as cursor:
            cursor.execute(sql, update_values)
            return cursor.rowcount

    def destroy(self, request, *args, **kwargs):
        # Override destroy method to handle both single and bulk delete
        if kwargs.get("pk") == "all":
            deleted_count, _ = self.get_queryset().delete()
            return Response(
                {"message": f"Deleted {deleted_count} objects"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="count")
    def count(self, request):
        queryset = self.filter_queryset(self.queryset)

        count = queryset.count()

        return Response({"count": count}, status=status.HTTP_200_OK)
