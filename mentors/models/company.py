from django.db import models
from django.utils.translation import gettext_lazy as _

from utilities.db.basemodel import BaseModel, BaseModelManager


class Company(BaseModel):
    name = models.CharField(max_length=64, unique=True, verbose_name=_("Name"))

    objects = BaseModelManager()

    def __str__(self):
        return self.name
