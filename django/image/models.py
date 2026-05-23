from django.db import models
from cognition.models import CognitionFrame
from common.models import Log
from django.utils.translation import gettext_lazy as _


class NaoImage(models.Model):
    class Camera(models.TextChoices):
        TOP = "TOP", _("Top")
        BOTTOM = "BOTTOM", _("Bottom")

    class Type(models.TextChoices):
        raw = "RAW", _("raw")
        jpeg = "JPEG", _("jpeg")

    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="images"
    )
    log = models.ForeignKey(
        Log, on_delete=models.CASCADE, related_name="image"
    )
    camera = models.CharField(max_length=10, choices=Camera, blank=True, null=True)
    type = models.CharField(max_length=10, choices=Type, blank=True, null=True)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    blurredness_value = models.IntegerField(blank=True, null=True)
    brightness_value = models.IntegerField(blank=True, null=True)
    labelstudio_url = models.CharField(max_length=200, blank=True, null=True)
    has_annotations = models.BooleanField(blank=True, null=True, db_index=True)
    annotation = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}-{self.camera}-{self.type}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["frame", "camera", "type"], name="unique_frame_camera_type"
            )
        ]
        indexes = [
            # 1. The Ultimate Cursor Optimization Index
            models.Index(fields=["log", "id"], name="naoimage_log_id_idx"),
            
            # 2. Recommended Filter Combinations (Optional but highly useful)
            models.Index(fields=["log", "camera", "type"], name="naoimage_log_filter_idx"),
        ]