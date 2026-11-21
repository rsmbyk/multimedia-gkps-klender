# Quickstart: a dead companion says why

**Spec**: `specs/218-restart-log/spec.md`

## Run

```sh
cd ~/Projects/multimedia-gkps-klender-218
../multimedia-gkps-klender/.venv/bin/python manage.py test tests.test_launcher_fonts --keepdb
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| A dead companion's line is printed (SC-001, FR-001, FR-002) | the module's `test_a_companion_that_is_not_running_shows_its_own_last_line` | the stubbed line and `docker compose build` in stderr |
| A healthy companion is not asked (SC-002, FR-004) | `…::test_a_running_companion_is_not_asked_for_its_log` | no `logs` call logged by the stub |
| A failed start runs nothing (SC-003) | `…::test_a_failed_start_runs_no_check` | exit 1, no `exec` call |
| The command is valid (SC-004) | `docker compose logs --no-color --tail 1 media` on the running stack | one line, prefixed `media-1  |` |
| The launchers agree (FR-006) | read `docker/up.sh` and `docker/up.ps1` | the same three lines |

## Not yet runnable

- A genuinely crash-looping companion cannot be staged here without taking the running stack's ports;
  the stub stands in for it, and SC-004 proves the command itself against the real service.
