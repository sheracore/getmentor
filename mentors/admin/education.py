from django.contrib import admin

from ..models import Education, Major, University
from .duration import DurationAdmin

admin.site.register(University)
admin.site.register(Major)


class EducationAdmin(DurationAdmin):  # TODO change to userdatamodel
    fields = [
        'university',
        'degree',
        'major',
        'location',
        'grade',
        'activities_societies'
    ]
    list_display = [
        'university',
        'degree',
        'major',
        'location',
        'grade',
        'activities_societies'
    ]
    list_filter = [
        'degree'
    ]
    search_fields = [
        'major__name',
        'university__name',
        'activities_societies',
    ]
    exclude = []
    raw_id_fields = [
        'university',
        'major',
        'location',
    ]
    dynamic_raw_id_fields = []
    readonly_fields = [
        'university',
        'major',
        'location',
    ]
    allowed_actions = []
    inlines = []

    def __init__(self, *args, **kwargs):
        parent_class = DurationAdmin
        super(EducationAdmin, self).__init__(*args, **kwargs)

        self.fields = self.fields + parent_class.fields
        self.list_display = self.list_display + parent_class.list_display
        self.list_filter = parent_class.list_filter + self.list_filter
        self.search_fields = self.search_fields + parent_class.search_fields
        self.exclude = self.exclude + parent_class.exclude
        self.raw_id_fields = self.raw_id_fields + parent_class.raw_id_fields
        self.readonly_fields = self.readonly_fields + parent_class.readonly_fields
        self.inlines = self.inlines + parent_class.inlines


admin.site.register(Education, EducationAdmin)
