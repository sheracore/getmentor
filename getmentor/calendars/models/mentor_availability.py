from django.core.exceptions import ValidationError
from django.db import models

from getmentor.utilities.db.abstract_models.basemodel import (
    UserBaseModel, UserBaseModelManager)

from .availability import Availability


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
        all_mentor_availability = MentorAvailability.objects.filter(mentor=self.mentor)

        for mentor_avail in all_mentor_availability:
            old_avail = mentor_avail.availability
            if not old_avail.day_of_week == self.availability.day_of_week:
                continue

            if (self.availability.start_time < old_avail.end_time and
                    self.availability.end_time > old_avail.start_time):
                raise ValidationError({'availability': 'Time slots overlap with another availability.'})
