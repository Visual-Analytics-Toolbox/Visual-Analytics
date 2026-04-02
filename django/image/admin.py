from django.contrib import admin
from .models import NaoImage
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import SingleNumericFilter


# Register your models here.
class ImageAdmin(ModelAdmin):
    search_fields = ["get_log_id"]
    list_display = ["frame__log__id", "frame__frame_number", "camera", "type"]
    list_select_related = ["frame", "frame__log"]

    list_filter_submit = True
    list_filter = [
        ("frame__frame_number", SingleNumericFilter),
        ("frame__log__id", SingleNumericFilter),
    ]
    autocomplete_fields = ["frame"]
    show_full_result_count = False

    def get_log_id(self, obj):
        return obj.frame.log.id

    def get_frame_number(self, obj):
        return obj.frame.frame_number

    get_log_id.short_description = "Log ID"
    get_frame_number.short_description = "Frame Number"


class UnfoldAdminClass(ModelAdmin):
    raw_id_fields = ("image",)


admin.site.register(NaoImage, ImageAdmin)
