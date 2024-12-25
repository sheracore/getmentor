from django.contrib import admin

from utilities.admin import DurationAdmin

from ..models import Experience, ExperienceSkill, Role, Skill

admin.site.register(Skill)
admin.site.register(ExperienceSkill)
admin.site.register(Role)


class ExperienceAdmin(DurationAdmin):  # TODO change to userdatamodel
    fields = [
        'mentor',
        'role',
        'seniority',
        'company',
        'location',
        'description',
    ]
    list_display = [
        'mentor',
        'role',
        'seniority',
        'company',
        'location',
        'description',
    ]
    list_filter = [
        'seniority',
    ]
    search_fields = [
        'mentor__user__email',
        'role__name',
        'company__name',
        'description',
    ]
    exclude = []
    raw_id_fields = [
        'mentor',
        'role',
        'company',
        'location',
    ]
    dynamic_raw_id_fields = []
    readonly_fields = [
    ]
    allowed_actions = []
    inlines = []

    def __init__(self, *args, **kwargs):
        parent_class = DurationAdmin
        super(ExperienceAdmin, self).__init__(*args, **kwargs)

        self.fields = self.fields + parent_class.fields
        self.list_display = self.list_display + parent_class.list_display
        self.list_filter = parent_class.list_filter + self.list_filter
        self.search_fields = self.search_fields + parent_class.search_fields
        self.exclude = self.exclude + parent_class.exclude
        self.raw_id_fields = self.raw_id_fields + parent_class.raw_id_fields
        self.readonly_fields = self.readonly_fields + parent_class.readonly_fields
        self.inlines = self.inlines + parent_class.inlines


admin.site.register(Experience, ExperienceAdmin)
