from django_filters import rest_framework as filters
from .models import CognitionFrame
from django.db.models import Q

class CognitionFrameFilter(filters.FilterSet):
    # Define the filter explicitly to control its behavior
    closest_motion_frame = filters.CharFilter(method="filter_non_values")

    class Meta:
        model = CognitionFrame
        fields = ["frame_number", "frame_time", "log", "closest_motion_frame"]

    def filter_non_values(self, queryset, name, value):
        # If the incoming string is "None", return records where the field is actually NULL
        if value == "None":
            return queryset.filter(**{f"{name}__isnull": True})

        # Otherwise, perform a standard exact match
        return queryset.filter(**{name: value})
    
class CognitionRepresentationFilter(filters.FilterSet):
    start_pos = filters.CharFilter(method="filter_non_values")
    size = filters.CharFilter(method="filter_non_values")
    log = filters.NumberFilter(field_name="log")
    representation_data_is_empty = filters.BooleanFilter(method="filter_empty_json")

    class Meta:
        fields = ["start_pos", "frame", "size", "frame__log"]

    def filter_empty_json(self, queryset, name, value):
        if value: 
            # TRUE: This part was already working for you, keep it as is
            return queryset.filter(
                Q(representation_data__isnull=True) | 
                Q(representation_data__len=0)
            )
        
        # FALSE: Native Postgres query to get rows that have actual data
        return queryset.filter(representation_data__isnull=False).extra(
            where=[
                "representation_data != '{}'::jsonb",
                "representation_data != '[]'::jsonb"
            ]
        )
        
