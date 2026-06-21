from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from label_studio_sdk.core import ApiError
from label_studio_sdk import LabelStudio
from common.models import VideoRecording
from rest_framework import status
from . import schema
import os
from .models import RawGCSituation
from .serializers import RawGCSituationSerializer
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from pathlib import Path
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


@schema.video_annotation_view_schema
class VideoAnnotation(GenericAPIView):
    """
    Get Video Annotations from Labelstudio - used for visualization in the frontend
    """

    queryset = VideoRecording.objects.all()

    def get(self, request, pk):
        video = self.get_object()

        if video.labelstudio_url:
            task_id = video.labelstudio_url.split("task=")[-1]
            l_client = LabelStudio(
                base_url="https://labelstudio-api.berlin-united.com",
                api_key=os.environ.get("LABELSTUDIO_API_KEY"),
            )
            try:
                video_task = l_client.tasks.get(id=task_id)
                return Response(
                    {"result": video_task},
                    status=status.HTTP_200_OK,
                )
            except ApiError:
                return Response(
                    {"error": "couldn't fetch task from Labelstudio"},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

        return Response(
            {"error": "This video has no labelstudio url"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class RawGCSituationViewSet(viewsets.ModelViewSet):
    queryset = RawGCSituation.objects.all()
    serializer_class = RawGCSituationSerializer
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]


class RawGCSituationAudioUpload(APIView):
    parser_classes = [MultiPartParser]
    destination_folder = "/mnt/videos/audio"
    queryset = RawGCSituation.objects.all()

    def post(self, request, *args, **kwargs):

        if "file" not in request.FILES:
            return Response(
                {"error": "No file provided. Please use the 'file' key."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.data.get("uuid", "") == "":
            return Response(
                {"error": "Please provide a UUID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        raw_gc_situation = get_object_or_404(
            RawGCSituation, uuid=request.data.get("uuid")
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

        try:
            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
        except IOError as e:
            return Response(
                {"error": f"Failed to save file: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        raw_gc_situation.audio = file_path
        raw_gc_situation.save()

        return Response(
            {
                "message": "File uploaded successfully.",
                "filename": filename,
                "path": str(file_path),
            },
            status=status.HTTP_201_CREATED,
        )
