# Preview: the add bar opens over the seam

**Spec**: `specs/143-add-bar/spec.md`
**Shape**: `live` — the slice's own server. This slice is a stylesheet and a script, and what it
changes is *motion*: a static page would show the bar's position but not that the page has stopped
moving, which is the whole point.

## Run

```sh
cd ~/Projects/multimedia-gkps-klender-143
DATABASE_URL="postgres://multimedia:<pw>@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8820 --noreload
```

Open `http://127.0.0.1:8820/tatib/142/` (24 text entries, 3 breaks) or `/tatib/144/` (all five kinds).

## The state before this slice

There is no frozen copy of it in this folder: the old behaviour is the same markup and stylesheet at
the commit this branch was cut from, and `git show` gives it back exactly.

```sh
git show 38507a35:static/styles/design/components.css | grep -n "entry__add" -A4
```

That is the in-flow row: `grid-template-rows: 1fr; padding: 8px 0; margin-block: 0` — 43.6px taken
from the page every time a row opens.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| rest | open the route, do not point at the stage | a 1px seam between every pair of blocks, at `.15` opacity — findable, not loud |
| hover | point straight down the list | the entry under the pointer never moves; both its rows open on the seams above and below |
| the bar | keep pointing at one entry | the bar is centred on the column, sitting on its line, with the four buttons unchanged at rest |
| button hover | point at `+ Passage` | a solid `--focus` border and an opaque fill; the seam line does not read through it |
| controls | point at the open entry's Edit | it is fully clickable — the bar's hit area is only as wide as its buttons |
| keyboard | click the page, then Tab | a row opens as its first button takes focus; Tab again walks the four |
| start bar | hover the first entry | the bar opens above it, inside the head's margin, and the first entry does not move |
| separators | scroll to a section break | its rule and diamond are quieter than the divider colour, with 8px more air than an entry |
| dark | press the theme control | the same states with the dark palette |
