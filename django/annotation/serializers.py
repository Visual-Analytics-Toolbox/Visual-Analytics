from rest_framework import serializers
from .models import Annotation
from common.serializers import TagSerializer
from common.models import Tag


class AnnotationSerializer(serializers.ModelSerializer):
    color = serializers.SerializerMethodField()
    frame_number = serializers.CharField(read_only=True)
    image_url = serializers.CharField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Tag.objects.all(),
        source="tags",
        required=False,
    )

    class Meta:
        model = Annotation
        fields = "__all__"

    def get_color(self, obj):
        return Annotation.Classes.get_color(obj.class_name)
