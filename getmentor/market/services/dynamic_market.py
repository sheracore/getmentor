from typing import List

from django.core.cache import cache
from django.db.models import Count, F

from getmentor.market.models import ExcludedMarket
from getmentor.mentors.models import Expertise


class DynamicMarket:
    CACHE_KEY = "dynamic_market"

    @classmethod
    def qualified_markets(cls) -> List[dict]:
        """Market choice, dynamically by number of expertise
        :returns
        [
          {
           'name': <expertise>,
           'industry__name': <industry>,
           'mentor_count': <number of mentors of expertise>
          }
        ]
        """

        expertise_mentors = cache.get(cls.CACHE_KEY)
        if not expertise_mentors:
            excluded_markets = ExcludedMarket.objects.values_list('expertise__pk', flat=True)

            # Mentor counts per expertise
            expertise_mentors = list(Expertise.objects.annotate(mentor_count=Count('mentors')).filter(
                mentor_count__gte=F('industry__market_qualified_limitation')).exclude(pk__in=excluded_markets).values(
                'name', 'industry__name', 'mentor_count'))
            cache.set(cls.CACHE_KEY, expertise_mentors, 60 * 60)

        return expertise_mentors

    @classmethod
    def market_expertises(cls) -> List[str]:
        qualified_markets = cls.qualified_markets()
        return list(map(lambda industry: industry.get('name'), qualified_markets))

    @classmethod
    def clear_cache(cls):
        cache.delete(cls.CACHE_KEY)
