from drf_spectacular.utils import extend_schema, extend_schema_view

team_viewset_schema = extend_schema_view(
    list=extend_schema(
        summary="List RoboCup Teams",
        description="Returns a list of all participating RoboCup teams.",
        tags=["Teams"],
    ),
    create=extend_schema(
        summary="Add RoboCup Team",
        description="Register a new RoboCup team.",
        tags=["Teams"],
    ),
    retrieve=extend_schema(
        summary="Get Team",
        description="Get a RoboCup team by database id",
        tags=["Teams"],
    ),
    partial_update=extend_schema(
        summary="Patch Team",
        description="Patch a RoboCup team by database id",
        tags=["Teams"],
    ),
    destroy=extend_schema(
        summary="Delete Team",
        description="Delete a RoboCup team by database id",
        tags=["Teams"],
    ),
)

game_viewset_schema = extend_schema_view(
    list=extend_schema(summary="List Game halves", description="", tags=["Games"]),
    create=extend_schema(summary="Add Game Half", description="", tags=["Games"]),
    retrieve=extend_schema(summary="Get Game Half", description="", tags=["Games"]),
    partial_update=extend_schema(
        summary="Patch Game Half", description="", tags=["Games"]
    ),
    destroy=extend_schema(summary="Delete Game Half", description="", tags=["Games"]),
)
