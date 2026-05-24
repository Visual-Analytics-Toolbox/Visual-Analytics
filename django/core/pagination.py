from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import CursorPagination


class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 100
    page_size_query_param = "page_size"


class CursorPagination(CursorPagination):
    page_size = 100
    page_size_query_param = "limit"
    ordering = "id"  # This automatically handles the fast, indexed ordering!
