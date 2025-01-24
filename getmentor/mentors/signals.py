from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Mentor
from .tasks import (invalidate_matcher_cache_after_deleting_mentor_task,
                    invalidate_matcher_cache_after_saving_mentor_task)


@receiver(post_save, sender=Mentor)
def after_save(sender, instance, created, **kwargs):
    if created:
        # Invalidate market cache keys after saving
        invalidate_matcher_cache_after_saving_mentor_task.delay(instance.expertise.pk)


@receiver(post_delete, sender=Mentor)
def after_delete(sender, instance, **kwargs):
    # Invalidate market cache keys after deleting
    invalidate_matcher_cache_after_deleting_mentor_task.delay(instance.expertise.pk)
