# Analysis: a newly created songbook or song opens as its row would

**Spec**: `specs/225-open-created-songbook-song/spec.md`
**Plan**: `specs/225-open-created-songbook-song/plan.md`
**Tasks**: `specs/225-open-created-songbook-song/tasks.md`
**Run**: 2026-11-23 · base `e83e7154`

## Artifact digests (sha256, first 12)

| Artifact | Digest |
| --- | --- |
| `spec.md` | `3cfdc86be68e` |
| `plan.md` | `303dda78211d` |
| `research.md` | `7ffc4e88b598` |
| `data-model.md` | `a1c4137c419f` |
| `quickstart.md` | `0a7d611e27f1` |
| `tasks.md` | `32c39fa05d3e` |
| `checklists/requirements.md` | `b1f91b53c163` |
| `fold.md` | `169fb1e7ed3a` |
| `converge.md` | `25b60dd530f7` |

## Checks

- Consistency: 9/9 requirement IDs in the spec trace to a plan row and a task; the plan's
  verification split (9 test, 0 inspection, 0 manual) matches the traceability rows; every path
  named in the plan's Documentation and Source blocks exists in this worktree. The repo's
  `check_pack_consistency.py` helper is not present in the tree or the vault, so these were checked
  directly rather than by that script.
- Focused verification: six create/edit/refusal E2E tests red on the base code, green after the
  implementation; ten focused tests (including spec 209's two) green in the final run.
- Live reproduction: `reproduce.py` against `127.0.0.1:8768` shows the after-save state matching
  the click-through target for both record kinds, with the in-page marker preserved.

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | process | `plan.md` | `CONSTITUTION.md` is absent, so the Constitution Check has no principles to apply. | accepted — SDD-01 makes it optional |
| A2 | MED | test | `tests/e2e/test_editor.py` | An early implementation skipped the quiet focus restore; the existing spec-025 E2E caught it. | fixed — `restoreRequestedFocus` runs in the navigation promise's `.then`, and the result is recorded as F2 in `converge.md` |
| A3 | LOW | process | `analysis.md` | Gate 2 was accepted on the spec, plan, tasks and requirements checklist; this analysis was written at delivery rather than before that gate. | accepted with a note — 0 CRITICAL and full coverage on re-read; the timing is recorded here rather than rewritten |
| A4 | LOW | scope | `plan.md` | The declared verification is focused; module-wide runs were added as regression checks and surfaced known base failures. | accepted — those failures are carried in `converge.md`, not fixed here |

**CRITICAL**: 0 · **HIGH**: 0 · **MED**: 1 · **LOW**: 3

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | songbook row current, child pane open |
| FR-002 | ✅ | ✅ | song URL, heading, row, stage on |
| FR-003 | ✅ | ✅ | in-place navigation, panel state, parent selection |
| FR-004 | ✅ | ✅ | edits, other kinds, spec-209 service path unchanged |
| FR-005 | ✅ | ✅ | refused create leaves state put |
| SC-001 | ✅ | ✅ | one songbook save, no second click |
| SC-002 | ✅ | ✅ | one song save, four measured values |
| SC-003 | ✅ | ✅ | marker, timeOrigin, `data-nav` |
| SC-004 | ✅ | ✅ | other paths and refusals as on base |

**Coverage**: 100% · **CRITICAL**: 0

## Applied mechanically

- Corrected tasks T013 to say the board card is at In progress until a PR number exists; the
  In review and Done moves wait for delivery.
- Restated `test_the_shell_survives_a_save` against the new contract after the implementation
  changed the stage; recorded as F3 in `converge.md`.

## Escalated

- None. The one decision this pack rests on — what "opened" means — was made at gate 1 and is
  recorded in the spec's Clarifications.

## History
- 2026-11-23 — delivery re-read: digests above, 0 CRITICAL, 100% coverage, one MED finding fixed in
  implementation; gate 2 had been accepted earlier without a separate analysis run (A3).
- 2026-11-23 — develop advanced with spec 224 before the merge; the declared patch bump was restated
  to 1.36.10 → 1.36.11, the capability/spec indexes were merged with 224, and the focused set plus
  the 224 placement tests ran green on the merged tree (12 tests).
