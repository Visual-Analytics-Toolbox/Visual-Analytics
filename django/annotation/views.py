from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from label_studio_sdk import LabelStudio
from label_studio_sdk.core import ApiError
from rest_framework.generics import GenericAPIView
from rest_framework import status
from common.models import VideoRecording
import os


class VideoAnnotation(GenericAPIView):
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
