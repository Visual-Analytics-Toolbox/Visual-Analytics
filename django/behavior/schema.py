from drf_spectacular.utils import extend_schema, extend_schema_view

behavior_option_viewset_schema = extend_schema_view(
    list=extend_schema(
        summary="List Behavior Options",
        description="",
        tags=["Behavior"]
    ),
    create=extend_schema(
        summary="Add Behavior Option",
        description="",
        tags=["Behavior"]
    ),
    retrieve=extend_schema(
        summary="Get Behavior Option",
        description="",
        tags=["Behavior"]
    ),
    partial_update=extend_schema(
        summary="Patch Behavior Option",
        description="",
        tags=["Behavior"]
    ),
    destroy=extend_schema(
        summary="Delete Behavior Option",
        description="",
        tags=["Behavior"]
    ),
)

behavior_option_state_viewset_schema = extend_schema_view(
    list=extend_schema(
        summary="List Behavior States",
        description="",
        tags=["Behavior"]
    ),
    create=extend_schema(
        summary="Add Behavior States",
        description="",
        tags=["Behavior"]
    ),
    retrieve=extend_schema(
        summary="Get Behavior States",
        description="",
        tags=["Behavior"]
    ),
    partial_update=extend_schema(
        summary="Patch Behavior States",
        description="",
        tags=["Behavior"]
    ),
    destroy=extend_schema(
        summary="Delete Behavior States",
        description="",
        tags=["Behavior"]
    ),
)

behavior_frame_option_viewset_schema = extend_schema_view(
    list=extend_schema(
        summary="List Behavior Frame Options",
        description="",
        tags=["Behavior"]
    ),
    create=extend_schema(
        summary="Add Behavior Frame Options",
        description="",
        tags=["Behavior"]
    ),
    retrieve=extend_schema(
        summary="Get Behavior Frame Options",
        description="",
        tags=["Behavior"]
    ),
    partial_update=extend_schema(
        summary="Patch Behavior Frame Options",
        description="",
        tags=["Behavior"]
    ),
    destroy=extend_schema(
        summary="Delete Behavior Frame Options",
        description="",
        tags=["Behavior"]
    ),
    count=extend_schema(
        summary="Count BehaviorFrameOptions ",
        description="",
        tags=["Behavior"]
    )
)