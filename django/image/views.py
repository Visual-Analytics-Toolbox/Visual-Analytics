from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.db.models import Q
from django.db import connection
from django_filters.rest_framework import DjangoFilterBackend
from psycopg2.extras import execute_values
from . import serializers
from . import models
from core.pagination import LargeResultsSetPagination
from behavior.models import BehaviorFrameOption
from cognition.models import CognitionFrame
from django.forms.models import model_to_dict
from .image_filter import NaoImageFilter
from django.http import JsonResponse
import numpy as np
import time


class ImageCountView(APIView):
    queryset = models.NaoImage.objects.all()

    def get(self, request):
        # Get filter parameters from query string
        query_params = request.query_params.copy()
        if "log" in query_params.keys():
            log_id = int(query_params.pop("log")[0])

            qs = models.NaoImage.objects.filter(frame__log=log_id)
        else:
            qs = models.NaoImage.objects.all()

        filters = Q()
        for field in models.NaoImage._meta.fields:
            param_value = query_params.get(field.name)
            if param_value == "None" or param_value == "null":
                filters &= Q(**{f"{field.name}__isnull": True})
                # print(f"filter with {field.name} = {param_value}")
            elif param_value:
                # print(f"filter with {field.name} = {param_value}")
                filters &= Q(**{field.name: param_value})

        # apply filters if provided
        qs = qs.filter(filters)

        # get the count
        count = qs.count()

        return Response({"count": count}, status=status.HTTP_200_OK)


class ImageValidateView(APIView):
    queryset = models.NaoImage.objects.all()

    def post(self, request):
        # useful to check what else is send via webhook (we could get the annotation data here and put it in a different format for example)
        for k, v in request.data.items():
            print(k, v)
            print()
        image_id = (
            request.data["task"]["data"]["markdown_description"]
            .split("/")[-1]
            .rstrip(")")
        )

        image_instance = get_object_or_404(models.NaoImage, id=image_id)
        
        if request.data["annotation"]["result"]:
            image_instance.annotation = request.data["annotation"]["result"]
            image_instance.has_annotations = True
            image_instance.save()
            return JsonResponse({"status": "copied annotations"})
        return JsonResponse({"status": "ignored empty annotation"})


class ImageUpdateView(APIView):
    queryset = models.NaoImage.objects.all()

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

        for item in data:
            update_fields.update(key for key in item.keys() if key != "id")

        # Build the case statements for each field
        case_statements = []
        for field in update_fields:
            case_when_parts = []
            for item in data:
                if field in item and item[field] is not None:
                    case_when_parts.append(f"WHEN id = {item['id']} THEN %s")

            if case_when_parts:
                case_stmt = (
                    f"""{field} = (CASE {" ".join(case_when_parts)} ELSE {field} END)"""
                )
                print(f"\t{case_stmt}")
                case_statements.append(case_stmt)

        # Collect all values for the parameterized query
        update_values = []
        for field in update_fields:
            for item in data:
                if field in item and item[field] is not None:
                    update_values.append(item[field])

        # Build the complete SQL query
        ids = [str(item["id"]) for item in data]
        sql = f"""
            UPDATE image_naoimage
            SET {", ".join(case_statements)}
            WHERE id IN ({",".join(ids)})
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, update_values)
            return cursor.rowcount


class ImageViewSet(viewsets.ModelViewSet):
    queryset = models.NaoImage.objects.all()
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = NaoImageFilter

    def get_serializer_class(self):
        # Use the Read serializer for retrieving data
        if self.action in ("list", "retrieve"):
            return serializers.ImageReadSerializer

        # Use the Write serializer for creating/updating data
        return serializers.ImageWriteSerializer

    def get_queryset(self):
        qs = models.NaoImage.objects.all()
        qs = qs.select_related("frame").all()

        return qs

    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)

        is_many = isinstance(request.data, list)

        if is_many:
            return self.bulk_create(request.data)
        else:
            return self.single_create(request.data)

    # FIXME combine with ImageUpdateView
    def update(self, request, *args, **kwargs):
        # Check if the data is a list (bulk update) or dict (single update)
        is_many = isinstance(request.data, list)
        print(is_many)
        if is_many:
            return self.bulk_update()
        else:
            return super().update(request, *args, **kwargs)

    def single_create(self, data):
        serializer = self.get_serializer(data=data, many=False)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        instance, created = models.NaoImage.objects.get_or_create(
            frame=validated_data.get("frame"),
            camera=validated_data.get("camera"),
            type=validated_data.get("type"),
            defaults=validated_data,
        )

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        serializer = serializers.ImageReadSerializer(instance)
        return Response(serializer.data, status=status_code)

    def bulk_create(self, data):
        # validated_data = serializer.validated_data
        starttime = time.time()
        rows_tuples = [
            (
                row["frame"],
                row["camera"],
                row["type"],
                row["image_url"],
                row["blurredness_value"],
                row["brightness_value"],
            )
            for row in data
        ]
        with connection.cursor() as cursor:
            query = """
            INSERT INTO image_naoimage (frame_id, camera, type, image_url, blurredness_value, brightness_value)
            VALUES %s
            ON CONFLICT (frame_id, camera, type) DO NOTHING;
            """
            # rows is a list of tuples containing the data
            execute_values(cursor, query, rows_tuples, page_size=1000)
        print(time.time() - starttime)
        # TODO calculate some statistics similar to what we did before here
        return Response({}, status=status.HTTP_200_OK)
