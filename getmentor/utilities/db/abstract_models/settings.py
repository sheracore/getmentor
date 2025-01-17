from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .basemodel import BaseModel, BaseModelManager


class AdminSettingsManager(BaseModelManager):

    @property
    def _cache_key(self):
        return f"settings_{self.model._meta.app_label}_{self.model._meta.model_name}"

    def get(self, *args, **kwargs):
        obj = cache.get(self._cache_key)

        if not obj:
            # Fetch from the database or create if it doesn't exist
            obj, _ = self.get_or_create(*args, **kwargs)

            # Store the object in the cache
            cache.set(self._cache_key, obj, 24 * 60 * 60)
        return obj

    def clear_cache(self):
        cache.delete(self._cache_key)


class AdminSettings(BaseModel):

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        child_model_class = type(self)
        if not self.pk and child_model_class.objects.exists():
            # If trying to create a new row and a row already exists, raise an error
            raise ValidationError(_("Only one instance of Setting is allowed"))

        # Clearing cache after updating the settings
        child_model_class.objects.clear_cache()


# TODO: Implement User Settings
