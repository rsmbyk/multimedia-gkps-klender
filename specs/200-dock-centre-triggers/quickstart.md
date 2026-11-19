# Quickstart: the dock follows the live entry only when following

**Spec**: `specs/200-dock-centre-triggers/spec.md`

## Prerequisites

- Python 3.12 venv at `~/Projects/multimedia-gkps-klender/.venv` (the worktree's `manage.py` runs
  with it), Playwright and Chromium installed in that venv.
- The compose `db` service running; build a `DATABASE_URL` from `docker compose port db 5432` and
  the password in `docker-compose.yml`. Use a throwaway database name so a parallel session's tests
  cannot collide (e.g. `.../gkps200`).
- The static files served by name: `STATICFILES_STORAGE` overridden to Django's plain storage for
  the browser suites.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-200
export DATABASE_URL='postgres://multimedia:<pw>@127.0.0.1:<port>/gkps200'
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_obs_dock_follow --keepdb --noinput
```

## Run

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8765 --noreload
# open /obs/dock, pick a service, click an entry to project it
```

The dock's JS is cached heuristically by the browser: after changing `obs-dock.js`, hard-reload
(Ctrl+Shift+R). If a dev server serves `DJANGO_DEBUG=False`, `collectstatic` plus a restart is also
needed before the manifest names the new file.

## Verify

| Check | Command / steps | Expected |
| --- | --- | --- |
| The new suite (red first, then green) | `manage.py test tests.e2e.test_obs_dock_follow --keepdb` | each new test fails on `develop` for the mode reason, then passes on the slice |
| The other dock suites | `manage.py test tests.e2e.test_obs_dock tests.e2e.test_dock_keys tests.e2e.test_dock_goto tests.e2e.test_dock_bucket_head --keepdb` | unchanged results; the known red tests on `develop` stay red identically |
| Gate-1 look and triggers | open `specs/200-dock-centre-triggers/preview/index.html` | crosshair between the arrows; every trigger reachable by hand; probe prints 0 px landings |

The heavy browser suites are run at the push step by the owner's standing preference; until then a
targeted test or the preview probe is enough.

## Manual checks

1. With a service on air, press Next three times: the live row stays in the middle of the list.
2. Scroll the list away, press Next and Back: the live row changes but the list stays put; press
   the centre control: the list returns to the live row and the next advance follows again.
3. Scroll away again and click the sticky **Next** band: the pointer moves to the next entry, its
   first row is marked, that row centres, and following resumes.
4. Leave the dock still for 15 s with the live row off screen, nothing else open and the words up:
   the list centres and following resumes.
5. Expand another entry's header: following ends; the next advance leaves the list alone.
6. Switch appearance to dark and repeat check 2: the control keeps the arrow buttons' filled
   window-focus face.

## Not yet runnable

- The E2E module `tests.e2e.test_obs_dock_follow` is written red-first at Implement; before that
  task it does not exist, and the command above is the lane it will use.
- A live preview of the unmerged implementation is not available until Implement; the gate-1
  artifact is the static preview.
