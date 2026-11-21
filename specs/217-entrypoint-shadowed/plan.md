# Implementation Plan: the runtime entrypoint survives the bind mount

**Spec**: `specs/217-entrypoint-shadowed/spec.md` (Accepted, Gate 1 2026-11-21)
**Branch**: `fix/217-entrypoint-shadowed`
**Bump**: `patch` (D004; shown at Gate 2)
**Preview**: `n/a — the image's entrypoint path; no product surface, markup or stylesheet changes`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | `Dockerfile` (image build), POSIX `sh` for the guard tests |
| Primary dependencies | none new |
| Existing patterns | `tests/test_entrypoint_line_endings.py` (spec 216) parses the `Dockerfile` and runs the strip command on a CRLF fixture; `tests/test_launcher_fonts.py` drives a launcher through a stubbed `docker` |
| Storage | none |
| Testing | new `tests/test_runtime_entrypoint.py`; `tests/test_entrypoint_line_endings.py` narrowed to the `*.sh` pin |
| Target platform | any checkout; the failing case is a Windows one, whose `web` service mounts it over `/app` |
| Constraints | `docker-compose.yml`'s `.:/app` mount is the development setup and stays; the suite must run without a Docker daemon |
| Scale / scope | 1 file changed in the image, 2 test modules, ~6 tests |

## Constitution Check

No `CONSTITUTION.md` in this repository — nothing to check (SDD-01). Re-checked after Phase 1:
unchanged.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Five decisions: the path (D001), the contents (D002),
the split (D003), the bump (D004), the verification (D005).

## Phase 1 — Design

- `data-model.md` — explicitly none.
- `contracts/none.md` — explicitly none: the container's command surface and the launchers are
  untouched.
- `quickstart.md` — the commands that demonstrate every row.

### Design notes

- The `COPY` names the source explicitly rather than relying on the earlier `COPY . .`, so the runtime
  entrypoint's source is visible next to the line that strips it.
- One `RUN` does the strip and the `chmod`, so the two cannot drift apart or be reordered by a later
  edit without the test noticing.
- The comment above the pair names the mount, because the next reader will otherwise move the file
  back beside the application code.
- `tests/test_entrypoint_line_endings.py` keeps the `*.sh` pin and points at the new module; its
  `Dockerfile`-placement test is deleted, not rewritten — the behaviour it asserted (a strip of
  `docker/entrypoint.sh`) is gone.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 (entrypoint outside `/app`) | `Dockerfile` `COPY` target | `test` → `tests/test_runtime_entrypoint.py::RuntimeEntrypointPathTests::test_the_runtime_entrypoint_lives_outside_the_mounted_tree` | asserts the target does not begin `/app/` and is the path the strip names |
| FR-002 (strip + chmod on that copy) | `Dockerfile` `RUN` | `test` → `…::RuntimeEntrypointStripTests::test_the_copied_entrypoint_runs_after_the_strip` | the command as written, applied to a CRLF fixture, then run under `/bin/sh` |
| FR-003 (`ENTRYPOINT` names it; nothing inside the tree is required) | `Dockerfile` `ENTRYPOINT` | `test` → `…::RuntimeEntrypointPathTests::test_the_image_starts_from_that_path_and_no_other` | exactly one absolute path in the line, and it is the copied one |
| FR-004 (`media` and `web` both start) | built image + `docker-compose.yml:25` | `manual` — the image run with the CRLF checkout mounted at `/app` exits 0; without the mount it exits 0 too | the two shapes the services take |
| SC-001 (the bind-mounted shape runs) | built image | `manual` — `docker run --rm -v <crlf-checkout>:/app gkps217-proof echo OK` → `OK`, exit 0 | today it exits 2 |
| SC-002 (path outside the mount) | `Dockerfile` | `test` → the FR-001/FR-003 rows | |
| SC-003 (both services `Up` from a CRLF checkout) | running stack | `manual` — `docker compose build && docker compose up -d` with a CRLF `docker/entrypoint.sh`; `docker ps` shows `web` and `media` `Up` | the operator's own machine is the only place this runs end to end |
| US1/AC1–2 | built image | `manual` — the SC-001 row | |
| US1/AC3 (an LF checkout is unchanged) | `Dockerfile` | `test` → `…::test_the_strip_leaves_an_lf_entrypoint_untouched` | |
| Edge: no bind mount | built image | `manual` — the image run without `-v` exits 0 | |
| Edge: a Linux checkout | — | `inspection` — both copies are LF; `git check-attr eol` still answers `lf` (`tests/test_entrypoint_line_endings.py`) | |
| Edge: path inside the container | built image | `manual` — `command -v` inside the container answers `/usr/local/bin/gkps-entrypoint.sh` | |
| Edge: contents and order unchanged | `docker/entrypoint.sh` | `inspection` — the file is byte-identical to the version spec 216 verified | |

**Verification split**: `5 test · 2 inspection · 3 manual`.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/217-entrypoint-shadowed/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  converge.md  fold.md
  contracts/none.md  checklists/requirements.md
```

### Source

```
Dockerfile                              (COPY + strip to /usr/local/bin, ENTRYPOINT there)
tests/test_runtime_entrypoint.py        (new)
tests/test_entrypoint_line_endings.py   (narrowed to the *.sh pin)
docs/spec/local-stack.md                (Fold: R4 modified)
backlog/board.md, backlog/items/ITEM-232-entrypoint-shadowed.md, backlog/items/ITEM-233-stale-image-signal.md
CHANGELOG.md, VERSION                   (delivery commit)
```

### Structure Decision

No new directory: the runtime-path guards join `tests/` beside the checkout guard they extend, and
the change itself stays inside the `Dockerfile` step that already prepares the entrypoint.