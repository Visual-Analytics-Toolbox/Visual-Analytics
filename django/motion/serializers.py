from rest_framework import serializers
from .models import (
    MotionFrame,
    ButtonData,
    IMUData,
    FSRData,
    AccelerometerData,
    InertialSensorData,
    MotionStatus,
    SensorJointData,
    MotorJointData,
    GyrometerData,
)


class MotionFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotionFrame
        fields = "__all__"


class IMUDataSerializer(serializers.ModelSerializer):
    frame = MotionFrameSerializer(read_only=True)
    representation_data = serializers.JSONField(read_only=True)

    class Meta:
        model = IMUData
        fields = "__all__"

    def to_representation(self, instance):
        """
        Speed up serialization by skipping individual field
        attribute lookups if performance is critical.
        """
        ret = super().to_representation(instance)
        # Ensure representation_data is included if it was injected
        ret["representation_data"] = getattr(instance, "representation_data", None)
        return ret


class ButtonDataSerializer(serializers.ModelSerializer):
    frame = MotionFrameSerializer(read_only=True)

    class Meta:
        model = ButtonData
        fields = "__all__"


class FSRDataSerializer(serializers.ModelSerializer):
    frame = MotionFrameSerializer(read_only=True)

    class Meta:
        model = FSRData
        fields = "__all__"


class AccelerometerDataSerializer(serializers.ModelSerializer):
    frame = MotionFrameSerializer(read_only=True)

    class Meta:
        model = AccelerometerData
        fields = "__all__"


class InertialSensorDataSerializer(serializers.ModelSerializer):
    frame = MotionFrameSerializer(read_only=True)

    class Meta:
        model = InertialSensorData
        fields = "__all__"


class MotionStatusSerializer(serializers.ModelSerializer):
    frame = MotionFrameSerializer(read_only=True)

    class Meta:
        model = MotionStatus
        fields = "__all__"


class MotorJointDataSerializer(serializers.ModelSerializer):
    frame = MotionFrameSerializer(read_only=True)

    class Meta:
        model = MotorJointData
        fields = "__all__"


class SensorJointDataSerializer(serializers.ModelSerializer):
    frame = MotionFrameSerializer(read_only=True)

    class Meta:
        model = SensorJointData
        fields = "__all__"


class GyrometerDataSerializer(serializers.ModelSerializer):
    frame = MotionFrameSerializer(read_only=True)

    class Meta:
        model = GyrometerData
        fields = "__all__"
