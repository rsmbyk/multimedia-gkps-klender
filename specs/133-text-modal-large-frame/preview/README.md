# Preview: a text entry's large frame

**Spec**: `specs/133-text-modal-large-frame/spec.md`
**Route**: `/tatib/<id>/` on the worktree's own server — `http://127.0.0.1:8768/`

## Run

```sh
# from this worktree, against the compose database (read-only for this preview)
cd /home/rsmbyk/Projects/multimedia-gkps-klender-133
export PW=$(grep -m1 'POSTGRES_PASSWORD:' docker-compose.yml | sed 's/.*POSTGRES_PASSWORD: *//')
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:59075/multimedia"
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8768 --noreload
```

Ports 8766 and 8767 belong to the 132 worktree's server; 8768 is this slice's.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| New text, empty service | `/tatib/148/` → the `Add Text` tile | 840×760 frame, full-bleed title band, 26px gutters, Text box filling to the action row |
| New text vs New media | same page, `Add Media` tile | the two dialogs are the same box at the same place |
| Single-screen mode | in the dialog, click `Single-screen` | switch thumb slides, hidden `default_screen_mode` = `single_screen`, help line changes, frame does not resize |
| Save guard | type, then clear the Text box | Save enables then disables |
| Edit text, page scrolled | `/tatib/144/` → the text entry's Edit (hover the row) | 840×760 centred on the window at any scroll position, existing text in a 507px box |
| Other kinds unchanged | `/tatib/144/` → `+ Passage`, `+ Song`, a song's Edit | compact 480-wide dialogs, 22px padding |
| Short window | resize to 1280×600 | 840×568, Text box 227px, action row at y=526 |
| Narrow window | resize to 390×844 | 352×760 at (19, 42), title band 64.5px, 18px gutters |
| Dark theme | the theme toggle | same geometry, tokens unchanged |
| Date popover | `/tatib/` → a service's Edit → the date field | the calendar still opens 8px under its trigger, inside the window |

## Measurement

```sh
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/133-text-modal-large-frame/preview/probe_modal_frame.py \
    http://127.0.0.1:8768 /tmp/tatib-133 /tatib/148/ '[data-entry-edit="3"]' /tatib/144/
```

The probe prints the dialog box, content padding, title band, every top-level field, the Text box, the
action row and the two buttons for `+ Text` and `+ Media` at 1440×900, 1280×800 and 390×844, the same
pair in the dark theme, the Edit form on `/tatib/144/`, the switch and Save-guard state, and one
screenshot per state next to the prefix. `[data-entry-edit="3"]` is the one text entry in the local
database; `148`/`144` are the local service ids this preview was measured on.

## Live preview or mockup

**Live preview** — the project's own route and components. The change is in
`static/styles/design/components.css` and `multimedia/web/templates/reading/_entry_form.html`, so the
served page is the real code path; nothing here is drawn twice.

## What is not a preview

A screenshot, a static image and a recording are not previews at either tier.
