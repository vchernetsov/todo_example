from django.utils import timezone


def tz_now():
    """Function returns current timezone-related current time"""
    return timezone.now()
