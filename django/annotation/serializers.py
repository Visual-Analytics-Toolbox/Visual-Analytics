from rest_framework import serializers
from .models import Annotation,AnnotationTag
from common.serializers import TagSerializer
from common.models import Tag


class AnnotationSerializer(serializers.ModelSerializer):
    color = serializers.SerializerMethodField()
    frame_number = serializers.CharField(read_only=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Annotation
        fields = "__all__"

    def get_color(self, obj):
        return Annotation.Classes.get_color(obj.class_name)

    def get_tags(self, obj):
        # Get all Tag objects related to this annotation via AnnotationTag
        tags = Tag.objects.filter(annotations__annotation=obj)
        return TagSerializer(tags, many=True).data