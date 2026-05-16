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


robot_viewset_schema = extend_schema_view(
    list=extend_schema(summary="List Robots", description="", tags=["Robots"]),
    create=extend_schema(summary="Add Robot", description="", tags=["Robots"]),
    retrieve=extend_schema(summary="Get Robot", description="", tags=["Robots"]),
    partial_update=extend_schema(
        summary="Patch Robot", description="", tags=["Robots"]
    ),
    destroy=extend_schema(summary="Delete Robot", description="", tags=["Robots"]),
)

event_viewset_schema = extend_schema_view(
    list=extend_schema(summary="List Events", description="", tags=["Events"]),
    create=extend_schema(summary="Add Event", description="", tags=["Events"]),
    retrieve=extend_schema(summary="Get Event", description="", tags=["Events"]),
    partial_update=extend_schema(
        summary="Patch Event", description="", tags=["Events"]
    ),
    destroy=extend_schema(summary="Delete Event", description="", tags=["Events"]),
)

experiment_viewset_schema = extend_schema_view(
    list=extend_schema(
        summary="List Experiments", description="", tags=["Experiments"]
    ),
    create=extend_schema(
        summary="Add Experiment", description="", tags=["Experiments"]
    ),
    retrieve=extend_schema(
        summary="Get Experiment", description="", tags=["Experiments"]
    ),
    partial_update=extend_schema(
        summary="Patch Experiment", description="", tags=["Experiments"]
    ),
    destroy=extend_schema(
        summary="Delete Experiment", description="", tags=["Experiments"]
    ),
)

log_viewset_schema = extend_schema_view(
    list=extend_schema(summary="List Logs", description="", tags=["Logs"]),
    create=extend_schema(summary="Add Log", description="", tags=["Logs"]),
    retrieve=extend_schema(summary="Get Log", description="", tags=["Logs"]),
    partial_update=extend_schema(summary="Patch Log", description="", tags=["Logs"]),
    destroy=extend_schema(summary="Delete Log", description="", tags=["Logs"]),
)

logstatus_viewset_schema = extend_schema_view(
    list=extend_schema(summary="List Log Status", description="", tags=["Log Status"]),
    create=extend_schema(summary="Add Log Status", description="", tags=["Log Status"]),
    retrieve=extend_schema(
        summary="Get Log Status", description="", tags=["Log Status"]
    ),
    partial_update=extend_schema(
        summary="Patch Log Status", description="", tags=["Log Status"]
    ),
    destroy=extend_schema(
        summary="Delete Log Status", description="", tags=["Log Status"]
    ),
)

video_viewset_schema = extend_schema_view(
    list=extend_schema(summary="List Videos", description="", tags=["Videos"]),
    create=extend_schema(summary="Add Videos", description="", tags=["Videos"]),
    retrieve=extend_schema(summary="Get Videos", description="", tags=["Videos"]),
    partial_update=extend_schema(
        summary="Patch Videos", description="", tags=["Videos"]
    ),
    destroy=extend_schema(summary="Delete Videos", description="", tags=["Videos"]),
)

videoslice_viewset_schema = extend_schema_view(
    get=extend_schema(summary="Get Video Slice", description="", tags=["VideoSlices"])
)

model_upload_view_schema = extend_schema(
    summary="Upload Model",
    description="",
    tags=["Model Upload"],
)
dataset_upload_view_schema = extend_schema(
    summary="Upload Dataset",
    description="",
    tags=["Dataset Upload"],
)

healthissues_viewset_schema = extend_schema_view(
    list=extend_schema(
        summary="List Health Issues", description="", tags=["Health Issues"]
    ),
    create=extend_schema(
        summary="Add Health Issue", description="", tags=["Health Issues"]
    ),
    retrieve=extend_schema(
        summary="Get Health Issue", description="", tags=["Health Issues"]
    ),
    partial_update=extend_schema(
        summary="Patch Health Issue", description="", tags=["Health Issues"]
    ),
    destroy=extend_schema(
        summary="Delete Health Issue", description="", tags=["Health Issues"]
    ),
)
