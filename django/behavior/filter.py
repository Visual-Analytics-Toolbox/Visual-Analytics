from django_filters import rest_framework as filters
from .models import BehaviorFrameOption


class BehaviorFrameOptionFilter(filters.FilterSet):
    log = filters.NumberFilter(field_name="frame__log")