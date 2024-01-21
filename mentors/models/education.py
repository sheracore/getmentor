from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from utilities.db.fields import MonthField, YearField
from utilities.db.models import BaseModel, BaseModelManager


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

    def __str__(self):
        return self.name


class Major(BaseModel):
    name = models.CharField(max_length=128, unique=True, verbose_name=_("name"))

    objects = BaseModelManager()

    def __str__(self):
        return self.name


class Education(BaseModel):
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
    grade = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        verbose_name=_('Grade'))
    is_current = models.BooleanField(
        default=False,
        verbose_name=_("I am currently working in this role"))
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
    activities_societies = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name=_('Activities and Societies'))

    objects = BaseModelManager()

    def __str__(self):
        # TODO add mentor name
        return f"{self.major.name} at {self.university.name}"

    def clean(self):
        super(Education, self).clean()
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
