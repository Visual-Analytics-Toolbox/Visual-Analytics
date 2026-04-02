import os
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework_extensions.mixins import CacheResponseMixin
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from . import models
from django.http import (
    JsonResponse,
    HttpResponse,
    FileResponse,
    HttpResponseServerError,
)
from django.views.decorators.http import require_GET
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q, F
from django.db import connection
from psycopg2.extras import execute_values
from django.template import loader
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.authentication import TokenAuthentication
from pathlib import Path
import logging
import requests

logger = logging.getLogger(__name__)
User = get_user_model()


@require_GET
def scalar_doc(request):
    template = loader.get_template("api/api_scalar.html")
    return HttpResponse(template.render())


@require_GET
def health_check(request):
    return JsonResponse({"message": "UP"}, status=200)


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["team_id", "name"]


class RobotViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RobotSerializer
    queryset = models.Robot.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["model", "head_number", "body_serial", "head_serial"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        instance, created = models.Robot.objects.get_or_create(
            head_number=request.data.get("head_number"),
            model=request.data.get("model"),
            defaults=validated_data,
        )

        serializer = self.get_serializer(instance)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "country"]

    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)

        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)

        if is_many:
            return self.bulk_create(serializer)
        else:
            return self.single_create(serializer)

    def single_create(self, serializer):
        validated_data = serializer.validated_data

        instance, created = models.Event.objects.get_or_create(
            name=validated_data.get("name"), defaults=validated_data
        )

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)

    def bulk_create(self, serializer):
        validated_data = serializer.validated_data

        with transaction.atomic():
            # Get all existing names
            existing_names = set(
                models.Event.objects.filter(
                    name__in=[item["name"] for item in validated_data]
                ).values_list("name", flat=True)
            )

            # Separate new and existing events
            new_events = []
            existing_events = []
            for item in validated_data:
                if item["name"] not in existing_names:
                    new_events.append(models.Event(**item))
                    existing_names.add(
                        item["name"]
                    )  # Add to set to catch duplicates within the input
                else:
                    existing_events.append(models.Event.objects.get(name=item["name"]))

            # Bulk create new events
            created_events = models.Event.objects.bulk_create(new_events)

        # Combine created and existing events
        all_events = created_events + existing_events

        # Serialize the results
        result_serializer = self.get_serializer(all_events, many=True)

        return Response(
            {
                "created": len(created_events),
                "existing": len(existing_events),
                "events": result_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class GameViewSet(viewsets.ModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["event"]

    def get_queryset(self):
        queryset = models.Game.objects.prefetch_related("recordings").all()

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        instance, created = models.Game.objects.get_or_create(
            event_id=request.data.get("event"),
            start_time=request.data.get("start_time"),
            half=request.data.get("half"),
            defaults=validated_data,
        )

        serializer = self.get_serializer(instance)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = models.Experiment.objects.all()
    serializer_class = serializers.ExperimentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["event", "name", "type"]

    def get_queryset(self):
        queryset = models.Experiment.objects.select_related("event").annotate(
            event_name=F("event__name")
        )

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        instance, created = models.Experiment.objects.get_or_create(
            event=request.data.get("event"),
            name=request.data.get("name"),
            type=request.data.get("type"),
            defaults=validated_data,
        )

        serializer = self.get_serializer(instance)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)


class LogViewSet(viewsets.ModelViewSet):
    queryset = models.Log.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["game", "player_number", "robot__head_number"]

    def get_serializer_class(self):
        # Use the Read serializer for retrieving data
        if self.action in ("list", "retrieve"):
            return serializers.LogReadSerializer

        # Use the Write serializer for creating/updating data
        return serializers.LogWriteSerializer

    def get_queryset(self):
        queryset = (
            models.Log.objects.select_related("robot").all()
        )

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        instance, created = models.Log.objects.get_or_create(
            game=validated_data.get("game"),
            experiment=validated_data.get("experiment"),
            player_number=validated_data.get("player_number"),
            log_path=validated_data.get("log_path"),
            defaults=validated_data,
        )

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        # we need to use the read serializer explicitely here because the action is create/patch
        serializer = serializers.LogReadSerializer(instance)
        return Response(serializer.data, status=status_code)


class LogStatusViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LogStatusSerializer
    queryset = models.LogStatus.objects.all()

    def get_queryset(self):
        queryset = models.LogStatus.objects.all()
        query_params = self.request.query_params

        filters = Q()
        for field in models.LogStatus._meta.fields:
            param_value = query_params.get(field.name)
            if param_value:
                filters &= Q(**{field.name: param_value})
        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        return queryset.filter(filters)

    def create(self, request, *args, **kwargs):
        # we get and remove log_id from the request data before validating the rest of the data
        # other we get an error because log_id is 1:1 field to log.id
        log = request.data.pop("log")
        log_instance = get_object_or_404(models.Log, id=int(log))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        validated_data = serializer.validated_data

        instance, created = models.LogStatus.objects.update_or_create(
            log=log_instance, defaults=validated_data
        )

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = models.VideoRecording.objects.all()
    serializer_class = serializers.VideoRecordingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["game", "experiment", "type"]
    # TODO maybe make it possible again to filter for log_id - if game has a recording the log has a recording as well

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        instance, created = models.VideoRecording.objects.get_or_create(
            game=validated_data.get("game"),
            experiment=validated_data.get("experiment"),
            type=validated_data.get("type"),
            video_path=validated_data.get("video_path"),
            defaults=validated_data,
        )

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)


class VideoSliceView(APIView):
    def get(self, request):
        # Get filter parameters from query string
        game_id = request.query_params.get("game")
        start = float(request.query_params.get("start"))
        end = float(request.query_params.get("end"))

        qs = models.VideoRecording.objects.filter(game=game_id)
        if not qs.exists():
            return HttpResponseServerError("No Video file found")

        # FIXME: how to select gopro or picam if both exists - maybe prefer picam if exist

        # Make the blocking HTTP call to the FFmpeg service
        base_url = "http://ffmpeg-svc.ffmpeg.svc.cluster.local:80/video"
        params = {"path": qs.first().video_path, "start": start, "end": end}
        ffmpeg_response = requests.get(
            base_url, params=params, timeout=300
        )  # 5 min timeout
        if ffmpeg_response.status_code not in [200, 202]:
            logger.error(
                f"FFmpeg API failed with status {ffmpeg_response.status_code}: {ffmpeg_response.text}"
            )
            return HttpResponseServerError(
                "Video generation service failed to start or complete."
            )

        try:
            # Open the file in binary mode
            json_response = ffmpeg_response.json()
            video_file = open(json_response["output"], "rb")

            # Create the FileResponse
            response = FileResponse(video_file, content_type="video/mp4")

            # Set the Content-Disposition header to trigger a download
            response["Content-Disposition"] = (
                f'attachment; filename="{json_response["output"]}"'
            )

            logger.info(
                f"Successfully created FileResponse for {json_response['output']}"
            )
            return response

        except Exception as e:
            logger.error(f"Error serving file {json_response['output']}: {e}")
            return HttpResponseServerError("Error reading the generated video file.")


class FileUploadBaseView(APIView):
    """
    A base class for file uploads to avoid code duplication.
    Subclasses must define 'destination_folder'.
    """

    parser_classes = [MultiPartParser]
    destination_folder = None  # MUST be overridden by subclasses
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        # Check for 'file' key in the request
        # The client must send the file using the 'file' key in a multipart/form-data request.
        if "file" not in request.FILES:
            return Response(
                {"error": "No file provided. Please use the 'file' key."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        uploaded_file = request.FILES["file"]

        # Sanitize the filename
        filename = os.path.basename(uploaded_file.name)

        # Create the destination directory if it doesn't exist
        destination_dir = Path(self.destination_folder)
        destination_dir.mkdir(parents=True, exist_ok=True)

        file_path = destination_dir / filename

        # Handle potential file overwrites
        if file_path.exists():
            return Response(
                {"error": f"File with name '{filename}' already exists."},
                status=status.HTTP_409_CONFLICT,
            )

        # 5. Write the file to the destination in chunks (memory-efficient)
        try:
            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
        except IOError as e:
            return Response(
                {"error": f"Failed to save file: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            {
                "message": "File uploaded successfully.",
                "filename": filename,
                "path": str(file_path),
            },
            status=status.HTTP_201_CREATED,
        )


class ModelUploadView(FileUploadBaseView):
    """
    Handles file uploads to the 'models/' directory.
    """

    destination_folder = "/mnt/models"


class DatasetUploadView(FileUploadBaseView):
    """
    Handles file uploads to the 'datasets/' directory.
    """

    destination_folder = "/mnt/datasets"


class HealthIssuesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HealthIssuesSerializer
    queryset = models.HealthIssues.objects.all()
