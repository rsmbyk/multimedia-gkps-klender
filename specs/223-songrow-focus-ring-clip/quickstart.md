# Quickstart: song-row focus ring is clipped at the list top

**Spec**: `specs/223-songrow-focus-ring-clip/spec.md`

## Prerequisites

- The repo's virtualenv at `../multimedia-gkps-klender/.venv` (Playwright and Chromium are installed).
- A database of its own so a concurrent `manage.py test` in another worktree cannot take the same
  `test_*` database: `gkps223`, below.
- For the live preview: the slice's worktree server on `127.0.0.1:8767`, started from this worktree
  with the shared virtualenv and a `DATABASE_URL` pointing at the local compose database.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-223
export PY=../multimedia-gkps-klender/.venv/bin/python
# Take DATABASE_URL from the running compose web container's environment, replace its host with
# 127.0.0.1 and its database name with gkps223. Credentials are never written to a tracked file:
export DATABASE_URL="postgres://multimedia:***@127.0.0.1:<db-port>/gkps223"
$PY manage.py collectstatic --noinput
```

## Run

The slice's own cases — three, described in `research.md` D005:

```sh
$PY manage.py test tests.e2e.test_songrow_focus_ring --keepdb --noinput
```

The module that must stay green because it owns the rest of this page (FR-005):

```sh
$PY manage.py test tests.e2e.test_reading --keepdb --noinput
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| the first row's whole ring fits | `$PY manage.py test tests.e2e.test_songrow_focus_ring --keepdb --noinput` | red before the fix (`0px >= 2px` is false), green after it (`3px >= 2px`) |
| Tab and key-after-pointer agree | the same module | both cases pass with the same computed UA outline |
| no state restyled | the same module | heights, pitch, `aria-current` and `outlineStyle none` unchanged |
| the reading page is unaffected | `$PY manage.py test tests.e2e.test_reading --keepdb --noinput` | green — its cases run unchanged |
| the ring by hand | open `specs/223-songrow-focus-ring-clip/preview/index.html`, choose **A**, click **Focus top row**, press any key | the ring's top edge is drawn inside the scrollport |

## Not yet runnable

- **The full browser matrix.** It is deferred to the push step; only the slice's module and the
  reading module are run here.
- **The red run before the fix** is recorded in `analysis.md` rather than quoted as a number in
  advance; the test is written and run before `components.css` is touched.
