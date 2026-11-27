# Quickstart: sidebar mark centring

**Spec**: `specs/237-sidebar-mark-centering/spec.md`

## Prerequisites

- The worktree's slice branch checked out and collectstatic run once after a CSS edit;
  the repository's Python environment with Django and Playwright available.
- A local PostgreSQL database reachable through `DATABASE_URL`, and a Chromium browser
  installed for Playwright. Credentials are deliberately not written into repo artifacts.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-237
python ~/.hermes/cache/scratch/gkps237/run.py collectstatic --noinput
python ~/.hermes/cache/scratch/gkps237/run.py runserver 0.0.0.0:8776 --noreload
```

The launcher reads the database URL from the compose web container and is machine-local;
it is not part of the repo. Hard-reload the browser tab after each static change.

## Run

```sh
# Live preview: open / first, click Tata Ibadah, open service 111ojo.
xdg-open http://127.0.0.1:8776/

# Frozen before/after readouts, both themes at 1440/1024/390px:
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/237-sidebar-mark-centering/preview/probe.py
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Live probe | command above | mark centre `−4/−11.5/−22px` before, `0px` after; number `0px`; x `42/66px` unchanged |
| Targeted E2E | `python ~/.hermes/cache/scratch/gkps237/run.py test tests.e2e.test_sidebar_mark_centring --keepdb` | all tests in the new module pass with a throwaway database; the base rule fails the centre assertions |
| Full browser suite | deferred to the push step per your standing preference | report only; do not run between pushes |

## Not yet runnable

- The targeted E2E module is written during Implement, not before gate 2; the command
  is a path, not a claim that it has already passed.
- The probe needs a Python with Playwright installed and a running local server; both
  are machine-specific and are intentionally not stored in the spec pack.
