from drf_spectacular.utils import extend_schema, extend_schema_view

mattermost_gitlab_trigger_view_schema = extend_schema_view(
    post=extend_schema(
        summary="Trigger GitLab Pipeline from Slack",
        description="",
        tags=["AI"],
    ),
)
