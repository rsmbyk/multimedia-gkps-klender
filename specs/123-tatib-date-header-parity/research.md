# Research: Match the Tata Ibadah date header to the songbook header

**Spec**: `specs/123-tatib-date-header-parity/spec.md`
**Date**: 2026-10-24

## Unknowns remaining: 0

## Where the two headers diverge

Both pages render the same element — `reading/base.html:355` writes `<p class="read__eyebrow"
id="readEyebrow">` for every reading route, and its text is set per route in
`multimedia/web/reading/views.py` (song citation at `:1824`, service date at `:1885`). The look divides in
the stylesheet:

| Rule | File:line | Values |
| --- | --- | --- |
| shared base | `static/styles/design/components.css:1015` | 16.5px / weight 600 / line-height 1.65 / .12em / uppercase / ink at .78 |
| Tata Ibadah override | `static/styles/design/components.css:2547` (develop) | `font-size: 11px; letter-spacing: .08em; white-space: nowrap` |
| Tata Ibadah margin | `static/styles/design/components.css:1173` | `margin-bottom: 0` so the eyebrow centres with the 34px Project button |

## Why the override exists

`git log -S"font-size: 11px; letter-spacing: .08em"` lands on `7ffd243a` — spec 112's media-handoff work,
which put the Project button, the update control, and the transfer rail on the eyebrow's row. The date was
shrunk to keep that row on one line. Spec 102 (accepted) records the eyebrow at 16.5px / .12em for this
same element, so the code has been diverging from an accepted spec since spec 112 — this slice restores
102's values and supersedes 112's size/tracking half only.

## What the tests already pin

- `tests/e2e/test_reading.py::ReadingE2ETests::test_tatib_date_and_project_button_are_vertically_centered` —
  `marginBottom == 0px`, date/button centre delta ≤ 1px, date right ≤ button left, title below the row, at
  1440 and 390. Re-run against the preview build: **passes** (the header still pairs at both widths).
- `tests/e2e/test_reading.py:1111,1117` — `.read__head-top` height ≥ 34px: unaffected by a 34→69px row.
- `multimedia/web/tests.py:313,319` — the header **text** (`23 Agustus 2026`, `Tata Ibadah`): untouched.
- `tests/e2e/test_offline_library.py:213-218` and `tests/e2e/test_saved_render_parity.py:64,79,164` — the
  saved renders pin the eyebrow's text, not its style; `static/web/offline-render.js:545` reuses
  `#readEyebrow` inside the same shell, so the saved page inherits the corrected rule with no JS change.

## Measured behaviour of the taller date (preview build)

Header row content: date 171px + 12px gap + Project 88px = **271px**. Observed on the running page, opened
by click from `/`:

| Window | Stage header row | Result |
| --- | --- | --- |
| 1440px, both sidebars open | 400px | one row, 34px, centre delta 0.00px |
| 1280px, both sidebars open | 240px | two rows, 69px, button beneath the date, no page overflow |
| 390px, mobile shell | 290px | one row, 34px, centre delta 0.00px |

The 390px case matters: it is the width the existing centring test uses, and the row there is wide enough
for the pair, so that pin stays valid.

## Alternatives considered

- **Keep 11px and only widen the tracking.** Rejected: it reproduces the current look, which is the defect.
- **Shrink the date below a breakpoint to keep one row.** Rejected by the owner at Clarify (2026-10-24): the
  Project action wraps beneath the date instead, so the date keeps one size everywhere.
- **Raise the base `.read__eyebrow` instead of touching the override.** Rejected: it would resize the Bible,
  Kidung, and media-library headers, which are the reference and must not move.
- **Use a container query for the wrap.** Rejected: `flex-wrap` already reflows on the actual available width,
  which is what the row needs; a container query would need a named container on `.stage` and a breakpoint
  guess for a date whose width varies with the month name.
