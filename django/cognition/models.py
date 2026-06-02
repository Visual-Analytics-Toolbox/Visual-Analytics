from django.db import models
from common.models import Log
from django.db.models import Q

class CognitionFrame(models.Model):
    log = models.ForeignKey(
        Log, on_delete=models.CASCADE, related_name="cognitionframe"
    )
    frame_number = models.IntegerField(blank=True, null=True)
    frame_time = models.IntegerField(blank=True, null=True)
    closest_motion_frame = models.ForeignKey(
        "motion.Motionframe",
        on_delete=models.SET_NULL,
        related_name="closest_motion_frame",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Cognition Frames"
        indexes = [
            models.Index(fields=["log", "frame_number"]),
        ]
        unique_together = ("log", "frame_number")


class AudioData(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="audiodata"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="audiodata2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Audio Data"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_audiodata")
        ]


class BallModel(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="ballmodel"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="ballmodel2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Ball Model"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_ballmodel")
        ]
        indexes = [
            models.Index(fields=["log", "id"], name="ballmodel_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='idx_repr_has_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class BallCandidates(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="ballcandidates"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="ballcandidates2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Ball Candidates"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_ballcandidates"
            )
        ]


class BallCandidatesTop(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="ballcandidatestop"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="ballcandidatestop2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Ball Candidates Top"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_ballcandidatestop"
            )
        ]


class CameraMatrix(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="cameramatrix"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="cameramatrix2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Camera Matrix"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_cameramatrix"
            )
        ]


class CameraMatrixTop(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="cameramatrixtop"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="cameramatrixtop2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Camera Matrix Top"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_cameramatrixtop"
            )
        ]


class OdometryData(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="odometrydata"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="odometrydata2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Odometry Data"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_odometrydata"
            )
        ]


class FieldPercept(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="fieldpercept"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="fieldpercept2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Field Percept"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_fieldpercept"
            )
        ]


class FieldPerceptTop(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="fieldpercepttop"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="fieldpercepttop2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Field Percept Top"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_fieldpercepttop"
            )
        ]


class GoalPercept(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="goalpercept"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="goalpercept2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Goal Percept"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_goalpercept"
            )
        ]


class GoalPerceptTop(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="goalpercepttop"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="goalpercepttop2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Goal Percept Top"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_goalpercepttop"
            )
        ]


class MultiBallPercept(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="multiballpercept"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="multiballpercept2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Multi Ball Percept"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_multiballpercept"
            )
        ]


class RansacCirclePercept2018(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="ransaccirclepercept2018"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="ransaccirclepercept20182")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Ransac Circle Percept 2018"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_ransaccirclepercept2018"
            )
        ]


class RansacLinePercept(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="ransaclinepercept"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="ransaclinepercept2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Ransac Line Percept"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_ransaclinepercept"
            )
        ]


class RobotInfo(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="robotinfo"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="robotinfo2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Robot Info"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_robotinfo")
        ]


class ShortLinePercept(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="shortlinepercept"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="shortlinepercept2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Short Line Percept"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_shortlinepercept"
            )
        ]


class ScanLineEdgelPercept(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="scanlineedgelpercept"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="scanlineedgelpercept2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Scanline Edgel Percept"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_scanlineedgelpercept"
            )
        ]


class ScanLineEdgelPerceptTop(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="scanlineedgelpercepttop"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="scanlineedgelpercepttop2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Scanline Edgel Percept Top"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_scanlineedgelpercepttop"
            )
        ]


class TeamMessageDecision(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="teammessagedecision"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="teammessagedecision2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Team Message Decision"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_teammessagedecision"
            )
        ]


class Teamstate(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="teamstate"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="teamstate2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Team State"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_teamstate")
        ]


class WhistlePercept(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="whistlepercept"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="whistlepercept2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Whistle Percept"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_whistlepercept"
            )
        ]


class RobotPose(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="robotpose"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="robotpose2")
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Robot Pose"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_robotpose")
        ]
