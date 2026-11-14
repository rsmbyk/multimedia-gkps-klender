"""The Tata Ibadah list's date buckets (spec 132).

The dated list asks "how old is this service", not "which calendar month": the
four buckets below are fixed, and a service's bucket is derived from its date and
the congregation's present day. Nothing here is stored.
"""

from zoneinfo import ZoneInfo

from django.utils import timezone


RECENT_DAYS = 30

BUCKETS = (
    ('upcoming', 'Upcoming'),
    ('last-30-days', 'Last 30 days'),
    ('earlier-this-year', 'Earlier this year'),
    ('older', 'Older'),
)


def present_day():
    """The congregation's calendar day (`Asia/Jakarta`), not the server's UTC date.

    The project runs on UTC; a service dated today would stop counting as today at
    07:00 WIB under that clock, which is the wrong heading for seven hours a day.
    """
    return timezone.now().astimezone(ZoneInfo('Asia/Jakarta')).date()


def bucket_key(day, today):
    """Which bucket a service date falls in. ``today`` is the congregation's day."""
    if day >= today:
        return 'upcoming'
    if (today - day).days <= RECENT_DAYS:
        return 'last-30-days'
    if day.year == today.year:
        return 'earlier-this-year'
    return 'older'


def groups(services, today=None):
    """The panel's buckets: ``(key, label, rows)`` for each bucket that holds rows.

    The caller's own row order is kept, except that ``upcoming`` puts today's rows
    first and leaves the future farthest-first (spec 132): a stable partition is
    the whole rule, so the existing date-descending order supplies the rest.
    """
    today = today or present_day()
    buckets = {key: [] for key, _ in BUCKETS}
    for service in services:
        if service.date is None:
            continue
        buckets[bucket_key(service.date, today)].append(service)
    buckets['upcoming'].sort(key=lambda service: service.date != today)
    return [(key, label, buckets[key]) for key, label in BUCKETS if buckets[key]]
