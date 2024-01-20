from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MentorsConfig(AppConfig):
    name = "mentors"
    app_label = "mentors"
    verbose_name = _("Mentor")
    verbose_name_plural = _("Mentors")
