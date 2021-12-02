import functools
import pytz
import config

from datetime import datetime


tz_local = pytz.timezone(config.TIMEZONE)
tz_utc = pytz.utc


@functools.lru_cache()
def get_default_timezone():
    """
    Return the default time zone as a tzinfo instance.
    """
    return tz_local


# Utilities


def localtime(value=None, timezone=None):
    if value is None:
        value = now()
    if timezone is None:
        timezone = get_default_timezone()
    # Emulate the behavior of astimezone() on Python < 3.6.
    if is_naive(value):
        raise ValueError("localtime() cannot be applied to a naive datetime")
    return value.astimezone(timezone)


def localdate(value=None, timezone=None):
    return localtime(value, timezone).date()


def now():
    return datetime.utcnow().replace(tzinfo=tz_utc)


def is_aware(value):
    """
    Determine if a given datetime.datetime is aware.

    The concept is defined in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo

    Assuming value.tzinfo is either None or a proper datetime.tzinfo,
    value.utcoffset() implements the appropriate logic.
    """
    return value.utcoffset() is not None


def is_naive(value):
    """
    Determine if a given datetime.datetime is naive.

    The concept is defined in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo

    Assuming value.tzinfo is either None or a proper datetime.tzinfo,
    value.utcoffset() implements the appropriate logic.
    """
    return value.utcoffset() is None
