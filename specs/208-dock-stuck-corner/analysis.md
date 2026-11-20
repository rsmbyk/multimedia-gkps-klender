# Analyze: the live entry header's corners follow its pin state

**Date**: 2026-11-20
**Artifacts read**: `spec.md` (Accepted), `plan.md`, `tasks.md`,
`checklists/requirements.md`, `fold.md`, `preview/README.md`
**Metrics**: 11 FR · 13 SC · 13 acceptance/edge scenarios · 13 tasks · 14 checklist items ·
coverage 24/24 requirement-and-scenario items, 12 traceability rows · 0 CRITICAL · 1 HIGH ·
2 MEDIUM · 2 LOW

## Findings

| ID | Severity | Dimension | Finding | Disposition |
| --- | --- | --- | --- | --- |
| F1 | HIGH | Verification | SC-007 rests on four dock suites outside the edited file; the board carries ITEM-220, a machine-local chevron settle-wait race that fails on the unmodified base. | **Accepted, guarded** — the 67-test regression was run on the slice; the single intermittent error was attributed to base and recorded as ITEM-220, never folded into this slice. |
| F2 | MEDIUM | Consistency | The bundle trigger was revised several times during live review (edge, fully-off, row early, band top); the spec's Revision keeps every ruling with its supersession. | **Fixed** — the active FR/SC text states only the band-top boundary; superseded rulings stay visible as history, not as competing requirements. |
| F3 | MEDIUM | Completeness | The bottom pin cannot be the header node itself: a sticky first child has no room to pin upward. | **Accepted, recorded** — the list-level clone is the mechanism (Assumptions, R18); the capability speaks of the visual state, not the node. |
| F4 | LOW | Ambiguity | "Always visible" for the Next band could be read as showing with no next entry. | **Recorded assumption** — the band is tied to the existence of a next entry; it is always shown while one exists, on screen or not. |
| F5 | LOW | Traceability | FR-006 is an unchanged-behaviour requirement verified by diff, not by a dedicated test. | **Accepted** — inspection is the right verification for an unchanged rule; the diff is named in the plan's traceability row. |

## History

- 2026-11-20 — first analysis; zero CRITICAL, 24/24 covered, one HIGH reported with its guard.
