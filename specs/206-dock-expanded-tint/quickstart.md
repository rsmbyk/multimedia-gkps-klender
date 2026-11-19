# Quickstart: A whisper of a tint on an open entry header

**Spec**: `specs/206-dock-expanded-tint/spec.md` · Contracts: [none](./contracts/none.md) ·
Data model: [none](./data-model.md)

## Prerequisites

- The repo's venv at `../multimedia-gkps-klender/.venv/bin/python` (Django 4.0.1, Playwright).
- Chromium from `playwright install chromium`.
- A reachable Postgres — the main compose stack's is on `127.0.0.1:59075`.
- No server is needed for the preview: the page is self-contained.

## Run the test this slice edits

```sh
cd ~/Projects/multimedia-gkps-klender-206
export DATABASE_URL='postgres://multimedia:multimedia@127.0.0.1:59075/multimedia'
../multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_obs_dock --tag=e2e --keepdb \
  -k test_an_open_header_tints_at_half_the_hover_face -v 2
```

Red before the rule lands, green after. The same suite without `-k` is the no-change check for the
spec 198 and spec 200 behaviour.

## Look at the wash

```sh
cd ~/Projects/multimedia-gkps-klender-206
python3 -m http.server 8770 --bind 127.0.0.1
```

Open <http://127.0.0.1:8770/specs/206-dock-expanded-tint/preview/index.html> — four strengths side by
side, both themes, real hover, at the OBS panel's 400 px. It is the gate-1 artifact, frozen at the
accepted 4 %.

For the real thing, the dock itself:

```sh
cd ~/Projects/multimedia-gkps-klender-206
export DATABASE_URL='postgres://multimedia:multimedia@127.0.0.1:59075/multimedia'
../multimedia-gkps-klender/.venv/bin/python manage.py runserver 127.0.0.1:8769
```

Open <http://127.0.0.1:8769/obs/dock>, pick a service, open two entries: the open headers carry the
wash, the live entry keeps its green fill, and hovering either shows the pointer face.
