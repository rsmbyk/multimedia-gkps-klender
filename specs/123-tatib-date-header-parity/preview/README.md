# Preview: Tata Ibadah date header parity

**Spec**: `specs/123-tatib-date-header-parity/spec.md`
**Route**: `/` → rail **Tata Ibadah** → a dated service (opens `/tatib/148/`); undated template `/tatib/84/`;
song reference `/songs/1351/`

## Run

```sh
DATABASE_URL=postgres://… .venv/bin/python manage.py runserver 0.0.0.0:8766 --noreload
```

From this worktree (`fix/123-tatib-date-header-parity`). The stylesheet is served per request, so a CSS
edit shows on reload with no restart.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| default | open a dated service (25 Oktober 2026) at a wide window | date set like the song page's songbook header (16.5px / .12em / ink .78), one row with Project, centres aligned |
| reference | open `/songs/1351/` | the songbook header the date now has to match |
| responsive — wrapped | narrow the window until the stage is under ~271px of header width (1280 with both sidebars open here) | Project drops beneath the date on an 8px gap, date keeps its full size, row grows 34px → 69px, no sideways scroll |
| responsive — mobile | resize to 390px and open the service from the panel | date and Project still share one row (290px of header), centres aligned |
| undated | `/tatib/?mode=template` → open a template service | the `Tata Ibadah` label carries the same style |
| saved copy | with the saved library ready, open the same service from the panel while offline | same header; renders through the same classes (not exercised in this preview — see the spec's traceability) |
| empty / error / loading | `n/a — the date is static text with no data dependency` | |

## What is not a preview

A screenshot, a static image and a recording are not previews. The preview is the **running** screen,
built from the project's own components and tokens.
