from django.db import models
from django.utils.translation import gettext_lazy as _

from getmentor.core.links.models import Link
from getmentor.core.locations.models import Location
from getmentor.utilities.db.abstract_models.basemodel import (
    UserBaseModel, UserBaseModelManager)
from getmentor.utilities.db.abstract_models.durationmodel import \
    AbstractDurationModel

from .company import Company
from .mentor import Mentor


class Certificate(AbstractDurationModel, UserBaseModel):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, verbose_name=_("Mentor"))
    name = models.CharField(
        max_length=128,
        verbose_name=_("Name"))
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

    objects = UserBaseModelManager()

    def __str__(self):
        return f"{self.name} from {self.company.name}"

    class Meta:
        verbose_name = _('License and Certificate')
        verbose_name_plural = _('Licenses and Certificates')
