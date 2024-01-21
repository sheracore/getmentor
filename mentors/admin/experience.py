from django.contrib import admin

from ..models import (Company, Experience, ExperienceSkill, Role,  # noqa F401
                      Skill)

admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(ExperienceSkill)
admin.site.register(Role)
admin.site.register(Company)
