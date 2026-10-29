# Preview: a passage and a song carry their own kind mark

**Spec**: `specs/144-passage-song-icons/spec.md`
**Shape**: `static` comparison of four candidates, plus the live slice server
**Open**: `specs/144-passage-song-icons/preview/preview.html` (click the bar) or
`compare.html` (all four side by side), or live at `/tatib/144/` on the slice's server

`/tatib/144/` is the service with all five kinds in it: one passage, four songs, one text entry and
three media files. It is the page the request came from.

## Run

```sh
cd ~/Projects/multimedia-gkps-klender-144
DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8830 --noreload
```

Open `http://127.0.0.1:8830/tatib/144/`. The static pages are regenerated from that server:

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/144-passage-song-icons/preview/build_preview.py
```

## Why the stylesheet is frozen

`preview/assets/*.css` are `static/styles/design/*.css` as of `05379336` — `develop` at the commit
this slice branched from — copied by the build script, not linked. **Now** has to keep showing the
stage without a kind mark after the working tree grows one; linking the live stylesheet would turn
**Now** into a second **A**.

Two things are injected into the page by the build script, because a static page runs no server and
no script: the kind marks themselves (the template will render them server-side) and the media
chip's glyph, which `media-stage.js` normally fills in at runtime from its own path table.

## The four candidates

| | mark | title starts at | title column | passage row | song row `Bait 1-7` | song row `HAL 7` |
| --- | --- | --- | --- | --- | --- | --- |
| **Now** | none | 32px | 302px | 56px | 62.5px | 62.5px |
| **A · Glyph in the media column** | 20 × 20, x = 44 (centre 54 = the chip's centre), centred on the row | **84px** | **250px** | 56px | 86.3px | 86.3px |
| **B · Glyph on the title** | 20 × 20, x = 32, riding the title's first line on a 30px hanging indent | 62px | 272px | 56px | 62.5px | 86.3px |
| **C · Outline chip** | 30 × 30, x = 33, 1px `--divider` ring, no fill | 75px | 259px | 56px | 86.3px | 86.3px |
| **D · Tinted chip** | 30 × 30, x = 33, `--head-ink` at 9% | 75px | 259px | 56px | 86.3px | 86.3px |

**A is the adopted one**, with the media row's own columns: the chip runs x = 33…75 (centre 54) and
a media title starts at x = 84, and A puts the glyph's centre and the passage/song title on exactly
those two lines. Its title column is therefore the media title's — 250px — which is why all four
songs wrap here and none of the other candidates wraps more than two.

Measured in headless Chromium on the static pages, which carry the live page's own markup in a
400px column — the reading pane a 1440px window produces with both sidebars open. Every number is a
row's own box; the preview's rows are 420px wide because the stage hangs 10px each side of the pane.

**The one cost no candidate avoids:** `HAL 7 — Porini Dong Marribu Hali` measures **295.6px** on one
line and today's title column is **302px**, so any mark at all — the narrowest indent is 30px —
wraps that title onto a second line at this pane width. Two of the four songs in this service are
that title. At a 1920px window the pane is 880px and nothing wraps.

**There is no gutter to hang a mark in.** The row already hangs 10px outside the reading pane on
each side (`.tatib__item { margin-inline: -10px }`), so a mark outside the row would sit over the
page's own gap, outside the row's hover fill. Every candidate keeps it inside the row.

## Why each one is shaped the way it is

- **A** is the media chip's seat, a bare glyph instead of a chip, on the chip's own centre line and
  on the media title's column: one left rail for every kind. On a row that also has a `Bait` line the
  glyph sits between the title and the verse line, because the row's centre is there — not on the
  title. This is the adopted candidate.
- **B** is the same glyph moved onto the title's own first line: the mark is inside the heading, the
  heading carries a 30px hanging indent so wrapped words still line up under the words, and the
  `Bait` line takes the same 30px so the block keeps one left edge. It costs the least width, and it
  was the recommendation before the owner asked for the media columns instead.
- **C** and **D** keep the chip's anatomy — a rounded square at the row's left — so the family
  resemblance is strongest; they are told apart from the media chip by size (30 vs 42px), by the
  absence of the accent colour, and (C) by having no fill at all.
- The glyphs are the same stroke language as the media chip's: 24 viewBox, 1.8 stroke, round caps.
  Passage is an open book, song is a single flagged note — deliberately not the audio chip's beamed
  double note.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| Now | open the page, `Now` (default) | no mark anywhere; the passage title's left edge is the row's own 12px padding |
| A / B / C / D | press a candidate | the mark's glyph, its seat, and the title's new left edge |
| text rows | press **Mark text rows too** | a paragraph glyph on the `VOTUM` row — the second question, not part of the ask |
| hover | press **Show hover** | the second row takes `--icon-hover-bg`; the mark keeps `--head-ink` on it — 4.77:1 light / 5.23:1 dark |
| dark | press **Dark** | `--head-ink` on `--canvas` is 5.57:1 light / 6.59:1 dark; the media chip's `--focus` glyph is 6.08:1 / 5.89:1, so the media chip still reads as the heavier mark |

## Screenshots

`shots/` holds each candidate rendered at 400px, plus the four-column sheet and B in dark theme.
They are evidence for the record; the pages above are what to judge from.
