from django_filters import rest_framework as filters


class BehaviorFrameOptionFilter(filters.FilterSet):
    log = filters.NumberFilter(field_name="frame__log")
    active_state = filters.NumberFilter(field_name="active_state")
    option = filters.NumberFilter(field_name="option")


class XabslSymbolSparseFilter(filters.FilterSet):
    log = filters.NumberFilter(field_name="frame__log")
