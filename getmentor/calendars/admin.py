from django.contrib import admin

from .models.availability import Availability
from .models.calendar_settings import CalendarSettings
from .models.mentor_availability import MentorAvailability

admin.site.register(Availability)
admin.site.register(MentorAvailability)
admin.site.register(CalendarSettings)
