"""The addresses this release retires, and the archive over them (spec 194).

One table, three readers: `multimedia/obs/urls.py` and `multimedia/web/urls.py`
build their 302 patterns from `routes()`, the pre-existing `/songs/books*` moves
come from `legacy_routes()`, and `/archive/…` asks `successor()` where an old
address lives today. Because the direct routes and the archive read the same
tuples, they cannot disagree, and next release deletes this file plus the marked
blocks in the two URLconfs and `multimedia/urls.py` — nothing else.

Every answer here is a 302. The release claims nothing permanent: the addresses
are retired for a release, not deleted, and the next release decides per address
between a 301 and reuse.

The three `/songs/books*` rows are older than this slice and keep their 301. What
changed is where they point: their old targets lived under `/manage/`, which this
release retires, so they now name the reading pages.
"""

import re
from urllib.parse import unquote

from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.urls import path, re_path
from django.views.generic import RedirectView


# --- spec 194: the retirement ------------------------------------------------

# (old path without its edges, live successor). Both slash forms are registered,
# so APPEND_SLASH never answers one of them with a 301 of its own.
RETIRED = (
    ('home', '/'),
    ('obs/bible/dock', '/obs/dock'),
    ('obs/songs/dock', '/obs/dock'),
    ('obs/tatib/dock', '/obs/dock'),
    ('obs/bible/source', '/obs/blank'),
    ('obs/songs/source', '/obs/blank'),
    ('obs/tatib/source', '/obs/blank'),
    ('obs/project/source', '/obs/blank'),
    ('obs/project/settings', '/'),
)

# (prefix, successor): everything under it goes to the root.
RETIRED_PREFIXES = (
    ('manage', '/'),
)

# (regex on the path without its edges, destination template). These keep 301.
LEGACY = (
    ('songs/books', '/songs/'),
    ('songs/books/(?P<book_id>[0-9]+)', '/songs/book/{book_id}/'),
    ('songs/songs/(?P<song_id>[0-9]+)', '/songs/{song_id}/'),
)


def redirect(destination):
    """A 302 to `destination`, carrying the request's query string on."""
    return RedirectView.as_view(url=destination, permanent=False, query_string=True)


def _belongs(old, prefix):
    """Whether `old` is mounted under `prefix`.

    The root URLconf (`prefix=''`) owns the paths with no slash in them; the
    `/obs/` URLconf owns the ones below `obs/`. A retirement belongs to exactly
    one of the two, so neither URLconf registers an address it does not serve.
    """
    return old.startswith(prefix + '/') if prefix else '/' not in old


def routes(prefix=''):
    """The 302 patterns for the URLconf mounted at `prefix`."""
    patterns = []
    for old, destination in RETIRED:
        if not _belongs(old, prefix):
            continue
        relative = old[len(prefix) + 1:] if prefix else old
        patterns.append(path(relative, redirect(destination)))
        patterns.append(path(relative + '/', redirect(destination)))
    if not prefix:
        for old, destination in RETIRED_PREFIXES:
            patterns.append(re_path(r'^%s(?:/.*)?$' % old, redirect(destination)))
    return patterns


def _legacy_view(destination):
    def view(request, **kwargs):
        url = destination.format(**kwargs)
        query = request.META.get('QUERY_STRING')
        if query:
            url = '%s?%s' % (url, query)
        return HttpResponsePermanentRedirect(url)
    return view


def legacy_routes():
    """The three pre-existing 301 moves, re-pointed at the reading pages."""
    return [re_path(r'^%s$' % regex, _legacy_view(destination))
            for regex, destination in LEGACY]


def successor(path):
    """The live address for a retired or archived one; the path itself otherwise.

    Computed from the tables, never by asking the server, so an archive answer is
    one hop: `/archive/manage/songs/12/` does not pass through `/manage/…`.

    A path carrying a backslash answers `/`. A browser reads `/\\evil.example` as
    `//evil.example`, so an archive address must never be able to name another host.
    """
    if '\\' in path:
        return '/'
    if not path.startswith('/'):
        path = '/' + path
    key = path.strip('/')
    for prefix, destination in RETIRED_PREFIXES:
        if key == prefix or key.startswith(prefix + '/'):
            return destination
    for old, destination in RETIRED:
        if key == old:
            return destination
    for regex, destination in LEGACY:
        match = re.fullmatch(regex, key)
        if match:
            return destination.format(**match.groupdict())
    # Collapse the edge slashes: '//evil.example' is another host to a browser, and
    # the tail's own trailing slash is the only one worth keeping.
    trailing = '/' if path.endswith('/') and key else ''
    return '/%s%s' % (key, trailing)


def archive(request, rest=''):
    """The old version, reachable for one release: 302 to the live successor."""
    destination = successor(unquote(rest))
    query = request.META.get('QUERY_STRING')
    if query:
        destination = '%s?%s' % (destination, query)
    return HttpResponseRedirect(destination)
