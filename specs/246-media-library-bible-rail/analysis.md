# Analysis — spec 246

**Date**: 2026-11-27
**Stage**: Analyze (gate 2 pending)
**Metrics**: 9 test · 5 inspection · 4 manual · 18/18 traceability rows covered · 1 production file changed · 2 new E2E tests · 0 unknowns · 0 CRITICAL · 0 HIGH

## Artifact SHAs (SHA-256, first 12 hex)

| Artifact | SHA |
| --- | --- |
| `spec.md` | `795c092fab0a` |
| `plan.md` | `13a4339215af` |
| `research.md` | `2140adc4cad7` |
| `data-model.md` | `f34e6c7ee587` |
| `contracts/none.md` | `591096560687` |
| `quickstart.md` | `bcaaaf460899` |
| `checklists/requirements.md` | `a9b765389b18` |
| `tasks.md` | `f1f1c5535a41` |
| `preview/probe.py` | `1a4d35d323d2` |
| `preview/manual_probes.py` | `5c2280df1017` |
| `tests/e2e/test_media_library_bible_rail.py` | `e6c258b31c37` |
| `multimedia/web/reading/views.py` | `b14fa6dbf480` |

## Findings

| ID | Level | Finding | Disposition |
| --- | --- | --- | --- |
| AN-01 | MEDIUM | Base and preview sidebar row counts differ (66 vs 2) because each surface has its own dataset. | Accepted: the claim is the request count and the hidden empty state; the spec states why the absolute counts differ. No action. |
| AN-02 | LOW | The new E2E waits a fixed 500ms before reading state. | Accepted: the assertion reads the request list and DOM after the click, not a timeout on a node; the local server is deterministic. No action. |
| AN-03 | MEDIUM | Own-tile toggle, cross-section switch and direct load are probe-recorded, not committed tests. | Accepted: declared `manual`/`inspection` in the plan and evidenced by `preview/manual_probes.py`. No action. |
| AN-04 | LOW | The eight reviewer checklist items remain unticked. | Owner decides at gate 2; the agent never ticks reviewer-owned items. No action. |
| AN-05 | INFO | No `CONSTITUTION.md` at the repo root. | Constitution check skipped per SDD-01. No action. |

Zero CRITICAL and zero HIGH findings. Coverage reads Plan's traceability table: all 18 rows carry
a method, a component and named evidence. No orphan requirement, entity or interface remains.

## History

- 2026-11-27 · Plan/Tasks/Analyze · 0 CRITICAL, 18/18 rows covered, five findings recorded with dispositions.
- 2026-11-27 · Fold · tasks T009–T014 closed out; the SHAs above are the artifacts as read at Analyze.
