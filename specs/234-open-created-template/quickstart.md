# Quickstart: a created Template opens on the stage

**Spec**: `specs/234-open-created-template/spec.md`

## Prerequisites

- The compose stack's `db` and `web` services running (the helper reads the web container's
  `DATABASE_URL` at run time; no credential is stored in the repo).
- Main checkout's virtualenv: `/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python`.
- Playwright Chromium installed for the E2E class.

## Setup

From the slice worktree root:

```sh
VENV=/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python
$VENV specs/234-open-created-template/preview/setup_db.py gkps234
```

## Run

```sh
$VENV specs/234-open-created-template/preview/serve.py --port 8774 --worktree "$(pwd)"
```

Open `http://127.0.0.1:8774/` and click through Tata Ibadah. For the before/after comparison,
start the base worktree on another port with the same script and pass `--worktree <base>`.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Base vs slice navigation | `$VENV specs/234-open-created-template/preview/probe.py http://127.0.0.1:8775 http://127.0.0.1:8774` | base stays on the list; slice lands on `/tatib/<id>/?mode=template` |
| Stage geometry | `$VENV specs/234-open-created-template/preview/measure.py` | measured boxes in `preview/README.md` |
| Browser acceptance (at push) | `$VENV specs/234-open-created-template/preview/with_db.py manage.py test tests.e2e.test_editor --keepdb` | new create cases pass; dated/edit/refused/generate/copy cases stay green |

## Not yet runnable

- The full E2E suite is deferred to the push step; only the preview probe and static checks have
  run before then, per the owner's verification preference.
