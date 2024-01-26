from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from utilities.db.fields import MonthField, YearField


class AbstractDurationModel(models.Model):
    is_current = models.BooleanField(
        default=False,
        verbose_name=_("I am currently in this organization."))
    start_year = YearField(
        last_n_year=50,
        verbose_name=_('Start Year'))
    end_year = YearField(
        last_n_year=50,
        blank=True,
        null=True,
        verbose_name=_('End Year'))
    start_month = MonthField(
        verbose_name=_('Start Month'))
    end_month = MonthField(
        blank=True,
        null=True,
        verbose_name=_('End Month'))

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if self.is_current:
            if self.end_year or self.end_month:
                raise ValidationError({
                    'is_current': [_('you can not use this field with end_year or end_month at the same time.')],
                })
        else:
            if not self.end_year:
                raise ValidationError({'end_year': _('this field is required')})
            if not self.end_month:
                raise ValidationError({'end_month': _('this field is required')})
