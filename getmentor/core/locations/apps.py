from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LocationsConfig(AppConfig):
    name = "getmentor.core.locations"
    app_label = "locations"
    verbose_name = _("Location")
    verbose_name_plural = _("Locations")
