# Implementation Plan: Stack Restart Policy

**Spec**: `specs/191-compose-restart/spec.md` (Accepted, Gate 1 2026-11-14)
**Branch**: `feat/191-compose-restart`
**Bump**: `patch` (D005; shown at Gate 2)
**Preview**: `n/a — compose configuration only; no product surface, markup or stylesheet changes`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Docker Compose v2 file (YAML); Python 3.12 for the guard tests |
| Existing patterns | `docker-compose.yml` services `web` / `db` / `media`; media already carries `restart: unless-stopped` (line 64) as the in-file precedent |
| Storage | none — two keys in the compose file; no model, no migration, no stored state |
| Testing | `tests/test_docker_compose.py` (`SimpleTestCase`, `yaml.safe_load`); new class `DockerComposeRestartPolicyTests` beside `DockerComposePortRulesTests` |
| Target platform | the operators' computers: Docker Desktop (macOS/Windows) and Docker Engine (Linux) |

## Constitution Check

No `CONSTITUTION.md` exists in this repository, so there are no principles to check against
(SDD-01 makes it optional and it is never auto-created). Run before Phase 0 — nothing to check.
Re-checked after Phase 1: unchanged, still nothing to check.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Six decisions: the policy value (D001), where it
lives (D002), the services covered (D003), the boot-order window (D004), the bump level (D005),
the verification split (D006).

## Phase 1 — Design

- `data-model.md` — explicitly none: no entities, no stored state.
- `contracts/none.md` — explicitly none: no external interface changes; the `docker compose`
  command surface keeps its shape.
- `quickstart.md` — the commands that demonstrate every traceability row, and which run today.

### Design notes

- Each of `web` and `db` gains a `restart: unless-stopped` key in its service block, placed as the
  `media` service places its own (trailing key of the block), so the file reads as one convention.
- No override files, no launcher changes: the policy must hold for a plain `docker compose up`,
  which is the documented baseline (spec 182's constraint).
- The out-of-band `docker update` repair on the owner's machine (2026-11-14) keeps working and
  becomes redundant once the file lands and the stack is next recreated.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1 / FR-001 (web policy) | `docker-compose.yml` | `test` → `tests/test_docker_compose.py::DockerComposeRestartPolicyTests::test_web_and_db_restart_on_daemon_restart` | media's row already pinned in the same file |
| US1 / FR-002 (db policy) | `docker-compose.yml` | `test` → same function | |
| US1 scenarios 1–2 (the stack returns after a daemon restart) | running stack | `manual` — restart Docker Desktop (or reboot); `docker ps` shows web/db/media `Up`, `curl` on the published web port answers `200` | the only real proof of the runtime behaviour |
| US2 scenario 1 (a deliberate stop stays stopped) | running stack | `manual` — `docker compose stop`, restart the daemon, no service starts itself | guards against `always` |
| SC-001 (serving with no manual step) | running stack | `manual` — shares the US1 proof | |

**Verification split (planned)**: `2 test · 0 inspection · 3 manual`.

## Project Structure (changes)

```
docker-compose.yml
tests/test_docker_compose.py
specs/191-compose-restart/{spec,plan,research,tasks,analysis,converge,fold,...}.md
specs/191-compose-restart/checklists/requirements.md
specs/191-compose-restart/contracts/none.md
docs/spec/local-stack.md        (Fold: R3 added)
backlog/board.md, backlog/items/ITEM-195-compose-restart.md
CHANGELOG.md, VERSION           (delivery commit)
```
