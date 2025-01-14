from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MentorsConfig(AppConfig):
    name = "getmentor.calendars"
    app_label = "calendars"
    verbose_name = _("Calendar")
    verbose_name_plural = _("Calendars")
