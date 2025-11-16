from rest_framework import serializers
from .models import NaoImage
from cognition.serializers import CognitionFrameSerializer


class ImageSerializer(serializers.ModelSerializer):
    frame = CognitionFrameSerializer(read_only=True)

    class Meta:
        model = NaoImage
        fields = "__all__"
