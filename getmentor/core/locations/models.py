from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from getmentor.utilities.db.abstract_models.basemodel import (
    UserBaseModel, UserBaseModelManager)


class Location(UserBaseModel):
    country = CountryField(verbose_name=_("Country"))
    city = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('City'))

    objects = UserBaseModelManager()

    def __str__(self):
        return f"{self.country} - {self.city}"
