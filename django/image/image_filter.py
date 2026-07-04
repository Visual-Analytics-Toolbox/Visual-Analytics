from django_filters import rest_framework as filters
from .models import NaoImage
from django.db.models import Func, IntegerField
from django.db.models.fields.json import KeyTransform


class NaoImageFilter(filters.FilterSet):
    # This allows filtering by ?frame=3155214
    frame = filters.NumberFilter(field_name="frame__id")
    # You can also add other frame attributes
    frame_number = filters.NumberFilter(field_name="frame__frame_number")
    log = filters.NumberFilter(field_name="log")

    # Define the filter explicitly to control its behavior
    labelstudio_url = filters.CharFilter(method="filter_non_values")
    brightness_value = filters.CharFilter(method="filter_non_values")
    blurredness_value = filters.CharFilter(method="filter_non_values")
    annotation = filters.CharFilter(method="filter_non_values")
    known_ball = filters.BooleanFilter(method="filter_known_ball")
    has_annotations = filters.BooleanFilter(method="filter_non_values")

    class Meta:
        model = NaoImage
        fields = {
            "frame": ["exact"],
            "labelstudio_url": ["exact"],
            "brightness_value": ["gt", "lt", "gte", "lte"],
            "blurredness_value": ["gt", "lt", "gte", "lte"],
            "camera": ["exact"],
            "type": ["exact"],
        }

    def filter_known_ball(self, queryset, name, value):
        """
        Traverses: NaoImage -> CognitionFrame -> BallModel -> JSONField
        Dynamically selects ballcandidates or ballcandidatestop based on the camera filter.
        """
        if value is True:
            # 1. Check the 'camera' query parameter (defaults to 'ballcandidates' if not TOP)
            camera_value = self.data.get("camera")
            candidate_relation = (
                "ballcandidatestop" if camera_value == "TOP" else "ballcandidates"
            )

            # 2. Dynamically construct the filter arguments
            filter_kwargs = {
                "frame__ballmodel__representation_data__contains": {
                    "knows": True,
                    "valid": True,
                },
                f"frame__{candidate_relation}__representation_data__has_key": "patches",
            }

            # 3. Construct the dynamic path for the KeyTransform
            transform_path = f"frame__{candidate_relation}__representation_data"

            return (
                queryset.filter(**filter_kwargs)
                .annotate(
                    # Extract the array and count its length using Postgres
                    patches_count=Func(
                        KeyTransform("patches", transform_path),
                        function="jsonb_array_length",
                        output_field=IntegerField(),
                    )
                )
                .filter(
                    # Filter for at least 2 items (as per your gte=2 logic)
                    patches_count__gte=2
                )
                .distinct()
            )

        elif value is False:
            # Excludes images that have a known ball
            return queryset.exclude(
                frame__ballmodel__representation_data__contains={"knows": True}
            ).distinct()

        return queryset

    def filter_non_values(self, queryset, name, value):
        # If the incoming string is "None", return records where the field is actually NULL
        if value == "None":
            return queryset.filter(**{f"{name}__isnull": True})

        if value == "Any":
            return queryset.filter(**{f"{name}__isnull": False})

        if value.lower() in ["true", "false"]:
            bool_value = value.lower() == "true"
            return queryset.filter(**{name: bool_value})

        # Otherwise, perform a standard exact match
        return queryset.filter(**{name: value})
