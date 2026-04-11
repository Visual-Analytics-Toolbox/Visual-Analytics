from django.db import models
from image.models import NaoImage
from common.models import VideoRecording
from django.utils.translation import gettext_lazy as _




# TODO build models for labeling situations

# TODO build models for ball patches
# class BallPatches(models.Model):
#    # TODO how can i use the information about which sha is best, like ordering or figuring out in which branches they are etc.
#    image = models.ForeignKey(NaoImage, on_delete=models.CASCADE, related_name="ballpatches")
#    commit = models.CharField(max_length=40, blank=True, null=True)
#    data = models.JSONField(blank=True, null=True)
