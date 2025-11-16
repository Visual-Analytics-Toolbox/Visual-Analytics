from rest_framework.pagination import LimitOffsetPagination


class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 100
    page_size_query_param = "page_size"
