from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False, verbose_name=_('Email'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Is staff'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['is_staff']

    class Meta:
        app_label = "users"
        verbose_name = _('User')
        verbose_name_plural = _('Users')


# ----------------------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
# import uuid

# from django.contrib.auth.models import (
#     AbstractBaseUser,
#     BaseUserManager,
#     PermissionsMixin,
# )
# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from phonenumber_field.modelfields import PhoneNumberField
#
# from learnwise.utilities.db.models import DataModel
#
# from .usersenum import UserEnum
#
#
# class UserManager(BaseUserManager):
#     # use_in_migrations = True
#     def get_queryset(self):
#         return super(UserManager, self).get_queryset()
#
#     def active(self):
#         return self.get_queryset().filter(is_active=True)
#
#     # python manage.py createsuperuser
#     def create_superuser(self, username, is_staff=True, password=''):
#         user = self.model(username=username, is_staff=is_staff, is_active=True, is_superuser=True)
#         user.save()
#         return user
#
#     # it's must be like this one because the base user like this
#     def create_user(self, username, is_staff=False, is_active=True, password=''):
#         user = self.model(username=username, is_staff=is_staff, is_active=True)
#         user.save()
#         return user
#
#     def system(self):
#         return self.get_queryset().get(username=UserEnum.SYSTEM.value)
#
#     def guest(self):
#         return self.get_queryset().get(username=UserEnum.GUEST.value)
#
#
# # PermissionsMixin
# class User(AbstractBaseUser, PermissionsMixin, DataModel):
#     password = None
#     username = PhoneNumberField(region="IR", unique=True, verbose_name=_('Username'))
#     is_staff = models.BooleanField(default=False, verbose_name=_('Is staff'))
#     is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
#
#     objects = UserManager()
#
#     USERNAME_FIELD = "username"
#     # REQUIRED_FIELDS must contain all required fields on your User model,
#     # but should not contain the USERNAME_FIELD or password as these fields will always be prompted for.
#     REQUIRED_FIELDS = ['is_staff']
#
#     class Meta:
#         app_label = "users"
#         verbose_name = _('User')
#         verbose_name_plural = _('Users')
#
#     def __str__(self):
#         return '{}'.format(self.username)
#
#     def info(self, provider):
#         obj, is_created = self.userinformation_set.get_or_create(user=self, provider=provider)
#         if is_created:
#             provider_info = provider.providerinfo
#             obj.timezone = provider_info.timezone
#             obj.language = provider_info.language
#             obj.save()
#         return obj
