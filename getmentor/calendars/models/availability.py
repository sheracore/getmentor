from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from getmentor.utilities.db.abstract_models.basemodel import (
    UserBaseModel, UserBaseModelManager)

from ..utils import time_difference_in_minutes


class Weekdays(models.IntegerChoices):
    MONDAY = 1, _('Monday')
    TUESDAY = 2, _('Tuesday')
    WEDNESDAY = 3, _('Wednesday')
    THURSDAY = 4, _('Thursday')
    FRIDAY = 5, _('Friday')
    SATURDAY = 6, _('Saturday')
    SUNDAY = 7, _('Sunday')


class Availability(UserBaseModel):
    day_of_week = models.IntegerField(choices=Weekdays.choices, help_text=_("Day of week"))
    start_time = models.TimeField()
    end_time = models.TimeField()

    objects = UserBaseModelManager()

    class Mets:
        unique_together = ('day_of_week', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.day_of_week} {self.start_time} to {self.end_time}"

    def clean(self):
        super(Availability, self).clean()

        valid_minutes = {0, 30}

        if self.start_time.minute not in valid_minutes:
            raise ValidationError({"start_time": _(f"Start time minute must be between {valid_minutes}.")})

        if self.end_time.minute not in valid_minutes:
            raise ValidationError({"end_time": _(f"End time minute must be between {valid_minutes}.")})

        if self.start_time > self.end_time:
            raise ValidationError({"start_time": _("Start time must be before end time")})

        if time_difference_in_minutes(self.end_time, self.start_time) < 120:
            raise ValidationError({"end_time": _("Your availabilities interval should be at least 120 minutes.")})
