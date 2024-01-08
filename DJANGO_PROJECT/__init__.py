from .celery import *  # noqa
from .celery import app as celery_app
from .settings import *  # noqa

__all__ = ["celery_app"]
