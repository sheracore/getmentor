from django.db import models
from django.utils.translation import gettext_lazy as _

from getmentor.utilities.db.abstract_models.basemodel import (
    BaseModel, BaseModelManager, UserBaseModel, UserBaseModelManager)


class Industry(BaseModel):
    user = models.ForeignKey('users.User', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=64, help_text=_('Industry name'))
    description = models.TextField(help_text=_('Industry description'))

    objects = BaseModelManager()

    def __str__(self):
        return f"{self.name}"


class Expertise(UserBaseModel):
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT)
    name = models.CharField(max_length=64, unique=True, verbose_name=_("Name"))
    objects = UserBaseModelManager()

    def __str__(self):
        return f"{self.name}"
