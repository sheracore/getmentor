from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .basemodel import BaseModel, BaseModelManager


class AdminSettingsManager(BaseModelManager):

    def _cache_key(self):
        return f"settings_{self.model._meta.app_label}_{self.model._meta.model_name}"


class AdminSettings(BaseModel):

    class Meta:
        abstract = True

    def clean(self, *args, **kwargs):
        super().clean()
        child_model_class = type(self)
        if child_model_class.objects.exists():
            # If trying to create a new row and a row already exists, raise an error
            raise ValidationError(_("Only one instance of Setting is allowed"))


# TODO: Implement User Settings
