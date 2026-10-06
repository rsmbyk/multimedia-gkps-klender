import re

from django.db.models import Q

from multimedia.songs import models

_BOOK_NUMBER_RE = re.compile(r'^\s*(?P<short>[A-Za-z]+)\s+(?P<number>\d+)\s*$')


def search_songs(query):
    """Return songs matching a free-text ``query``.

    Matches song title, hymn-book name, or hymn-book short name (all
    case-insensitive), plus an exact ``"<short name> <number>"`` book-number
    search such as ``"NKB 12"``. An empty query matches nothing.
    """
    text = (query or '').strip()
    if not text:
        return models.Song.objects.none()

    criteria = (
        Q(title__icontains=text)
        | Q(book__name__icontains=text)
        | Q(book__short_name__icontains=text)
    )

    match = _BOOK_NUMBER_RE.match(text)
    if match:
        criteria |= Q(book__short_name__iexact=match.group('short'), number=int(match.group('number')))

    return (
        models.Song.objects.active().filter(criteria, book__is_deleted=False)
        .select_related('book')
        .order_by('book__name', 'number', 'sub_number', 'title')
    )
