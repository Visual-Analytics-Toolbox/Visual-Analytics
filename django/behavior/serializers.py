from rest_framework import serializers
from . import models
from cognition.serializers import CognitionFrameSerializer


class BehaviorOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BehaviorOption
        fields = "__all__"


class BehaviorOptionsStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BehaviorOptionState
        fields = "__all__"


class BehaviorFrameOptionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BehaviorFrameOption
        fields = "__all__"


class BehaviorFrameOptionReadSerializer(serializers.ModelSerializer):
    # those lines are really important otherwise you cant return the fields here
    option_name = serializers.CharField(source='option.option_name')  # Gets option_name from BehaviorOption
    state_name = serializers.CharField(source='active_state.name')        # Gets name from BehaviorOptionState
    frame = CognitionFrameSerializer(read_only=True)

    class Meta:
        model = models.BehaviorFrameOption
        fields = "__all__"


class XabslSymbolCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.XabslSymbolComplete
        fields = "__all__"


class XabslSymbolSparseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.XabslSymbolSparse
        fields = "__all__"
