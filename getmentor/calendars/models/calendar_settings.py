from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from getmentor.utilities.db.abstract_models import (AdminSettings,
                                                    AdminSettingsManager)


class CalendarSettings(AdminSettings):

    allowed_time_offsets = ArrayField(
        models.IntegerField(
            validators=[MinValueValidator(0), MaxValueValidator(59)]),
        default=list,
        blank=True,
        help_text="Set of intervals in minutes (e.g., [0, 30])"
    )
    availability_interval = models.IntegerField(default=60, validators=[MinValueValidator(15), MaxValueValidator(1440)])

    objects = AdminSettingsManager()
