from rest_framework import serializers
from .models import NaoImage
from annotation.serializers import AnnotationSerializer


class ImageSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()

    class Meta:
        model = NaoImage
        fields = "__all__"


class ImageWithAnnotationsSerializer(ImageSerializer):
    annotations = AnnotationSerializer(source="annotation", many=True, read_only=True)
