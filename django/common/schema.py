from drf_spectacular.utils import extend_schema, extend_schema_view

team_viewset_schema = extend_schema_view(
    list=extend_schema(
        summary="List RoboCup Teams",
        description="Returns a list of all participating RoboCup teams.",
        tags=["teams"]
    ),
    create=extend_schema(
        summary="Add RoboCup Team",
        description="Register a new RoboCup team.",
        tags=["teams"]
    ),
    retrieve=extend_schema(
        summary="Get Team",
        tags=["teams"]
    ),
)