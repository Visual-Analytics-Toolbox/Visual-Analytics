from django_filters.rest_framework import DjangoFilterBackend
from core.pagination import LargeResultsSetPagination, CursorPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.views import APIView
from django.db import transaction
from .filter import CognitionFrameFilter
from .filter import CognitionRepresentationFilter
from .models import CognitionFrame
from django.db import connection
from django.apps import apps
from . import serializers
import json


class DynamicModelMixin:
    def get_model(self):
        # Get the model name from the URL kwargs
        model_name = self.kwargs.get("model_name")
        # Get the model class from the app's models
        return apps.get_model("cognition", model_name)

    def get_queryset(self):
        # Override get_queryset to use the dynamic model
        model = self.get_model()
        return model.objects.select_related("frame")


class DynamicModelViewSet(DynamicModelMixin, viewsets.ModelViewSet):
    pagination_class = CursorPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CognitionRepresentationFilter
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    # No need to define queryset or serializer_class here; they will be set dynamically
    def get_serializer_class(self):
        # Dynamically set the serializer class based on the model
        model = self.get_model()
        # Assuming you have a naming convention for serializers, e.g., <ModelName>Serializer
        serializer_class_name = f"{model.__name__}Serializer"
        return getattr(serializers, serializer_class_name)

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
            (
                row["log"],
                row["frame"],
                row["start_pos"],
                row["size"],
                json.dumps(row["representation_data"]),
            )
            for row in request.data
        ]

        with connection.cursor() as cursor:
            query = f"""
                INSERT INTO cognition_{model.__name__.lower()}(log_id, frame_id, start_pos, size, representation_data)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (frame_id) 
                DO UPDATE SET start_pos = EXCLUDED.start_pos, size = EXCLUDED.size, representation_data = EXCLUDED.representation_data;
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
    def count_records(self, request, *args, **kwargs):
        """
        Custom action to count records in the dynamic model.
        Accessible at /api/cognition/<modelname>/count/
        """
        model = self.get_model()
        base_queryset = model.objects.all()
        queryset = self.filter_queryset(base_queryset)

        # You can add any additional filtering here if needed
        count = queryset.count()

        return Response({"count": count})


class CognitionFrameUpdate(APIView):
    queryset = CognitionFrame.objects.all()

    def patch(self, request):
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

    def bulk_update(self, data):
        update_fields = set()

        # since closest_motion_frame is a foreign key and therefore has not the same name in the db
        # as it has in django we need to take care of the transformation manually here
        transformed_data = []

        for item in data:
            new_item = {}
            for key, value in item.items():
                if key == "closest_motion_frame":
                    new_item["closest_motion_frame_id"] = value
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
            UPDATE cognition_cognitionframe
            SET {", ".join(case_statements)}
            WHERE id IN ({",".join(ids)})
        """
        print(sql)

        with connection.cursor() as cursor:
            cursor.execute(sql, update_values)
            return cursor.rowcount


class CognitionFrameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CognitionFrameSerializer
    queryset = CognitionFrame.objects.all()
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CognitionFrameFilter
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        queryset = CognitionFrame.objects.all()

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
            INSERT INTO cognition_cognitionframe (log_id, frame_number, frame_time)
            VALUES (%s, %s, %s)
            ON CONFLICT (log_id, frame_number) DO NOTHING;
            """
            # rows is a list of tuples containing the data
            cursor.executemany(query, rows_tuples)

        return Response({}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="count")
    def count(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        # get the count
        count = queryset.count()

        return Response({"count": count}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        # Override destroy method to handle both single and bulk delete
        if kwargs.get("pk") == "all":
            deleted_count, _ = self.get_queryset().delete()
            return Response(
                {"message": f"Deleted {deleted_count} objects"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return super().destroy(request, *args, **kwargs)
