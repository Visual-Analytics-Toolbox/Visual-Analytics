from django_filters import rest_framework as filters
from .models import NaoImage

class NaoImageFilter(filters.FilterSet):
    # This allows filtering by ?frame=3155214
    frame = filters.NumberFilter(field_name="frame__id")
    # You can also add other frame attributes
    frame_number = filters.NumberFilter(field_name="frame__frame_number")
    log = filters.NumberFilter(field_name="frame__log")

    class Meta:
        model = NaoImage
        fields = ['frame', 'frame_number', 'log', 'camera', 'type']