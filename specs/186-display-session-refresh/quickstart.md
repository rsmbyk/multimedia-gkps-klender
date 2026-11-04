# Quickstart: a surface re-reads the session it is showing

**Spec**: `specs/186-display-session-refresh/spec.md`

## Prerequisites

The main checkout's virtualenv, the compose Postgres, and Playwright's Chromium — the same setup as
spec 185 (`specs/185-dock-goto/quickstart.md`). No new dependency, no migration.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-186            # this slice's worktree (stacked on 185)
export DATABASE_URL=postgresql://multimedia:multimedia@127.0.0.1:59075/multimedia
```

## Run

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8765 --noreload
```

Then `http://127.0.0.1:8765/obs/dock`: pick a service, project a screen, and delete the session
cookie (DevTools → Application → Cookies → `gkps-session` → delete). Focus the page: the live row and
the eye's `Hide words` go with it, without a reload.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| the dock stops painting a refused state | `<venv>/python manage.py test tests.e2e.test_display_session_refresh --noinput` | all pass |
| the projector does too | the same module | all pass |
| the neighbours still pass | `<venv>/python manage.py test tests.e2e.test_display_session --noinput` | unchanged from the base |

Run with `DATABASE_URL=…/gkps186` so a parallel session's test database cannot collide.

## Not yet runnable

- The E2E module does not exist until Implement's first task.
