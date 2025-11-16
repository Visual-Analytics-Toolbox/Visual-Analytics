from rest_framework import serializers
from .models import NaoImage
from cognition.serializers import CognitionFrameSerializer


class ImageWriteSerializer(serializers.ModelSerializer):
    # Only needs the field names exactly as they are in the request payload.
    # The 'frame' field maps directly to the underlying frame_id foreign key.

    class Meta:
        model = NaoImage
        fields = "__all__"
        # Note: 'frame' here expects the integer ID


class ImageReadSerializer(serializers.ModelSerializer):
    # This overrides the default field and uses your nested serializer for output
    frame = CognitionFrameSerializer(read_only=True)

    class Meta:
        model = NaoImage
        fields = "__all__"
