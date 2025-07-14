from rest_framework import serializers
from .models import NaoImage
from common.serializers import TagSerializer
from common.models import Tag

class ImageSerializer(serializers.ModelSerializer):
    frame_number = serializers.ReadOnlyField()
    tags = TagSerializer(many=True, read_only=True) 

    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        write_only=True, 
        queryset=Tag.objects.all(),
        source='tags', 
        required=False
    )
    class Meta:
        model = NaoImage
        fields = "__all__"