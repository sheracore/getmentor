from django.db import models
from django.utils import timezone


class YearField(models.PositiveIntegerField):
    """
    To get last n year YearField using last_n_year attribute
    Usage example:
        years = YearField(last_n_year=50)
    """
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', None)
        if not choices:
            last_n_year = kwargs.pop('last_n_year', 10)
            choices = self.get_last_n_year_choices(last_n_year)
        kwargs.setdefault('choices', choices)
        super(YearField, self).__init__(*args, **kwargs)

    @staticmethod
    def get_last_n_year_choices(n):
        current_year = timezone.now().year
        return [(year, str(year)) for year in range(current_year, current_year - n, -1)]


class MonthField(models.PositiveIntegerField):
    MONTH_CHOICES = [
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', self.MONTH_CHOICES)
        super(MonthField, self).__init__(*args, **kwargs)
