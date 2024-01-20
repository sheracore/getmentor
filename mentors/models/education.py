from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from utilities.db.fields import MonthField, YearField


class Degree(models.TextChoices):
    NO_DEGREE = 'NO_DEGREE', _('No Degree')
    HIGH_SCHOOL_DIPLOMA = 'HIGH_SCHOOL_DIPLOMA', _('High School Diploma')
    ASSOCIATE = 'ASSOCIATE', _('Associate')
    BACHELOR = 'BACHELOR', _('Bachelor')
    MASTER = 'MASTER', _('Master')
    DOCTOR = 'DOCTOR', _('Doctor')


class University(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Major(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Education(models.Model):
    # mentor_fk
    university = models.ForeignKey(
        University,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('university'))
    degree = models.CharField(
        choices=Degree.choices,
        verbose_name=_('Degree'))
    major = models.ForeignKey(
        Major,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Major'))
    grade = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        verbose_name=_('Grade'))
    start_year = YearField(
        last_n_year=50,
        blank=True,
        null=True,
        verbose_name=_('Start Year'))
    end_year = YearField(
        last_n_year=50,
        blank=True,
        null=True,
        verbose_name=_('End Year'))
    start_month = MonthField(
        blank=True,
        null=True,
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

    def __str__(self):
        return f"{self.major.name} at {self.university.name}"

    def clean(self):
        super(Education, self).clean()
        if self.start_year and not self.end_year:
            raise ValidationError({'end_year': _('this field is required')})
        if self.start_month and not self.end_month:
            raise ValidationError({'end_month': _('this field is required')})
        if self.end_year and not self.start_year:
            raise ValidationError({'start_year': _('this field is required')})
        if self.end_month and not self.start_month:
            raise ValidationError({'start_month': _('this field is required')})
