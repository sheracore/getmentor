from django.db import models
from django.utils.translation import gettext_lazy as _

from getmentor.utilities.db.abstract_models.basemodel import (
    UserBaseModel, UserBaseModelManager)


class Skill(UserBaseModel):
    name = models.CharField(max_length=64, blank=False, verbose_name=_("Name"))

    objects = UserBaseModelManager()

    def __str__(self):
        return self.name
