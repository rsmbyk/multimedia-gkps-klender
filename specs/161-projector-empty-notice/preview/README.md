# Preview: the projector's empty notice

**Spec**: `specs/161-projector-empty-notice/spec.md`
**Shape**: `static` — one page, the product's own stage markup, tokens and stylesheet
**Open**: `specs/161-projector-empty-notice/preview/preview.html` directly

The four boards are the display's own 1920×1080 stage, fitted at full size and then scaled to fit
the window (capped at 45%), so the page reads on a wide display and still fits the desktop preview
pane; the readout is always in the display's own coordinates.

## Run

```sh
# none: open the file directly. The stylesheets it draws with are copies:
python3 specs/161-projector-empty-notice/preview/build_preview.py   # refresh them from the base commit
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/161-projector-empty-notice/preview/probe.py                  # re-measure, refresh shots/
```

`assets/{fonts,tokens,projector}.css` are `static/styles/design/*.css` as of `24a6d6d2` (develop, the
base commit), copied by the build script rather than linked, so the **Today** column keeps drawing
develop's rules. `fonts.css` is re-pointed at the repository's committed faces
(`static/assets/fonts/`) because the copied file's own path points at a folder this pack does not
carry; the faces are the display's own, so the fitting measures the real type. `shots/` is what
`probe.py` writes and is not committed.

## Boards

| Board | State | What to look for |
| --- | --- | --- |
| empty · Today | empty service, nothing showing | the notice alone, centred near the bottom — the state the page is supposed to have |
| empty · This slice | the same, after the change | identical: with nothing else on the stage the notice stays |
| Go To · Today | a passage detoured onto the empty service | the passage's words, **and the empty-service sentence printed under them** — the defect |
| Go To · This slice | the same, after the change | the passage alone; the words take the band the notice held, the fitted type 103 → 107px |

The readout under the boards prints both columns' own boxes on the 1920×1080 stage; they match the
live page's reading in the spec (`## What the page does today`, `## UI/UX`), including the notice's
755×38.4 box and the stage's 945.6 → 984 heights.

## What the page does not show

It does not fetch: the passage is the product's own painted payload for Matius 5:1, typed into the
markup, so the Go To panel, its loading lock, the chapter fetch and the screens that a song detour
pages through are absent. It also draws the display as `data-showing="true"` only; the released and
`Update` re-read states are behaviour, and each one looks like one of the four boards (notice shown
or not) — the live route below is where those are exercised.

## Live check

The same page on the running app, from the worktree (serves `develop`'s projector code and the real
database):

```sh
cd ~/Projects/multimedia-gkps-klender-161
DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8765 --noreload
```

Open `http://127.0.0.1:8765/projector?service=147` (a Tata Ibadah with no items), press `g`, type
`Mat 5`, press `Enter`: the passage paints and the notice stays under it. `Escape` returns to the
service and the notice stays as it is.
