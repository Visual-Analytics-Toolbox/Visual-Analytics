from django.contrib import admin
from .models import RawGCSituation
from unfold.admin import ModelAdmin


class RawGCSituationAdmin(ModelAdmin):
    list_display = ["uuid", "json_data"]


admin.site.register(RawGCSituation, RawGCSituationAdmin)
