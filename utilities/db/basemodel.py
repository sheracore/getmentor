from django.db import models
from django.utils.translation import gettext_lazy as _

"""
DataModel
"""


class BaseModelQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return BaseModelQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class BaseModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""

    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    update_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        abstract = True
