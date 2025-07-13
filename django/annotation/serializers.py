from rest_framework import serializers
from .models import Annotation,AnnotationTag
from common.serializers import TagSerializer
from common.models import Tag


class AnnotationSerializer(serializers.ModelSerializer):
    color = serializers.SerializerMethodField()
    frame_number = serializers.CharField(read_only=True)
    tags = TagSerializer(many=True, read_only=True) 

    tag_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True,
        required=False 
    )

    class Meta:
        model = Annotation
        fields = "__all__"

    def get_color(self, obj):
        return Annotation.Classes.get_color(obj.class_name)
    
    def update(self, instance, validated_data):
        """
        Handle the update logic for the Annotation and its tags.
        """
        tag_ids = validated_data.pop('tag_ids', None)

        annotation_instance = super().update(instance, validated_data)

        # If tag_ids were provided in the PATCH request, update the relationship.
        if tag_ids is not None:
            # we don't do anything if a tag does not exist
            if Tag.objects.filter(id__in=tag_ids).count() == len(tag_ids):
                annotation_instance.tags.set(tag_ids)

        return annotation_instance