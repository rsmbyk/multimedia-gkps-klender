# Quickstart: a checkout made on Windows starts the stack

**Spec**: `specs/216-windows-checkout-start/spec.md`

## Prerequisites

- The repository's Python venv (`../multimedia-gkps-klender/.venv/bin/python`) for the suite.
- `git` — SC-002 reads the attributes through `git check-attr`, not by parsing the file.
- Docker with a daemon, only for the manual row: a machine without one still runs every test row.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-216
```

## Run

The suite rows:

```sh
../multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.test_entrypoint_line_endings tests.test_launcher_fonts --keepdb
```

The attributes row, by hand:

```sh
git check-attr eol -- docker/entrypoint.sh docker/up.sh docker/up.ps1
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| The strip is in the image, after `COPY . .` and before `chmod +x` (FR-001, FR-003) | `grep -n 'entrypoint.sh' Dockerfile` | `sed -i 's/\r$//' docker/entrypoint.sh` sits above `chmod +x docker/entrypoint.sh`, both after `COPY . .` |
| A CRLF entrypoint survives the strip (SC-001, FR-001) | the test builds a CRLF copy, applies the Dockerfile's own strip command, runs `sh <file> true` | exit 0 — without the strip the same file exits 2 with `set: Illegal option -` |
| The shell scripts are pinned, PowerShell is not (SC-002, FR-002) | `git check-attr eol -- docker/entrypoint.sh docker/up.sh docker/up.ps1` | `lf`, `lf`, `unspecified` |
| A dead companion reports instead of aborting (FR-004, FR-005, FR-006, FR-007) | `tests.test_launcher_fonts` with the stub answering `exec` non-zero | one line naming `docker compose logs media`; exit status is the stub's `up` status (0) |
| A running companion with no mounted font still warns (FR-005) | same suite, stub answering `exec` with `0` | the File-Sharing message, unchanged |
| The real image starts from a CRLF checkout (SC-001 end to end) | `docker compose build media && docker compose up -d media`, with `docker/entrypoint.sh` converted to CRLF in the working tree first | `docker ps` shows `media` `Up`, not restarting; restore the file afterwards |

## Not yet runnable

- The `up.ps1` half of FR-004/006/007 cannot be executed here: PowerShell is not installed
  (`command -v pwsh` finds nothing), and `tests/test_launcher_fonts.py` records the same limit for the
  launcher it already covers. Verified by inspection, per D006.
