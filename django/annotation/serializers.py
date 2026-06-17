from rest_framework import serializers
from .models import RawGCSituation


class RawGCSituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawGCSituation
        fields = '__all__'
