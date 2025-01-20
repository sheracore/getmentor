from django.db import models
from django.utils.translation import gettext_lazy as _

from getmentor.utilities.db.abstract_models.basemodel import (BaseModel,
                                                              BaseModelManager)


class Skill(BaseModel):
    user = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=64, blank=False, verbose_name=_("Name"))

    objects = BaseModelManager()

    def __str__(self):
        return self.name
