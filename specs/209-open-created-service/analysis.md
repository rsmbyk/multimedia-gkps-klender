# Analysis: a newly created service opens on the reading stage

**Spec**: `specs/209-open-created-service/spec.md`
**Plan**: `specs/209-open-created-service/plan.md`
**Tasks**: `specs/209-open-created-service/tasks.md`
**Run**: 2026-11-21 · base `989347f2`

## Artifact digests (sha256, first 12)

| Artifact | Digest |
| --- | --- |
| `spec.md` | `f975fb98e48a` |
| `plan.md` | `9663b41cf6dd` |
| `research.md` | `e08018e01816` |
| `data-model.md` | `fb01ef23ccca` |
| `quickstart.md` | `49d78ecb071a` |
| `tasks.md` | `6c4f87cf23a52` |
| `checklists/requirements.md` | `2647fad85d03f` |

## Checks

`check_pack_consistency.py specs/209-open-created-service --paths`: PASS COVERAGE 10/10 ids traced,
PASS SPLIT declared 14/2/0 = counted 14/2/0, PASS ASSIGNMENT 13 plan symbols / 13 in tasks,
PASS PATHS 17/17 exist. Focused local test command was run on the base commit:
`tests.e2e.test_editor.EditorE2ETests.test_add_empty_active_tatib` — 1 test OK (SQLite,
`DJANGO_DEVELOPMENT_MODE=true`).

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | process | `plan.md` | `CONSTITUTION.md` is absent, so the Constitution Check has no principles to apply. | accepted — SDD-01 makes it optional; no escalation needed |
| A2 | MED | test | `tests/e2e/test_editor.py` | `test_add_empty_active_tatib` finds the new service by `get_by_text('Ibadah Baru', exact=True)`; with the stage populated that matches both the row and the heading (Playwright strict mode). | fixed mechanically in tasks T008 — click the `.book` row by `[data-name]` |
| A3 | LOW | naming | `spec.md` | The spec calls the target state "open on the stage" in prose and pins it with URL/heading/current-row/child-pane values in US1 and SC-001. | accepted — the values make the wording measurable |
| A4 | LOW | scope | `plan.md` | No full-suite run is declared locally; per repo custom, browser E2E belongs to the push step. | accepted — the plan declares the two focused modules and the push-step matrix remains manual |

**CRITICAL**: 0 · **HIGH**: 0 · **MED**: 1 · **LOW**: 3

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | stage opens on the created Normal service |
| FR-002 | ✅ | ✅ | in-place navigation and child pane |
| FR-003 | ✅ | ✅ | panel state and other selections unchanged |
| FR-004 | ✅ | ✅ | Template, edit and other record kinds unchanged |
| FR-005 | ✅ | ✅ | validation and failed saves leave the stage put |
| FR-006 | ✅ | ✅ | generate and copy-as-template still navigate |
| SC-001 | ✅ | ✅ | one save, no second click |
| SC-002 | ✅ | ✅ | marker/timeOrigin/`data-nav` |
| SC-003 | ✅ | ✅ | existing template/editor assertions |
| SC-004 | ✅ | ✅ | URL and heading unchanged on refusal |
| US1/AC1 (row selection update) | ✅ | ✅ | T008 inspection row |

**Coverage**: 100% · **CRITICAL**: 0

## Applied mechanically

- Corrected two traceability paths from `static/web/reading/views.py` to
  `multimedia/web/reading/views.py`; the path check then passed 17/17.
- Expanded the Documentation block to root-relative paths so the path check resolves each artifact.

## Escalated

- None. The one owner decision this pack rests on was made at gate 1 (reading stage, in place) and
  is recorded in the spec's Clarifications.

## History
- 2026-11-21 — gate 2 read (digests before ticks: spec `16ded43c2cc0`, tasks `9aa55dd9705d`, checklist `da40515c5069`); 0 CRITICAL, 1 MED fixed mechanically in T008.
- 2026-11-21 — post-Converge re-read after gate ticks and the focus-restoration amendment; digests above, consistency checks still clean.
