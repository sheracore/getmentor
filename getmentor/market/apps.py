from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MatcherConfig(AppConfig):
    name = 'getmentor.market'
    app_label = "market"
    verbose_name = _("Market")
    verbose_name_plural = _("Markets")

    def ready(self):
        import getmentor.market.signals  # noqa: F401
