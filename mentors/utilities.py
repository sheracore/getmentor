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
    total_year = models.PositiveIntegerField(null=True, blank=True, editable=False, verbose_name=_('Total year'))
    total_month = models.PositiveIntegerField(null=True, blank=True, editable=False, verbose_name=_('Total month'))

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
            if self.start_year > self.end_year:
                raise ValidationError({'start_year': _('this field can not be bigger than end year')})
            if self.end_year == self.start_year and self.start_month > self.end_month:
                raise ValidationError({'start_month': _('this field can not be bigger than end month')})
            if self.start_year == self.end_year and self.start_month == self.start_month:
                raise ValidationError({'end_month': _('this field can not be the same as start month')})

    def save(self, *args, **kwargs):
        if self.end_year and self.end_month:
            total_month = (self.end_year - self.start_year) * 12 + abs(self.end_month - self.start_month)
            self.total_year = total_month // 12
            self.total_month = total_month % 12
        super().save()
