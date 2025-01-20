from django.db import models
from django.utils.translation import gettext_lazy as _

from getmentor.core.locations.models import Location
from getmentor.utilities.db.abstract_models.basemodel import (
    UserBaseModel, UserBaseModelManager)
from getmentor.utilities.db.abstract_models.durationmodel import \
    AbstractDurationModel

from ..company import Company
from ..mentor import Mentor
from .role import Role
from .seniority import Seniority
from .skill import Skill


class Experience(AbstractDurationModel, UserBaseModel):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, verbose_name=_("Mentor"))
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        verbose_name=_("Role")
    )
    seniority = models.ForeignKey(
        Seniority,
        null=True,
        on_delete=models.SET_NULL,
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

    objects = UserBaseModelManager()

    def __str__(self):
        # add mentor name
        return f"{self.role} at {self.company.name}"


class ExperienceSkill(UserBaseModel):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE,
                                   verbose_name=_("Experience"))
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name=_("Skill"))

    def __str__(self):
        return f"{self.experience}---skill-->{self.skill}"

    objects = UserBaseModelManager()
