from django_filters import rest_framework as filters
from .models import CognitionFrame


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
