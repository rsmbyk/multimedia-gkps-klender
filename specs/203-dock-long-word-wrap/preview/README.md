# Preview: A long word wraps in the dock runner

**Spec**: `specs/203-dock-long-word-wrap/spec.md`
**Shape**: `live`
**Open**: `http://127.0.0.1:8767/obs/dock` → click the service named `hhhh…` (25 Oktober 2026)

## Run

```sh
cd ~/Projects/multimedia-gkps-klender-203
PW=$(docker exec multimedia-gkps-klender-db-1 printenv POSTGRES_PASSWORD)
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:59075/multimedia"
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8767 --noreload
```

The runner is built by `static/web/obs-dock.js` from the fetched projector library, so a static page
cannot show it — this preview is the project's own route, components and tokens, running.

## The change, as one rule

The live server **ships the rule** — a plain run reads the fixed page. `probe.py --restore` puts the value
back to `normal` and reads the before state, so both readings come from one server and one page:

```css
.serviceline, .entryrow__t, .screenerow { overflow-wrap: anywhere; }
```

```sh
cd specs/203-dock-long-word-wrap/preview
PY=~/Projects/multimedia-gkps-klender/.venv/bin/python
$PY probe.py --out shots/after                     # as it ships now
$PY probe.py --restore --out shots/before          # the value restored to normal
$PY probe.py --restore --width 320 --height 900 --out shots/before-320
$PY probe.py --width 320 --height 900 --out shots/after-320
```

Each run writes `measure.json` (every box read from the rendered DOM) plus `picker.png` and
`runner.png`. `shots/` is gitignored.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| picker | open `/obs/dock` | the `hhhh…` name already wraps to 2 lines — `.servicerow__n` has had `overflow-wrap: anywhere` since spec 119 |
| runner, before the rule | `probe.py --restore`, or the same route on `:63404` | the title runs under the three head buttons; the URL entry runs past the panel; a horizontal scrollbar sits across the body |
| runner, as it ships | click that service on `:8767` | the title takes 3 lines inside its own column, the URL takes 2 inside its header, the body has no horizontal scrollbar |
| a run that already fits | rows 2, 3, 5 (`random.jpg`, `images (1).jpeg`) | 1 line, 19.6px header, 38.0px row — identical with and without the rule |
| a run that already breaks | row 4, the 137-character hyphenated filename | 3 lines, 58.7px — identical with and without the rule |
| open block | click any non-live header | the URL screen row wraps inside the row; `Image` and `Rest` rows keep their 28.8px height |
| live row | the highlighted entry | keeps its selected fill and its sticky pin at its own taller height; no chevron |
| narrow | resize the panel to 320px | title 5 lines inside a 148px column, body overflow 271 → 0 |
| wide | resize to 900px | everything already fits; every box unchanged, title still 1 line |
| truncators | a service with a next entry beyond the live one | `.nextband__label` and `.offstrip__label` stay one line ending `…` |

## Measured (456×1087, dark, 1×)

| box | before | after |
| --- | --- | --- |
| `.serviceline` spill | 328px · 1 line · 20.3px | 0px · 3 lines · 60.8px |
| `.dock__head` scroll − client | 170px | 0px |
| `#runBody` scroll − client | 135px | 0px |
| URL entry header spill | 178px · 1 line | 0px · 2 lines |
| URL screen row spill | 97px | 0px |
| number column | 33.6px at left 18 | unchanged |
| chevron | 10px off the row's right, 0px off centre | unchanged |

## What is not a preview

A screenshot, a static image and a recording are not previews. The PNGs in `shots/` are evidence of
a run, not the preview itself.
