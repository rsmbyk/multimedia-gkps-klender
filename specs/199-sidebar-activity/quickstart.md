# Quickstart: The first sidebar's idle rule, restored

**Spec**: `specs/199-sidebar-activity/spec.md`

## Prerequisites

- Python 3.12 with the repo's venv — from a worktree, `../multimedia-gkps-klender/.venv/bin/python`.
- Playwright 1.47 with its Chromium: `../multimedia-gkps-klender/.venv/bin/playwright install chromium`.
- The compose database reachable: `docker compose port db 5432` (the port is per machine; read it,
  do not assume it).

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-199
export DATABASE_URL="postgres://multimedia:multimedia@127.0.0.1:$(docker compose port db 5432 | cut -d: -f2)/multimedia"
```

No `collectstatic` is needed for the E2E: `ReadingE2ETests` overrides `STATICFILES_STORAGE` to
`StaticFilesStorage`, so `{% static %}` serves `static/web/reading.js` directly, hashed manifest or
not. A live manual look does need `manage.py collectstatic --noinput` first.

## Run

```sh
../multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_reading \
  --tag=e2e --noinput -v 2
```

For the live page (manual checks only):

```sh
../multimedia-gkps-klender/.venv/bin/python manage.py runserver 127.0.0.1:8771 --noreload
```

Open `http://127.0.0.1:8771/alkitab/mat/5` at 1280×900.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| The scroll fix, red first | `… manage.py test tests.e2e.test_reading.ReadingE2ETests.test_panel_scroll_restarts_sidebar_idle_timeout --tag=e2e` on `develop` | fails: the panel collapses before 899 s because the scroll restarted nothing |
| The scroll fix, green | the same command on this branch | passes: open at 899 s, mini at 900 s |
| The short-drag restart | `… .test_short_drag_restarts_sidebar_idle_timeout` | passes: 14:05 release → open at release + 899 s, closed at + 900 s |
| The exclusions | `… .test_second_sidebar_and_stage_activity_does_not_restart_sidebar_idle_timeout` | passes: `#chBody` and a stage wheel change nothing; collapse at 900 s |
| The nine scaled idle tests | the class command above | all pass at 899 000 / 900 000 ms |
| The number exists once | `grep -n IDLE_COLLAPSE_DELAY static/web/reading.js` | two lines: the declaration `= 900000` and its single read in `scheduleIdleCollapse`; no `60000` anywhere in the file |
| No wider surface | `grep -n "addEventListener" static/web/reading.js \| grep -i "activity\|noteSidebar"` | two bindings, both inside the six-name loop; none on `document`/`window` |
| By hand, the thumb | live page, drag the panel's scrollbar thumb, then read `document.getElementById('panelBody').scrollTop` | it changed, and `html[data-nav]` stays `open`; the fifteen-minute consequence is asserted only under the fake clock |

## Not yet runnable

- **A wall-clock wait of fifteen minutes** is not part of any command: the E2E replaces the clock
  (`page.clock.install`) because a real wait belongs to no suite. The manual row above checks the
  event, not the elapsed span.
- **A hidden-tab check** would need a CDP visibility override Chromium's Playwright API does not
  expose here; FR-007 is declared `inspection` in `plan.md` for that reason.
