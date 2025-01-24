from django.db import models
from django.utils.translation import gettext_lazy as _

from getmentor.utilities.db.abstract_models.basemodel import (BaseModel,
                                                              BaseModelManager)


class ExcludedMarket(BaseModel):
    user = models.ForeignKey('users.User',
                             blank=True,
                             null=True,
                             on_delete=models.SET_NULL)
    expertise = models.OneToOneField('mentors.Expertise',
                                     on_delete=models.CASCADE,
                                     help_text=_("Expertises to be excluded in the market"))

    objects = BaseModelManager()

    def __str__(self):
        return f'{self.expertise}'
