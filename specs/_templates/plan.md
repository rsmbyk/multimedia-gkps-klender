# Implementation Plan: <short title>

**Spec**: `specs/NNN-slug/spec.md`
**Branch**: `feat/NNN-slug`
**Bump**: `none` | `patch` | `minor` | `major`
**Preview**: `specs/NNN-slug/preview/` or `n/a — <reason>`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | |
| Primary dependencies | |
| Storage | |
| Testing | |
| Target platform | |
| Project type | |
| Performance goals | |
| Constraints | |
| Scale / scope | |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| <principle from CONSTITUTION.md> | pass · justified | |

Re-checked after Phase 1: <pass | violations and their justification>

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — <entities, or `n/a — <reason>`>
- `contracts/` — <interfaces, or `none`>
- `quickstart.md` — <how to run and verify>

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `path/to/module.py` | `test` → `tests/test_x.py::test_name` | |
| SC-002 | `tests/e2e/test_perf.py` | `test` | p95 ≤ 200 ms |
| US1/AC2 | `path/to/view.js` | `inspection` — <what to look for> | |
| FR-004 | `path/to/config.yml` | `manual` — <steps> | |

**Verification split**: n test · n inspection · n manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/NNN-slug/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/  checklists/  preview/
```

### Source

```
<the concrete layout this slice adds or changes>
```

### Structure Decision

<the real directories chosen, and why — no placeholders left behind>
