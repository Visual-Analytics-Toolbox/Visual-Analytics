from django_filters import rest_framework as filters
from .models import MotionFrame

class MotionFrameFilter(filters.FilterSet):
    # Define the filter explicitly to control its behavior
    closest_cognition_frame = filters.CharFilter(method='filter_non_values')

    class Meta:
        model = MotionFrame
        fields = ["frame_number", "frame_time", "log", "closest_cognition_frame"]

    def filter_non_values(self, queryset, name, value):
        # If the incoming string is "None", return records where the field is actually NULL
        if value == "None":
            return queryset.filter(**{f"{name}__isnull": True})
        
        # Otherwise, perform a standard exact match
        return queryset.filter(**{name: value})
    
class MotionRepresentationFilter(filters.FilterSet):
    start_pos = filters.CharFilter(method='filter_non_values')
    size = filters.CharFilter(method='filter_non_values')
    log = filters.NumberFilter(field_name="frame__log")
    
    class Meta:
        fields = ["start_pos","frame","size","frame__log"]


    def filter_non_values(self, queryset, name, value):
        # If the incoming string is "None", return records where the field is actually NULL
        if value == "None":
            return queryset.filter(**{f"{name}__isnull": True})
        
        # Otherwise, perform a standard exact match
        return queryset.filter(**{name: value})