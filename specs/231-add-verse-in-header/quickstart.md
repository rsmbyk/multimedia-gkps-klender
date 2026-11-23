# Quickstart: Add verse sits beside Project in the song header

**Spec**: `specs/231-add-verse-in-header/spec.md`

## Prerequisites

- Python 3.12 venv at `~/Projects/multimedia-gkps-klender/.venv`.
- The compose `db` and `web` services running (the launcher reads `DATABASE_URL` from `web`).
- Playwright with Chromium for the browser probe.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-231
# no migration, collectstatic or seed step — the share DB already holds editable songs
```

## Run

```sh
bash preview/serve.sh 8772
# http://127.0.0.1:8772/songs/1880/  (two verses, editable)
# http://127.0.0.1:8772/songs/1909/  (empty)
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Unit gate | `manage.py test multimedia.web.reading.test_verse_add_gate` | green after the placement pin is updated |
| Header boxes | browser probe at 1440×900 | Add verse 111×34 at x=1157 then Project 96×34 at x=1276 |
| Empty state | browser probe on `/songs/1909/` | no header buttons; one 112×38 button in the invitation |
| Control works | click `[data-add-verse]` | `#editorModal` opens with `New verse` |

## Not yet runnable

- The full E2E matrix is deferred to the push step per the owner's standing instruction; the
  focused template tests and the live probe are the in-between verification.
