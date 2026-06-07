from django.db.models import Q
from common.models import Log
from django.db import models


class MotionFrame(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="motionframe")
    frame_number = models.IntegerField(blank=True, null=True)
    frame_time = models.IntegerField(blank=True, null=True)
    closest_cognition_frame = models.ForeignKey(
        "cognition.CognitionFrame",
        on_delete=models.SET_NULL,
        related_name="closest_cognition_frame",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Motion Frames"
        indexes = [
            models.Index(fields=["log", "frame_number"]),
        ]
        unique_together = ("log", "frame_number")


class IMUData(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="imudata2")
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="imudata"
    )
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "IMU Data"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_imudata")
        ]

        indexes = [
            models.Index(fields=["log", "id"], name="imudata_log_id_idx"),
            models.Index(
                fields=["frame"],
                name="imudata_data",
                condition=~Q(representation_data__isnull=True)
                & ~Q(representation_data=[])
                & ~Q(representation_data={}),
            ),
        ]


class FSRData(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="fsrdata2")
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="fsrdata"
    )
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "FSR Data"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_fsrdata")
        ]

        indexes = [
            models.Index(fields=["log", "id"], name="fsrdata_log_id_idx"),
            models.Index(
                fields=["frame"],
                name="fsrdata_data",
                condition=~Q(representation_data__isnull=True)
                & ~Q(representation_data=[])
                & ~Q(representation_data={}),
            ),
        ]


class ButtonData(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="buttondata2")
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="buttondata"
    )
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Button Data"
        constraints = [
            models.UniqueConstraint(fields=["frame"], name="unique_frame_id_buttondata")
        ]

        indexes = [
            models.Index(fields=["log", "id"], name="buttondata_log_id_idx"),
            models.Index(
                fields=["frame"],
                name="buttondata_data",
                condition=~Q(representation_data__isnull=True)
                & ~Q(representation_data=[])
                & ~Q(representation_data={}),
            ),
        ]


class SensorJointData(models.Model):
    log = models.ForeignKey(
        Log, on_delete=models.CASCADE, related_name="sensorjointdata2"
    )
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="sensorjointdata"
    )
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Sensor Joint Data"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_sensorjointdata"
            )
        ]


class AccelerometerData(models.Model):
    log = models.ForeignKey(
        Log, on_delete=models.CASCADE, related_name="accelerometerdata2"
    )
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="accelerometerdata"
    )
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Accelerometer Data"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_accelerometerdata"
            )
        ]


class InertialSensorData(models.Model):
    log = models.ForeignKey(
        Log, on_delete=models.CASCADE, related_name="inertialsensordata2"
    )
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="inertialsensordata"
    )
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Inertial Sensor Data"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_inertialsensordata"
            )
        ]


class MotionStatus(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name="motionstatus2")
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="motionstatus"
    )
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Motion Status"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_motionstatus"
            )
        ]


class MotorJointData(models.Model):
    log = models.ForeignKey(
        Log, on_delete=models.CASCADE, related_name="motorjointdata2"
    )
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="motorjointdata"
    )
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Motor Joint Data"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_motorjointdata"
            )
        ]


class GyrometerData(models.Model):
    log = models.ForeignKey(
        Log, on_delete=models.CASCADE, related_name="gyrometerdata2"
    )
    frame = models.ForeignKey(
        MotionFrame, on_delete=models.CASCADE, related_name="gyrometerdata"
    )
    start_pos = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Gyrometer Data"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_gyrometerdata"
            )
        ]
