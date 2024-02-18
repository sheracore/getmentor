from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from utilities.db import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True, null=False, verbose_name=_("Email"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Is staff"))

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["is_staff"]

    def __str__(self):
        return f"{self.email}"

    class Meta:
        app_label = "users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")


@receiver(post_save, sender=User)
def user_after_save_receiver(sender, instance, created, **kwargs):
    instance.userprofile_set.get_or_create(user=instance)
