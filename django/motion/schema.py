from drf_spectacular.utils import extend_schema, extend_schema_view
from .serializers import MotionFrameSerializer

motion_frame_viewset_schema = extend_schema_view(
    list=extend_schema(
        summary="List Motion Frames", description="", tags=["Motion Frames"]
    ),
    create=extend_schema(
        summary="Add Motion Frames", description="", tags=["Motion Frames"]
    ),
    retrieve=extend_schema(
        summary="Get Motion Frames", description="", tags=["Motion Frames"]
    ),
    partial_update=extend_schema(
        summary="Patch Motion Frames", description="", tags=["Motion Frames"]
    ),
    bulk_update_endpoint=extend_schema(
        summary="Bulk update Motion Frames",
        description="",
        request=MotionFrameSerializer(many=True),
        tags=["Motion Frames"],
    ),
    destroy=extend_schema(
        summary="Delete Motion Frame", description="", tags=["Motion Frames"]
    ),
    count=extend_schema(
        summary="Count Motion Frames", description="", tags=["Motion Frames"]
    ),
)

motion_repr_viewset_schema = extend_schema_view(
    list=extend_schema(
        summary="List Motion Representations",
        description=(
            "Valid model names are  "
            "IMUData, ButtonData, FSRData, AccelerometerData, "
            "InertialSensorData, MotionStatus, SensorJointData, MotorJointData, GyrometerData. "
        ),
        tags=["Motion Representation"],
    ),
    create=extend_schema(
        summary="Add Motion Representations",
        description=(
            "Valid model names are: IMUData, ButtonData, FSRData, AccelerometerData, "
            "InertialSensorData, MotionStatus, SensorJointData, MotorJointData, GyrometerData. "
        ),
        tags=["Motion Representation"],
    ),
    retrieve=extend_schema(
        summary="Get Motion Representations",
        description=(
            "Valid model names are: IMUData, ButtonData, FSRData, AccelerometerData, "
            "InertialSensorData, MotionStatus, SensorJointData, MotorJointData, GyrometerData. "
        ),
        tags=["Motion Representation"],
    ),
    partial_update=extend_schema(
        summary="Patch Motion Representation",
        description=(
            "Valid model names are: IMUData, ButtonData, FSRData, AccelerometerData, "
            "InertialSensorData, MotionStatus, SensorJointData, MotorJointData, GyrometerData. "
        ),
        tags=["Motion Representation"],
    ),
    destroy=extend_schema(
        summary="Delete Motion Representation",
        description=(
            "Valid model names are: IMUData, ButtonData, FSRData, AccelerometerData, "
            "InertialSensorData, MotionStatus, SensorJointData, MotorJointData, GyrometerData. "
        ),
        tags=["Motion Representation"],
    ),
    count=extend_schema(
        summary="Count Motion Representations",
        description=(
            "Valid model names are: IMUData, ButtonData, FSRData, AccelerometerData, "
            "InertialSensorData, MotionStatus, SensorJointData, MotorJointData, GyrometerData. "
        ),
        tags=["Motion Representation"],
    ),
)
