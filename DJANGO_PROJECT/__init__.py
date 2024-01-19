from .celery import *  # noqa F401
from .celery import app as celery_app
from .settings import *  # noqa F401

__all__ = ["celery_app"]
