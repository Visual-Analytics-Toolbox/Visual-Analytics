from django_filters import rest_framework as filters
from .models import NaoImage


class NaoImageFilter(filters.FilterSet):
    # This allows filtering by ?frame=3155214
    frame = filters.NumberFilter(field_name="frame__id")
    # You can also add other frame attributes
    frame_number = filters.NumberFilter(field_name="frame__frame_number")
    log = filters.NumberFilter(field_name="frame__log")

    # Define the filter explicitly to control its behavior
    labelstudio_url = filters.CharFilter(method="filter_non_values")
    brightness_value = filters.CharFilter(method="filter_non_values")
    blurredness_value = filters.CharFilter(method="filter_non_values")

    class Meta:
        model = NaoImage
        fields = {
            "frame": ["exact"],
            "labelstudio_url": ["exact"],
            "brightness_value": ["gt", "lt", "gte", "lte"],
            "blurredness_value": ["gt", "lt", "gte", "lte"],
            "camera": ["exact"],
            "type": ["exact"],
            "validated": ["exact"],
        }

    def filter_non_values(self, queryset, name, value):
        # If the incoming string is "None", return records where the field is actually NULL
        if value == "None":
            return queryset.filter(**{f"{name}__isnull": True})

        # Otherwise, perform a standard exact match
        return queryset.filter(**{name: value})
