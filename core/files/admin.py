from django.contrib import admin

from .models import FileModel


class FileModelAdmin(admin.ModelAdmin):
    fields = [
        "title",
        "file",
        "size",
        "type",
        "blur_hash",
        "duration",
        "status",
    ]
    list_display = [
        "title",
        "size",
        "type",
        "duration",
        "status",
    ]
    list_filter = [
        "type",
        "status",
    ]
    search_fields = [
        "title",
    ]
    exclude = []
    raw_id_fields = []
    dynamic_raw_id_fields = []
    readonly_fields = [
        "size",
        "blur_hash",
        "duration",
    ]
    allowed_actions = []
    inlines = []


admin.site.register(FileModel, FileModelAdmin)
