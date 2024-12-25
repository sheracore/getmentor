from django.db import models
from django.utils.translation import gettext_lazy as _

from utilities.db.abstract_models.basemodel import BaseModel, BaseModelManager


class Expertise(BaseModel):
    name = models.CharField(max_length=32, unique=True, verbose_name=_("Name"))
    objects = BaseModelManager()

    def __str__(self):
        return f"{self.name}"
