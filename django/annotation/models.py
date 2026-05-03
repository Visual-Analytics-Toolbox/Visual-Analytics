from django.db import models
from image.models import NaoImage
from common.models import VideoRecording, Log
from cognition.models import CognitionFrame
from django.utils.translation import gettext_lazy as _


class Situation(models.Model):
    # optional content that describes the situation
    content = models.TextField(blank=True, null=True)
    # if situation is relativ to a log we need a reference to a log and the start and end frame
    log = models.ForeignKey(
        Log, on_delete=models.CASCADE, related_name="situation_log"
    )
    start_frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="situation_start"
    )
    end_frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="situation_end"
    )

    # if situation is relativ to a video timestamp we need the video it refers to and start and end frame
    # video_start_frame + video_end_frame
    # video
    video = models.ForeignKey(
        VideoRecording, on_delete=models.CASCADE, related_name="situation_video"
    )
    video_start_frame = models.IntegerField(blank=True, null=True)
    video_end_frame = models.IntegerField(blank=True, null=True)

    # gamecontroller frame
    # TODO: not sure what we get from the gamecontroller exactly