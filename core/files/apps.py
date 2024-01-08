from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FilesConfig(AppConfig):
    name = "core.files"
    app_label = "files"
    verbose_name = _("File")
    verbose_name_plural = _("Files")
