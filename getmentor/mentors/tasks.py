from celery import shared_task

from .models.expertise import Expertise


@shared_task
def invalidate_matcher_cache_after_saving_mentor_task(expertise_obj_id):
    """ If new mentor expertise does not exist in the market,
        remove the market cache to maybe add in new market calls """
    from getmentor.matcher.services import DynamicMarket

    expertise_obj = Expertise.objects.get(pk=expertise_obj_id)
    if expertise_obj.name not in DynamicMarket.market_expertises():
        DynamicMarket.clear_cache()


@shared_task
def invalidate_matcher_cache_after_deleting_mentor_task(expertise_obj_id):
    """ If new mentor expertise exists in the market,
        remove the market cache to maybe remove in new market calls """
    from getmentor.matcher.services import DynamicMarket

    expertise_obj = Expertise.objects.get(pk=expertise_obj_id)
    if expertise_obj.name in DynamicMarket.market_expertises():
        DynamicMarket.clear_cache()
