import pytz
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from faker import Faker

from getmentor.core.files.models import FileType
from getmentor.utilities.db.abstract_models.basemodel import (BaseModel,
                                                              BaseModelManager)
from getmentor.utilities.db.fields import FileField


class GenderType(models.IntegerChoices):
    MALE = 0
    FEMALE = 1
    CUSTOM = 2


class LanguageType(models.TextChoices):
    ENGLISH_US = "en_US", "English (US)"
    ENGLISH_UK = "en_GB", "English (UK)"
    PERSIAN = "fa", "فارسی"
    ARABIC = "ar", "العربیه"
    ESTONIAN = "et", "eesti keel"

    @classmethod
    def detect_current_language(cls):
        """The id of the Enum member."""
        try:
            lang = get_language()
            or_lang = lang.split("-")[0].split("_")[0]
            if len(lang) > 1:
                for value in LanguageType.values:
                    if value.find(lang) == 0:
                        return value
                for value in LanguageType.values:
                    if value.find(or_lang) == 0:
                        return value
            raise AttributeError()
        except AttributeError:
            lang = "en_US"
        return lang


def default_language():
    return LanguageType.detect_current_language()


def default_username():
    username = Faker().user_name()[:9]
    if UserProfile.objects.filter(username=username).exists():
        pk = UserProfile.objects.all().order_by("id").last().pk
        username = f"{username}{pk}"
    return username


class UserProfile(BaseModel):
    user = models.ForeignKey(
        "users.User",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name=(_("User")),
    )
    first_name = models.CharField(
        max_length=20, blank=True, default="", verbose_name=_("First name")
    )
    last_name = models.CharField(
        max_length=20, blank=True, default="", verbose_name=_("Last name")
    )
    username = models.CharField(
        default=default_username,
        max_length=18,
        validators=[
            RegexValidator(
                regex=r"^\w*-*\w*$",
                message=_("Username must be Alphanumeric"),
                code="invalid_username",
            ),
        ],
        verbose_name=_("Username for mention"),
    )
    gender = models.IntegerField(
        null=True,
        blank=True,
        choices=GenderType.choices,
        verbose_name=_("Gender"),
    )
    avatar = FileField(null=True,
                       blank=True,
                       on_delete=models.SET_NULL,
                       allow_type=[FileType.IMAGE],
                       verbose_name=_('Avatar'))
    timezone = models.CharField(
        max_length=100,
        choices=tuple(zip(pytz.common_timezones, pytz.common_timezones)),
        default=pytz.common_timezones[-1],
        verbose_name=_("Time zone"),
    )
    language = models.CharField(
        max_length=5,
        choices=LanguageType.choices,
        default=default_language,
        verbose_name=_("Language"),
    )

    objects = BaseModelManager()
