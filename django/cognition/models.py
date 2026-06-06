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
    start_pos = models.BigIntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Audio Data"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_audiodata")
        ]
        indexes = [
            models.Index(fields=["log", "id"], name="audiodata_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='audiodata_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class BallModel(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="ballmodel"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="ballmodel2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
                name='idx_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class BallCandidates(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="ballcandidates"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="ballcandidates2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="ballcandidates_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='ballcandidates_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class BallCandidatesTop(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="ballcandidatestop"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="ballcandidatestop2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="ballcandidatestop_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='ballcandidatestop_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class CameraMatrix(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="cameramatrix"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="cameramatrix2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="cameramatrix_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='cameramatrix_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class CameraMatrixTop(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="cameramatrixtop"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="cameramatrixtop2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="cameramatrixtop_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='cameramatrixtop_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class OdometryData(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="odometrydata"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="odometrydata2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="odometrydata_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='odometrydata_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class FieldPercept(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="fieldpercept"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="fieldpercept2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="fieldpercept_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='fieldpercept_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class FieldPerceptTop(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="fieldpercepttop"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="fieldpercepttop2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="fieldpercepttop_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='fieldpercepttop_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class GoalPercept(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="goalpercept"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="goalpercept2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="goalpercept_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='goalpercept_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class GoalPerceptTop(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="goalpercepttop"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="goalpercepttop2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="goalpercepttop_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='goalpercepttop_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class MultiBallPercept(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="multiballpercept"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="multiballpercept2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="multiballpercept_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='multiballpercept_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class RansacCirclePercept2018(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="ransaccirclepercept2018"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="ransaccirclepercept20182")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="ransaccirclepercept2018_idx"),
            models.Index(
                fields=['frame'], 
                name='ransaccirclepercept2018_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class RansacLinePercept(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="ransaclinepercept"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="ransaclinepercept2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="ransaclinepercept_idx"),
            models.Index(
                fields=['frame'], 
                name='ransaclinepercept_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class RobotInfo(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="robotinfo"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="robotinfo2")
    start_pos = models.BigIntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Robot Info"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_robotinfo")
        ]
        indexes = [
            models.Index(fields=["log", "id"], name="robotinfo_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='robotinfo_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class ShortLinePercept(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="shortlinepercept"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="shortlinepercept2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="shortlinepercept_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='shortlinepercept_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class ScanLineEdgelPercept(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="scanlineedgelpercept"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="scanlineedgelpercept2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="scanlineedgelpercept_idx"),
            models.Index(
                fields=['frame'], 
                name='scanlineedgelpercept_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class ScanLineEdgelPerceptTop(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="scanlineedgelpercepttop"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="scanlineedgelpercepttop2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="scanlineedgelpercepttop_idx"),
            models.Index(
                fields=['frame'], 
                name='scanlineedgelpercepttop_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class TeamMessageDecision(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="teammessagedecision"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="teammessagedecision2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="teammessagedecision_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='teammessagedecision_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class Teamstate(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="teamstate"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="teamstate2")
    start_pos = models.BigIntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Team State"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_teamstate")
        ]
        indexes = [
            models.Index(fields=["log", "id"], name="teamstate_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='teamstate_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class WhistlePercept(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="whistlepercept"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="whistlepercept2")
    start_pos = models.BigIntegerField(blank=True, null=True)
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
        indexes = [
            models.Index(fields=["log", "id"], name="whistlepercept_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='whistlepercept_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]


class RobotPose(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="robotpose"
    )
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="robotpose2")
    start_pos = models.BigIntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Robot Pose"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_robotpose")
        ]
        indexes = [
            models.Index(fields=["log", "id"], name="robotpose_log_id_idx"),
            models.Index(
                fields=['frame'], 
                name='robotpose_data',
                condition=~Q(representation_data__isnull=True) & ~Q(representation_data=[]) & ~Q(representation_data={})
            )
        ]
