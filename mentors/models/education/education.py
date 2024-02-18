from django.db import models
from django.utils.translation import gettext_lazy as _

from core.locations.models import Location
from utilities.db.basemodel import BaseModel, BaseModelManager

from ...utilities import AbstractDurationModel
from ..mentor import Mentor
from .major import Major
from .university import University


class Degree(models.TextChoices):
    NO_DEGREE = 'NO_DEGREE', _('No Degree')
    HIGH_SCHOOL_DIPLOMA = 'HIGH_SCHOOL_DIPLOMA', _('High School Diploma')
    ASSOCIATE = 'ASSOCIATE', _('Associate')
    BACHELOR = 'BACHELOR', _('Bachelor')
    MASTER = 'MASTER', _('Master')
    DOCTOR = 'DOCTOR', _('Doctor')


class Education(AbstractDurationModel, BaseModel):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, verbose_name=_("Mentor"))
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        verbose_name=_('university'))
    degree = models.CharField(
        choices=Degree.choices,
        verbose_name=_('Degree'))
    major = models.ForeignKey(
        Major,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('Major'))
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Location')
    )
    grade = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        verbose_name=_('Grade'))
    activities_societies = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name=_('Activities and Societies'))

    objects = BaseModelManager()

    def __str__(self):
        # TODO add mentor name
        return f"{self.mentor} at {self.university}"
