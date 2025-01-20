from django.db import models
from django.utils.translation import gettext_lazy as _

from getmentor.utilities.db.abstract_models.basemodel import (BaseModel,
                                                              BaseModelManager)


class University(BaseModel):
    user = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=128, unique=True, verbose_name=_("Name"))

    objects = BaseModelManager()

    class Meta:
        verbose_name = _('University')
        verbose_name_plural = _('Universities')

    def __str__(self):
        return self.name
