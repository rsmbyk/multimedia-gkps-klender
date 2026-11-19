# Quickstart: a clicked service keeps its date

**Spec**: `specs/201-sidebar-date-focus/spec.md`

## Prerequisites

- Python 3.12 virtualenv at `../multimedia-gkps-klender/.venv` with `requirements-dev.txt`.
- `playwright install chromium`.
- The worktree's `manage.py` run with that venv; collectstatic once for page-rendering tests.

## Setup

```sh
cd /home/rsmbyk/Projects/multimedia-gkps-klender-201
../multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
```

## Run

```sh
../multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_sidebar_date_reveal --keepdb
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Preview states | `cd specs/201-sidebar-date-focus/preview && ../../../.venv/bin/python probe.py` | `preview assertions: PASS`, clicked state `block` in the proposal panel and `none` in today's |
| Focused E2E | `manage.py test tests.e2e.test_sidebar_date_reveal --keepdb` | all cases green |
| No touch regression | same E2E module's touch case | controls drawn, date painted |

## Not yet runnable

- Nothing in this slice: the E2E and the static preview both run on this machine.
