from drf_spectacular.utils import extend_schema, extend_schema_view

image_viewset_schema = extend_schema_view(
    list=extend_schema(summary="List Images", description="", tags=["Images"]),
    create=extend_schema(summary="Add Images", description="", tags=["Images"]),
    retrieve=extend_schema(summary="Get Image", description="", tags=["Images"]),
    partial_update=extend_schema(
        summary="Patch Image", description="", tags=["Images"]
    ),
    destroy=extend_schema(summary="Delete Image", description="", tags=["Images"]),
    count=extend_schema(summary="Count Images", description="", tags=["Images"]),
    validate=extend_schema(summary="Validate Images", description="", tags=["Images"]),
)
