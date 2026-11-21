# Quickstart: the runtime entrypoint survives the bind mount

**Spec**: `specs/217-entrypoint-shadowed/spec.md`

## Prerequisites

- The repository venv for the suite; Docker for the manual rows.
- A CRLF checkout to prove the failing shape: `git archive HEAD | tar -x -C <dir>` and rewrite
  `docker/entrypoint.sh` with CRLF (19 CR bytes in the current file).

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-217
```

## Run

```sh
../multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.test_runtime_entrypoint tests.test_entrypoint_line_endings --keepdb
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| The runtime path is outside the mount (FR-001, SC-002) | the suite's `RuntimeEntrypointPathTests` | the `COPY` target does not begin `/app/` |
| The strip makes that copy runnable (FR-002) | the suite's `RuntimeEntrypointStripTests` | CRLF fixture exits 2 before, `reached` after |
| The image starts from that path only (FR-003) | the suite's `test_the_image_starts_from_that_path_and_no_other` | one absolute path in `ENTRYPOINT`, and it is the copy |
| The bind-mounted shape runs (FR-004, SC-001) | `docker build -t gkps217-proof .` in a CRLF context, then `docker run --rm -v <ctx>:/app gkps217-proof echo OK` | `OK`, exit 0 |
| No mount, same result (edge case) | `docker run --rm gkps217-proof echo OK` | `OK`, exit 0 |
| The container's own view (edge case) | `docker run --rm -v <ctx>:/app --entrypoint /bin/sh gkps217-proof -c 'grep -c "$(printf "\r")" /usr/local/bin/gkps-entrypoint.sh'` | `0`, while `/app/docker/entrypoint.sh` still holds 19 |
| Both services `Up` (SC-003) | on the operator's machine: `docker compose build && docker compose up -d`, `docker ps` | `web` and `media` `Up` |

## Not yet runnable

- SC-003's `docker compose` run cannot happen here: the worktree's compose project would compete for
  the running stack's published ports (63404, 59075, 63174). The bind-mount shape above is exactly
  what compose does to `web` (`- .:/app`), so the manual row reproduces it without the conflict.
