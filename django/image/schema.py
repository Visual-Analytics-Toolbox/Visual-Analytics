from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.extensions import OpenApiSerializerExtension

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

class ImageSerializerExtension(OpenApiSerializerExtension):
   
    target_class = 'image.serializers.ImageReadSerializer'

    def map_serializer(self, auto_schema, direction):
        schema = auto_schema._map_serializer(self.target, direction, bypass_extensions=True)
        
        if 'properties' in schema and 'image_url' in schema['properties']:
            schema['properties']['image_url']['description'] = (
                "Relative path. \n\n"
                "**PREFIX REQUIRED:** Prepend `https://logs.berlin-united.com/` "
                "to this value to get the full image URL."
            )
            
        return schema