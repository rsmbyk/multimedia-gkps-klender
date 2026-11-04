# Quickstart: one keyboard grammar for the dock and the projector

**Spec**: `specs/187-keyboard-parity/spec.md` · **Contracts**: `contracts/display-state.md`,
`contracts/keyboard.md` · **Data model**: `data-model.md`

## Prerequisites

- The worktree's virtualenv at `~/Projects/multimedia-gkps-klender/.venv` (the main checkout's).
- The compose stack's `db` service running (`docker compose port db 5432` for the host port).
- Playwright's Chromium installed for the git user that runs the E2E.

## Setup

```sh
cd ~/.hermes/worktrees/187-keyboard-parity
PW=$(grep -m1 'POSTGRES_PASSWORD:' docker-compose.yml | awk '{print $2}')
PORT=$(docker compose port db 5432 | cut -d: -f2)
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:${PORT}/multimedia"
export STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
```

## Run

```sh
# the dock and the projector, from this worktree, on a free port
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8765 --noreload &
# the dock: http://127.0.0.1:8765/obs/dock  ·  the projector: http://127.0.0.1:8765/projector?service=142
```

The preview is a single self-contained file; rebuild it after a source change:

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python specs/187-keyboard-parity/preview/build.py
~/Projects/multimedia-gkps-klender/.venv/bin/python specs/187-keyboard-parity/preview/probe.py
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| The sheet's rows, order and wording | `python specs/187-keyboard-parity/preview/probe.py` | `all checks passed`; 32 rows in five groups on the runner, 34 in six on the picker, 0 labels foreign to the projector, 0 out of its order |
| The dock's keys | `manage.py test tests.e2e.test_dock_keys --keepdb` | green |
| The projector's keys and sheet | `manage.py test tests.e2e.test_projector_keys --keepdb` | green |
| The go to's shared state | `manage.py test tests.e2e.test_goto_shared_state tests.e2e.test_dock_goto --keepdb` | green |
| The dock's own suite | `manage.py test tests.e2e.test_obs_dock --keepdb` | green |
| The projector's own suite | `manage.py test tests.e2e.test_projector --keepdb` | green |

## Not yet runnable

- `tests/e2e/test_dock_keys.py` and `tests/e2e/test_projector_keys.py` do not exist until Tasks run;
  the commands above are the ones they will answer to.
- The dock's `K` sheet, the picker's `G` and the held `Esc` are not in the dock's code yet — the
  preview draws them; the live dock shows today's behaviour until Implement lands.
