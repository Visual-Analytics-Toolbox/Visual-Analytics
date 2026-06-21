from rest_framework import serializers
from .models import RawGCSituation


class RawGCSituationSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()

    class Meta:
        model = RawGCSituation
        fields = "__all__"

    def create(self, validated_data):
        uuid_val = validated_data.get("uuid")

        # Look for an existing record with this UUID
        existing_instance = RawGCSituation.objects.filter(uuid=uuid_val).first()

        if existing_instance:
            # If it exists, just return it. Django will ignore the new data.
            return existing_instance

        # If it doesn't exist, proceed with the normal creation
        return super().create(validated_data)
