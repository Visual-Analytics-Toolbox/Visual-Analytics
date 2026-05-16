from drf_spectacular.utils import extend_schema, extend_schema_view

video_annotation_view_schema = extend_schema_view(
    get=extend_schema(
        summary="Get Video Annotations",
        tags=["Videos"],
    ),
)
