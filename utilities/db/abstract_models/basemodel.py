from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()

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


"""
class UserDataModelQuerySet(BaseModelQuerySet):
    def items_staff(self):
        from getmentor.core.users.models import UserProfile

        queryset = self.filter(user_id__in=UserInformation.objects.staff().values_list('user_id'))
        return queryset

    def user(self, user):
        return self.filter(user=user)


class UserBaseModelManager(BaseModelManager):
    def get_queryset(self):
        return ProviderUserDataModelQuerySet(self.model, using=self._db)

    def user(self, user, provider):
        queryset = super(ProviderUserDataModelManager, self).provider(provider).user(user)
        return queryset

    def items_staff(self):
        return self.get_queryset().items_staff()


class UserBaseModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))

    class Meta:
        abstract = True
"""  # noqa
