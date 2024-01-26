from django.contrib import admin

from ..models import (Certificate, Company, Experience,  # noqa F401
                      ExperienceSkill, Role, Skill)

admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(ExperienceSkill)
admin.site.register(Role)
admin.site.register(Company)
admin.site.register(Certificate)
