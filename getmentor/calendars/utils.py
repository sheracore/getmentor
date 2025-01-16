from datetime import datetime

from django.db.models import TimeField


def time_difference_in_minutes(start_time: TimeField, end_time: TimeField, ) -> int:
    """
    :param end_time:
    :param start_time:
    :return: int
    """
    # Convert the TimeField values to datetime objects (using today's date)
    start_time = datetime.combine(datetime.today(), start_time)
    end_time = datetime.combine(datetime.today(), end_time)

    # Calculate the time difference
    time_diff = end_time - start_time

    # Get the difference in minutes
    minutes = int(time_diff.total_seconds() / 60)

    return minutes
