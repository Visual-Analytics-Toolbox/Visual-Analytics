from drf_spectacular.utils import extend_schema, extend_schema_view

current_user_viewset_schema = extend_schema_view(
    list=extend_schema(summary="Get User", description="", tags=["Users"]),
)
token_view_schema = extend_schema_view(
    get=extend_schema(summary="Get Token", description="", tags=["Users"]),
)
refresh_token_view_schema = extend_schema_view(
    post=extend_schema(summary="Refresh Token", description="", tags=["Users"]),
)
