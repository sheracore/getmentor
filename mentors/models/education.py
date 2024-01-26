from django.db import models
from django.utils.translation import gettext_lazy as _

from core.locations.models import Location
from utilities.db.models import BaseModel, BaseModelManager

from ..utilities import AbstractDurationModel


class Degree(models.TextChoices):
    NO_DEGREE = 'NO_DEGREE', _('No Degree')
    HIGH_SCHOOL_DIPLOMA = 'HIGH_SCHOOL_DIPLOMA', _('High School Diploma')
    ASSOCIATE = 'ASSOCIATE', _('Associate')
    BACHELOR = 'BACHELOR', _('Bachelor')
    MASTER = 'MASTER', _('Master')
    DOCTOR = 'DOCTOR', _('Doctor')


class University(BaseModel):
    name = models.CharField(max_length=128, unique=True, verbose_name=_("name"))

    objects = BaseModelManager()

    class Meta:
        verbose_name = _('University')
        verbose_name_plural = _('Universities')

    def __str__(self):
        return self.name


class Major(BaseModel):
    name = models.CharField(max_length=128, unique=True, verbose_name=_("name"))

    objects = BaseModelManager()

    def __str__(self):
        return self.name


class Education(AbstractDurationModel, BaseModel):
    # TODO: mentor_fk
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
        return f"{self.major.name} at {self.university.name}"
