from django.db import models
from django.utils.translation import gettext_lazy as _

from utilities.db import BaseModel, BaseModelManager


class Link(BaseModel):
    title = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name=_('Title'),
    )
    blank = models.BooleanField(
        default=False,
        verbose_name=_('Blank'),
    )
    in_app = models.BooleanField(
        default=False, help_text=_('Open in app, like webview in application'), verbose_name=_('In app')
    )
    description = models.CharField(max_length=255, blank=True, verbose_name=_('Description'))
    url = models.URLField(
        verbose_name=_('URL'),
    )
    variable = models.CharField(
        max_length=255,
        blank=True,
        help_text=_(
            'You can use the following variables in your page link to pass user information via URL '
            'parameters. {{USER_ID}} {{USER_NAME}} {{USER_EMAIL}}'
        ),
        verbose_name=_('Variable'),
    )

    objects = BaseModelManager()

    class Meta:
        verbose_name = _('Link')
        verbose_name_plural = _('Links')

    def __str__(self):
        return "%s - %s" % (self.pk, self.title)
