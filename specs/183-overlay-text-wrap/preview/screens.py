"""Resolve a service's entry index to the screen the overlay paints for it first.

The projector page carries the screen list as a JSON island; each entry's first screen is
the one whose `entry_index` matches and which is not its rest. The probe and the preview
builder both read it, so neither hard-codes an index that moves when the fixture changes.
"""

import json
import re
import urllib.request


def screens(base, service):
    """The projector's screen list for a service, as the overlay's own controller reads it."""
    html = urllib.request.urlopen(f'{base}/projector?service={service}').read().decode()
    match = re.search(r'id="projectorScreenData"[^>]*>(.*?)</script>', html, re.S)
    if not match:
        raise SystemExit('no projectorScreenData island in the page')
    return json.loads(match.group(1))


def first_screen_of(screen_list, entry_index):
    """The screen that opens an entry: the first whose entry_index matches."""
    for position, screen in enumerate(screen_list):
        if screen.get('entry_index') == entry_index:
            return position
    raise SystemExit(f'entry {entry_index} paints no screen')
