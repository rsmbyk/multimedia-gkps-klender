# Quickstart: opening a service starts its entry blocks shut

**Spec**: `specs/204-dock-entry-open-reset/spec.md`

## Prerequisites

- Python 3.12 venv at `~/Projects/multimedia-gkps-klender/.venv` (the worktree's `manage.py` runs
  with it), Playwright and Chromium installed in that venv.
- The compose `db` service running; build a `DATABASE_URL` from `docker compose port db 5432` and
  the password in `docker-compose.yml`. Use a throwaway database name so a parallel session's tests
  cannot collide (e.g. `.../gkps204`).
- `STATICFILES_STORAGE` overridden to Django's plain storage for the browser suites (the module
  carries the decorator itself).
- For the preview only: nothing — it is a static page. A plain file server is optional and gives
  the reload state its cookie fidelity (see `preview/README.md`).

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-204
export DATABASE_URL='postgres://multimedia:***@127.0.0.1:<port>/gkps204'
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_dock_open_reset --keepdb --noinput
```

## Run

```sh
# the gate-1 preview (no server of its own):
xdg-open specs/204-dock-entry-open-reset/preview/index.html
# optional, for the reload state's cookie fidelity:
~/Projects/multimedia-gkps-klender/.venv/bin/python -m http.server 8899 --bind 127.0.0.1 \
  --directory specs/204-dock-entry-open-reset/preview
# then http://127.0.0.1:8899/index.html

# the real dock, once Implement has landed:
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8765 --noreload
# open /obs/dock, pick a service, expand a header, pick another service
```

The dock's JS is cached heuristically by the browser: after changing `obs-dock.js`, hard-reload
(Ctrl+Shift+R). A dev server serving `DJANGO_DEBUG=False` also needs `collectstatic` and a restart
before the manifest names the new file.

## Verify

| Check | Command / steps | Expected |
| --- | --- | --- |
| The new suite, red first | `manage.py test tests.e2e.test_dock_open_reset --keepdb` on the base (`ab46f384`) | the reset tests fail because a non-live block stands open after an open — not an import or selector error |
| The new suite, green | the same command on the slice | every test passes |
| The other dock suites | `manage.py test tests.e2e.test_obs_dock tests.e2e.test_obs_dock_follow tests.e2e.test_dock_keys tests.e2e.test_dock_goto tests.e2e.test_dock_bucket_head multimedia.web.test_obs_dock --keepdb` | unchanged results; a red identical on `develop` is carded with that evidence |
| The preview's states | `preview/probe.py [url]` | 64 states per behaviour, 0 page errors; `drafted` paints `[]` after every open, `today` paints the leak |
| An open writes nothing | `preview/probe_open_write.py [url]` | 10 opens: bytes identical, 0 channel messages, 0 morph frames, scrollTop 0 |
| The keyboard open path | `preview/probe_enter_path.py [url]` | `drafted` `[]`, `today` `[3]` |

The heavy browser suites run at the push step by the owner's standing preference; until then a
targeted module or the preview probes are the evidence.

## Manual checks

1. Open a service, click the header of position 4 — its block opens, nothing goes on air.
2. Back to the picker, open a different service — every block shut, no chevron down anywhere.
3. Back, open the *same* service again — every block shut.
4. Open positions 2, 4 and 9, then open a shorter service — nothing open at any position.
5. Click a screen row inside position 4 so it goes on air; open another service (nothing open
   there), then return — position 4's block is open, tinted, with no chevron.
6. With a block open by hand, project another entry — the hand-opened block stays open.
7. With a block open by hand, wait for a re-read (or save a change in another browser) — the block
   stays open and the list stays where it was.
8. Reload — every hand-opened block is gone; only the live entry's block is open.

## Not yet runnable

- `tests.e2e.test_dock_open_reset` is written red-first at Implement; before that task it does not
  exist, and the command above is the lane it will use.
- A live preview of the unmerged implementation is not available until Implement; the gate-1
  artifact is the static preview, whose dock script carries the drafted line gated on a flag.
