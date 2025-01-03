from django.db import models
from django.utils.translation import gettext_lazy as _

from getmentor.utilities.db.abstract_models.basemodel import (
    UserBaseModel, UserBaseModelManager)

from .expertise import Expertise


class Mentor(UserBaseModel):
    expertise = models.ForeignKey(Expertise, on_delete=models.CASCADE,
                                  verbose_name=_('Expertise'))

    objects = UserBaseModelManager()

    def __str__(self):
        return f"{self.user}-{self.expertise}"
