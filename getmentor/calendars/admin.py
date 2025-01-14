from django.contrib import admin

from .models.availability import Availability
from .models.mentor_availability import MentorAvailability

admin.site.register(Availability)
admin.site.register(MentorAvailability)
