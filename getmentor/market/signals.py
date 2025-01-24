from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import ExcludedMarket


@receiver(post_save, sender=ExcludedMarket)
def after_save(sender, instance, created, **kwargs):
    from .services import DynamicMarket
    if created:
        # Invalidate market cache keys after saving
        DynamicMarket.clear_cache()


@receiver(post_delete, sender=ExcludedMarket)
def after_delete(sender, instance, **kwargs):
    from .services import DynamicMarket

    # Invalidate market cache keys after deleting
    DynamicMarket.clear_cache()
