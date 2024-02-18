from django.db import models
from django.utils.translation import gettext_lazy as _

from utilities.db.basemodel import BaseModel, BaseModelManager


class Major(BaseModel):
    name = models.CharField(max_length=128, blank=False, verbose_name=_("Name"))

    objects = BaseModelManager()

    def __str__(self):
        return self.name
