from django.db import models
from django.utils.translation import gettext_lazy as _

from core.users.models import User
from utilities.db import BaseModel, BaseModelManager

from .expertise import Expertise


class Mentor(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    expertise = models.ForeignKey(Expertise, on_delete=models.CASCADE,
                                  verbose_name=_('Expertise'))

    objects = BaseModelManager()

    def __str__(self):
        return f"{self.user}-{self.expertise}"
