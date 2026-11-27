# Analysis: Back clears the Go To from the cue over an empty stage

**Date**: 2026-11-23

## Artifacts read

| Artifact | SHA-256 |
| --- | --- |
| `specs/228-goto-cue-back-reset/spec.md` | `04cfa00df29d8667703cc8d6beee4cbb8016a13324b15231a0103cb8e9902825` |
| `specs/228-goto-cue-back-reset/plan.md` | `32dffcf576dce7b6eaa790363dd28e7e6715f012500c895d9440befde032ae3d` |
| `specs/228-goto-cue-back-reset/tasks.md` | `14170bbee038c3e146f93ccd3b9d9a1635847e656a7b783cba5d8759d55e9464` |

**Metrics**: 9 FR · 5 SC · 10 scenarios · 24 traceability rows · 11 tasks · 13 checklist items ·
0 CRITICAL · 0 HIGH · 0 MEDIUM · 1 LOW · verification split 16 test · 4 inspection · 0 manual.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A1 | LOW | `US1/AC4` (never-opened cue) is checked by inspection rather than a new E2E. | Accepted — the empty branch is the same code at first render and after Back; a fourth case would repeat the same read-back. |
| A2 | LOW | The dock-Back case covers a passage; a dock-Back song case is not pinned. | Accepted — the branch that clears baits is exercised by the projector-Back song case, and the dock path is state-identical. |
| A3 | LOW | `#cue-progress` is cleared but not asserted in the E2E readback. | Accepted — the live probe records the whole cue text, where the progress had appeared; it reads only `·` after Back. |
| A4 | LOW | `test_quiet_controls_support_keyboard_and_mouse_jumps` fails in the loaded 39-test lane on both the slice and unmodified develop. | Accepted — identical assertion on develop at 33 tests, passes alone on the slice; pre-existing load sensitivity, not caused by these changes. |

## History

- 2026-11-23 — first pass: 0 CRITICAL, full coverage, 3 LOW accepted; no mechanical fixes applied.
- 2026-11-23 — revision pass (owner finding, unpushed slice): 1 additional LOW (loaded-lane flake),
  spec/plan/tasks re-hashed, fold and pack amended; no mechanical fixes applied.
- 2026-11-23 — second revision (owner finding, unpushed slice): `.cue-next[hidden]` display rule,
  FR-002 clarified to require actual non-display, spec/plan/tasks re-hashed and all three passes
  re-read; no new finding.
