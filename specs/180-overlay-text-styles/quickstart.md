# Quickstart: the overlay reads by kind

**Spec**: `specs/180-overlay-text-styles/spec.md`

## Prerequisites

- The main checkout's virtualenv — `../multimedia-gkps-klender/.venv` — this worktree has none of its own.
- The compose stack's database running (`docker compose up -d db` in the main checkout); its host port comes from
  `docker compose port db 5432`, its password from `docker-compose.yml`. Nothing here needs the `web` container.
- Playwright's Chromium installed in that virtualenv (`playwright install chromium`), which the E2E suite drives.

## Setup

```sh
cd /home/rsmbyk/Projects/multimedia-gkps-klender-165
export DATABASE_URL=postgres://multimedia:<password>@127.0.0.1:<port>/multimedia
export DJANGO_DEBUG=False            # serve the collected static tree, as OBS sees it
../multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
```

`DJANGO_DEBUG=False` makes WhiteNoise serve from `_static/`, so **re-run `collectstatic` after any change to
`static/`** — otherwise the live page keeps the previous CSS and JS.

## Run

```sh
../multimedia-gkps-klender/.venv/bin/python manage.py runserver 127.0.0.1:8816 --noreload
```

- Dock (the only surface with controls): <http://127.0.0.1:8816/obs/dock> — click the service, click an entry.
- Overlay (what OBS shows): <http://127.0.0.1:8816/obs/source/overlay> — transparent, so open it over a frame or in
  OBS itself. Python edits need a restart; template, CSS and JS edits need a reload (and `collectstatic` for the last
  two).

## Preview

- `specs/180-overlay-text-styles/preview/overlay-preview.html` — the 15 states, navigable (◀ ▶ · J K · Home/End ·
  1–9), playing the panel's own motion as you move between kinds.
- `specs/180-overlay-text-styles/preview/overlay-motion.html` — the transitions live, at 1× and ¼× / ⅛×.
- `specs/180-overlay-text-styles/preview/overlay-sequence.html` — the twelve appear/disappear moments as stills.
- `specs/180-overlay-text-styles/preview/overlay-walkthrough.mp4` — the same walk, recorded.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| The overlay's own behaviour | `../multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_obs_overlay --keepdb` | `Ran 10 tests … OK` |
| The dock still drives it | `… manage.py test tests.e2e.test_obs_dock multimedia.web.test_obs_dock --keepdb` | `Ran 16 tests … OK` |
| The screen payload | `… manage.py test multimedia.web.tests.ServiceProjectorTests --keepdb` | `OK` |
| Styles reach the live page | open the overlay, then in devtools: `getComputedStyle(document.querySelector('.obs-overlay__plate')).backgroundColor` | `rgba(10, 12, 16, 0.88)` |
| A step morphs rather than re-enters | in the dock press `↓` twice on a two-verse passage, watch the overlay | the card changes width/height smoothly; no fade-out |

## Not yet runnable

- `n/a` — every command above runs from this worktree today. The recorder that produced `overlay-walkthrough.mp4`
  lives outside the repo (a probe script), so it is evidence, not a reproducible step.
