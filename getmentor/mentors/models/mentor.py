from django.db import models
from django.utils.translation import gettext_lazy as _

from getmentor.utilities.db.abstract_models.basemodel import (BaseModel,
                                                              BaseModelManager)


class Mentor(BaseModel):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name=_('User'))
    expertise = models.ForeignKey('mentors.Expertise', on_delete=models.CASCADE, related_name='mentors',
                                  verbose_name=_('Expertise'))

    objects = BaseModelManager()

    def __str__(self):
        return f"{self.user}-{self.expertise}"
