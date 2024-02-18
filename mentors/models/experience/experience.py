from django.db import models
from django.utils.translation import gettext_lazy as _

from core.locations.models import Location
from utilities.db.basemodel import BaseModel, BaseModelManager

from ...utilities import AbstractDurationModel
from ..company import Company
from ..mentor import Mentor
from .role import Role
from .skill import Skill


class Seniority(models.IntegerChoices):
    ENTRY_LEVEL = 1, _('Entry Level')
    INTERMEDIATE = 2, _('Intermediate')
    SENIOR = 3, _('Senior')
    MANAGER = 4, _('Manager')
    DIRECTOR = 5, _('Director')
    LEAD = 6, _('Lead')
    EXECUTIVE = 7, _('Executive')
    FOUNDER = 8, _('Founder')


class Experience(AbstractDurationModel, BaseModel):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, verbose_name=_("Mentor"))
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
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Location')
    )
    description = models.TextField(
        max_length=1500,
        null=True,
        blank=True,
        verbose_name=_('Activities and Societies'))

    objects = BaseModelManager()

    def __str__(self):
        # add mentor name
        return f"{self.role} at {self.company.name}"


class ExperienceSkill(BaseModel):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE,
                                   verbose_name=_("Experience"))
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name=_("Skill"))

    def __str__(self):
        return f"{self.experience}---skill-->{self.skill}"

    objects = BaseModelManager()
