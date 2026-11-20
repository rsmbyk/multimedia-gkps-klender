# Analyze: A whisper of a tint on an open entry header

**Date**: 2026-11-19
**Artifacts read**: `spec.md` (Gate 1, 2026-11-19), `plan.md` (traceability), `tasks.md`,  
`checklists/requirements.md`, `research.md`, `data-model.md`, `contracts/none.md`,  
`quickstart.md`, `preview/index.html`
**Metrics**: 8 FR · 5 SC · 7 acceptance scenarios · 11 tasks · 17 checklist items · coverage 20/20  
requirement‑and‑scenario items, 19 traceability rows · 0 CRITICAL · 1 HIGH · 2 MEDIUM · 2 LOW

## Findings

| ID | Severity | Dimension | Finding | Disposition |
| --- | --- | --- | --- | --- |
| F1 | HIGH | Verification | SC‑004 ("no other dock state changes") is verified by four suites outside the file this slice edits, and the board carries known‑red dock/preview tests (`ITEM-184`, `ITEM-185`) whose failures are not this slice's. A red there must be attributed before it is read as a regression. | **Accepted, guarded** — T008 names the four suites; the closing report states any red with its board card. |
| F2 | MEDIUM | Consistency | The spec's Intent said the wash is "exactly half" the hover face. That is exact in light (8 % ink, an 8‑level wash against a 16‑level face) but not in dark, where the face is 9 % white (a 20‑level step) against the wash's 8–9. | **Fixed** — the Intent now states each theme's ratio; SC‑005 measures both rather than asserting one. |
| F3 | MEDIUM | Completeness | The gate‑1 preview lifts the percentage into `--open-rail` so four panes can share one rule. The artifact therefore is not the shipped line byte for byte. | **Accepted, paid back by T011** — the task re‑reads the preview against the shipped rule and requires the expressions to match apart from the lifted percentage. |
| F4 | LOW | Ambiguity | The spec never says what happens under `forced-colors`. | **Recorded assumption** — the dock does not opt into forced colours today, so no fallback is owed; named in the spec's Assumptions. |
| F5 | LOW | Traceability | The plan groups US2's three scenarios into one row, so the row count (19) is below the item count (20). | **Accepted** — all three scenarios are named in the row's text, and each maps to the same assertion block. |

## History

- 2026-11-19 — first analysis; zero CRITICAL, 20/20 covered, one HIGH reported with its guard.