from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from getmentor.utilities.db.abstract_models.basemodel import (BaseModel,
                                                              BaseModelManager)

from ..utils import time_difference_in_minutes
from .calendar_settings import CalendarSettings


class Weekdays(models.IntegerChoices):
    MONDAY = 1, _('Monday')
    TUESDAY = 2, _('Tuesday')
    WEDNESDAY = 3, _('Wednesday')
    THURSDAY = 4, _('Thursday')
    FRIDAY = 5, _('Friday')
    SATURDAY = 6, _('Saturday')
    SUNDAY = 7, _('Sunday')


class Availability(BaseModel):
    user = models.ForeignKey('users.User', blank=True, null=True, on_delete=models.SET_NULL)
    day_of_week = models.IntegerField(choices=Weekdays.choices, help_text=_("Day of week"))
    start_time = models.TimeField()
    end_time = models.TimeField()

    objects = BaseModelManager()

    class Mets:
        unique_together = ('day_of_week', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.day_of_week} {self.start_time} to {self.end_time}"

    def clean(self):
        super(Availability, self).clean()

        calendar_settings = CalendarSettings.objects.get()
        valid_minutes = calendar_settings.allowed_time_offsets
        availability_interval = calendar_settings.availability_interval

        if self.start_time.minute not in valid_minutes:
            raise ValidationError({"start_time": _(f"Start time minute must be between {valid_minutes}.")})

        if self.end_time.minute not in valid_minutes:
            raise ValidationError({"end_time": _(f"End time minute must be between {valid_minutes}.")})

        if self.start_time > self.end_time:
            raise ValidationError({"start_time": _("Start time must be before end time")})

        if time_difference_in_minutes(self.start_time, self.end_time) < availability_interval:
            raise ValidationError(
                {"end_time": _(f"Your availabilities interval should be at least {availability_interval} minutes.")})
