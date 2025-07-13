from rest_framework import serializers
from .models import NaoImage
from common.serializers import TagSerializer
from common.models import Tag

class ImageSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()
    tags = serializers.SerializerMethodField()
    class Meta:
        model = NaoImage
        fields = "__all__"

    def get_tags(self, obj):
        tags = Tag.objects.filter(images__image=obj)
        return TagSerializer(tags, many=True).data