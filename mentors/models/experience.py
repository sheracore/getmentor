from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from utilities.db.fields import MonthField, YearField
from utilities.db.models import BaseModel, BaseModelManager


class Skill(BaseModel):
    name = models.CharField(max_length=64, unique=True, verbose_name=_("name"))

    objects = BaseModelManager()

    def __str__(self):
        return self.name


class Company(BaseModel):
    name = models.CharField(max_length=64, unique=True, verbose_name=_("name"))

    objects = BaseModelManager()

    def __str__(self):
        return self.name


class Role(BaseModel):
    name = models.CharField(max_length=64, unique=True, verbose_name=_("name"))

    objects = BaseModelManager()

    def __str__(self):
        return self.name


class Seniority(models.IntegerChoices):
    ENTRY_LEVEL = 1, _('Entry Level')
    INTERMEDIATE = 2, _('Intermediate')
    SENIOR = 3, _('Senior')
    MANAGER = 4, _('Manager')
    DIRECTOR = 5, _('Director')
    LEAD = 6, _('Lead')
    EXECUTIVE = 7, _('Executive')
    FOUNDER = 8, _('Founder')


class Experience(BaseModel):
    # TODO: mentor_FK
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        verbose_name=_("Role")
    )
    seniority = models.IntegerField(
        choices=Seniority.choices,
        verbose_name=_("Seniority"))

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name=_("Company")
    )
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
    description = models.TextField(
        max_length=1500,
        null=True,
        blank=True,
        verbose_name=_('Activities and Societies'))

    objects = BaseModelManager()

    def __str__(self):
        # add mentor name
        return f"{self.company.name}-{self.role}"

    def clean(self):
        super(Experience, self).clean()
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


class ExperienceSkill(BaseModel):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, verbose_name=_("Experience"))
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name=_("Skill"))

    def __str__(self):
        return f"{self.experience}-{self.skill}"

    objects = BaseModelManager()


class Certificate:
    pass
