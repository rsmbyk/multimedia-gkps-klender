# Analysis: A Go To still names itself with no service under it

**Date**: 2026-11-23

## Artifacts read

| Artifact | SHA-256 |
| --- | --- |
| `specs/227-goto-cue-empty-service/spec.md` | `2d3f545c2c4ac52bb6489f2a4d71a088c3a7746ee01bc570b90ff1bf54dde7db` |
| `specs/227-goto-cue-empty-service/plan.md` | `38a3a6edc005a1101591f44359bf7473d5505b30b25cbf7f3dc7682d17e126fa` |
| `specs/227-goto-cue-empty-service/tasks.md` | `aa8496f1aa9886a31cb7d820d9b92a57ff99e9a669c034e37c6e16d6bbb501ed` |

**Metrics**: 5 FR · 3 SC · 6 scenarios · 13 traceability rows · 5 tasks · 8 checklist items ·
0 CRITICAL · 0 HIGH · 0 MEDIUM · 0 LOW · verification split 10 test · 3 inspection · 0 manual.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A1 | LOW | `FR-004`'s notice return is checked by inspection and an existing test, not by a new case. | Accepted — the picker test already asserts the idle return; a second pin would duplicate it. |
| A2 | LOW | The probe's Back box reports x=502.9 outside the cue box at 420px because `.cue-next` is placed by its own CSS. | Accepted — the box is the rendered control, not a cue child that needs relayout. |
| A3 | LOW | `FR-005` is an inspection row; the "no new message" claim rests on the diff. | Accepted — the diff is one guard and two tests, so no interface can have moved. |

## History

- 2026-11-23 — first pass: 0 CRITICAL, full coverage, 3 LOW accepted; no mechanical fixes applied.
