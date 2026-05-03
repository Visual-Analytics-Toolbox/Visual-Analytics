from django_filters import rest_framework as filters
from .models import Game


class GameFilter(filters.FilterSet):
    game_folder = filters.CharFilter(method="filter_non_values")

    class Meta:
        model = Game
        fields = ["event", "is_testgame", "game_folder", "start_time", "half"]

    def filter_non_values(self, queryset, name, value):
        # If the incoming string is "None", return records where the field is actually NULL
        if value == "None":
            return queryset.filter(**{f"{name}__isnull": True})

        # Otherwise, perform a standard exact match
        return queryset.filter(**{name: value})
