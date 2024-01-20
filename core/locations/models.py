from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class Location(models.Model):
    country = CountryField()
    city = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('City'))

    def __str__(self):
        return f"{self.country} - {self.city}"
