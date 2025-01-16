from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from getmentor.utilities.db.abstract_models.basemodel import (
    UserBaseModel, UserBaseModelManager)

from ..utils import time_difference_in_minutes
from .availability import Availability
from .calendar_settings import CalendarSettings


class MentorAvailability(UserBaseModel):
    mentor = models.ForeignKey('mentors.Mentor', on_delete=models.CASCADE)
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)

    objects = UserBaseModelManager()

    class Meta:
        unique_together = ('mentor', 'availability')

    def __str__(self):
        return f"{self.mentor} {self.availability}"

    def clean(self):
        super(MentorAvailability, self).clean()

        # Check availability interval limitation
        calendar_settings = CalendarSettings.objects.get()
        availability_interval = calendar_settings.availability_interval
        new_start, new_end = self.availability.start_time, self.availability.end_time

        if time_difference_in_minutes(new_start, new_end) < availability_interval:
            raise ValidationError(
                {"availability": _(
                    f"Your availabilities interval should be at least {availability_interval} minutes.")})

        # Check if your new availability time slot has overlap with previews availability
        all_mentor_availability = MentorAvailability.objects.filter(mentor=self.mentor)
        for mentor_avail in all_mentor_availability:
            old_avail = mentor_avail.availability
            if not old_avail.day_of_week == self.availability.day_of_week:
                continue

            # Check if it is updating action and availability hasn't changed do nothing
            if self.pk and self.availability.pk == old_avail.pk:
                return

            if new_start < old_avail.end_time and new_end > old_avail.start_time:
                raise ValidationError({'availability': _('Time slots overlap with another availability')})
