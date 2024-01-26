from django.db import models
from django.utils.translation import gettext_lazy as _

from core.links.models import Link
from utilities.db.models import BaseModel, BaseModelManager

from ..utilities import AbstractDurationModel


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


class Experience(AbstractDurationModel, BaseModel):
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
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, verbose_name=_("Experience"))
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name=_("Skill"))

    def __str__(self):
        return f"{self.experience}---skill-->{self.skill}"

    objects = BaseModelManager()


class Certificate(AbstractDurationModel, BaseModel):
    # TODO mentor_fk
    name = models.CharField(
        max_length=128,
        verbose_name=_("name"))
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name=_("Company")
    )
    credential_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text=_("If you have critical id for your certificate please insert here"),
        verbose_name="Credential ID", unique=True)
    credential_url = models.ForeignKey(
        Link,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Credential URL"))

    objects = BaseModelManager()

    def __str__(self):
        return f"{self.name} from {self.company.name}"

    class Meta:
        verbose_name = _('License and Certificate')
        verbose_name_plural = _('Licenses and Certificates')
