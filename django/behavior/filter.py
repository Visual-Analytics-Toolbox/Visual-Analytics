from django_filters import rest_framework as filters


class BehaviorFrameOptionFilter(filters.FilterSet):
    log = filters.NumberFilter(field_name="frame__log")
    frame = filters.NumberFilter(field_name="frame__id")
    frame_number = filters.NumberFilter(field_name="frame__frame_number")
    active_state = filters.NumberFilter(field_name="active_state")
    option = filters.NumberFilter(field_name="option")
    state_name = filters.CharFilter(field_name="active_state__name")
    option_name = filters.CharFilter(field_name="option__option_name")


class XabslSymbolSparseFilter(filters.FilterSet):
    log = filters.NumberFilter(field_name="frame__log")
