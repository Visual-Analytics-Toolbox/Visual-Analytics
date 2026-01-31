from django.contrib import admin
from .models import (
    Event,
    Game,
    Log,
    LogStatus,
    Experiment,
    VideoRecording,
    Team,
    Robot,
    HealthIssues,
)
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    DropdownFilter,
)


class EventAdmin(ModelAdmin):
    list_display = ("id", "name")


class ExperimentAdmin(ModelAdmin):
    list_display = ("id", "name", "type")


class GameAdmin(ModelAdmin):
    list_display = (
        "event_id",
        "get_id",
        "team1__name",
        "team2__name",
        "half",
        "is_testgame",
    )
    list_select_related = ["team1", "team2"]

    def get_id(self, obj):
        return obj.id

    get_id.short_description = "Game ID"


class GameExperimentFilter(DropdownFilter):
    title = "Content Type"
    parameter_name = "content_type"

    def lookups(self, request, model_admin):
        return [
            ["game", "Game"],
            ["experiment", "Experiment"],
        ]

    def queryset(self, request, queryset):
        if self.value() == "game":
            # Return only entries where experiment is null
            return queryset.filter(experiment__isnull=True)
        elif self.value() == "experiment":
            # Return only entries where experiment is not null
            return queryset.filter(experiment__isnull=False)
        return queryset


class LogAdmin(ModelAdmin):
    list_display = [
        "get_source_id",
        "get_id",
        "get_source_name",
        "is_test",
    ]
    list_select_related = [
        "game",
        "game__event",
        "experiment",
        "game__team1",
        "game__team2",
    ]

    def get_source_id(self, obj):
        if obj.game:
            return f"Game: {obj.game.id}"
        if obj.experiment:
            return f"Exp: {obj.experiment.id}"
        return "-"

    get_source_id.short_description = "Source ID"

    def get_source_name(self, obj):
        if obj.game:
            return f"{obj.game.team1} vs {obj.game.team2} - {obj.game.half}"
        if obj.experiment:
            return obj.experiment.name  # Assuming Experiment has a name field
        return "-"

    get_source_name.short_description = "Details"

    def get_id(self, obj):
        return obj.id

    def is_test(self, obj):
        if obj.game:
            return obj.game.is_testgame
        if obj.experiment:
            return True

    get_id.short_description = "Log ID"
    is_test.boolean = True


class LogStatusAdmin(ModelAdmin):
    # TODO: add this search field to every model that is related to log
    search_fields = ["log__log_path__icontains"]
    list_display = ["get_log_id", "get_log_path"]

    def get_log_id(self, obj):
        return obj.log.id

    def get_log_path(self, obj):
        return obj.log.log_path

    get_log_id.short_description = "Log ID"
    get_log_path.short_description = "Log Path"


class VideoRecordingAdmin(ModelAdmin):
    list_display = ["get_game_id", "video_path", "url", "type"]

    def get_game_id(self, obj):
        return obj.game.id


class TeamAdmin(ModelAdmin):
    list_display = ["id", "get_team_id", "get_team_name"]

    def get_team_id(self, obj):
        return obj.team_id

    def get_team_name(self, obj):
        return obj.name

    get_team_id.short_description = "Team ID"
    get_team_name.short_description = "Team Name"


class RobotAdmin(ModelAdmin):
    list_display = [
        "head_number",
        "model",
        "version",
        "body_serial",
        "head_serial",
        "purchased",
        "warranty_end",
    ]


# this is required for every model
@admin.register(HealthIssues)
class CustomAdminClass(ModelAdmin):
    pass


admin.site.register(Event, EventAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(LogStatus, LogStatusAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(VideoRecording, VideoRecordingAdmin)
admin.site.register(Robot, RobotAdmin)
