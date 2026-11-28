# Quickstart: earlier top pin for the live header

**Spec**: `specs/248-dock-top-pin-early/spec.md`

## Prerequisites

- Python venv at `/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python` (Playwright included).
- Compose stack up (`db`, `web`, `media`); the dock runs against its real DB at 127.0.0.1 with the
  compose-published port read at runtime.
- Free port 8793 for the slice's dev server, 63404 for the unchanged compose build.

## Setup

```sh
cd /home/rsmbyk/Projects/multimedia-gkps-klender-248/specs/248-dock-top-pin-early
chmod +x serve.sh run-tests.sh
./serve.sh &                       # collectstatic + runserver 0.0.0.0:8793 --noreload
```

`serve.sh` derives `DATABASE_URL` from the compose `web` container and never prints it.

## Run

```sh
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8793/obs/dock
```

Open `http://127.0.0.1:8793/obs/dock`, pick the first service, make entry 26 live, and scroll down;
the steps are in `preview/README.md`. The unchanged build is `http://127.0.0.1:63404/obs/dock`.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Boundary and geometry | `python preview/probe_boundary.py http://127.0.0.1:8793 after-boundary.json` | first pin at 1056, blockTop -2, pin 0/38 px, 0 boundary mismatches, 0 duplicate headers |
| Old boundary | `python preview/probe_boundary.py http://127.0.0.1:63404 before-boundary.json` | first pin at 1164, blockTop -110 |
| Targeted acceptance | `./run-tests.sh tests.e2e.test_dock_top_pin` | all cases green; the new boundary cases fail on unmodified develop |
| Regression modules | `./run-tests.sh tests.e2e.test_dock_stuck_corner tests.e2e.test_dock_open_reset` | green except separately recorded machine-local reds |

`run-tests.sh` uses the throwaway `gkps248` database so a parallel session cannot lock the shared
Postgres instance. The full browser suite is deliberately deferred to the push step.

## Not yet runnable

- The full `tests.e2e` matrix: deferred to the push step by repo preference; only the named modules
  above are run for this slice.
- Headless Safari/Firefox parity: the probe drives Chromium only, matching the other dock suites.
