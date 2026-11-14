# Analysis: song verse editing on the song page

**Date**: 2026-11-09
**Artifacts read**: `spec.md` (SHA: draft Accepted 2026-11-09), `plan.md`, `research.md`, `data-model.md`, `contracts/verse.md`, `quickstart.md`, `tasks.md`, `checklists/requirements.md`
**Metrics**: FR 22 · SC 7 · stories 5 · scenarios 15 · traceability rows 32 · tasks 12 · test 22 · inspection 6 · manual 0 · CRITICAL 0 · coverage 100% (32/32 requirements have a traced component and a declared verification)

## Findings

| ID | Severity | Location | Finding | Disposition |
| --- | --- | --- | --- | --- |
| A-001 | HIGH | FR-006e / Spec edge “hold still unchanged” (B mode) | With the live-cursor + frozen-mid rule, a middle-stanza grab after collapse reads past the last verse (pointer below compact list) — hold-still **does** move it in B, contradicting the edge-case line as written for A mode | Intent — owner recorded 2026-11-09 (*current cursor*) knowing the consequence; spec Assumption records it as the cost. Left for Gate 2 owner to confirm, not silently fixed. |
| A-002 | HIGH | `spec.md` UI/UX reorder numbers | Numbers came from the static preview, not the product template (no product code yet); Gate 2 numbers are referenced, not yet product-verified | Intent — by design pre-implementation. Implementation tasks (T012) re-measure on product CSS. |
| A-003 | MEDIUM | FR-006g readout | `from→now` on the ghost cell while the row is a placeholder; the placeholder’s own `numberRows` still paints — two painters must agree | Mechanical — tasks already split number paint across `paintNumbers`; keep as is, covered by E2E drag test. |
| A-004 | MEDIUM | T004 refactor scope | `pk__in` refactor touches `views.py` stage sites beyond current grep (`2251`, `1649`, `1586`, `1246`); plan names files not line numbers | Mechanical — implementer verifies with `rg -n "number__in"` before merging. |
| A-005 | LOW | Plan step weights | Effort on card is L (large) for 12 tasks — consistent; no split needed by story/capability | No action. |

## History

- 2026-11-09 — first Run: 0 CRITICAL, 100% coverage; mechanical leftovers A-003/A-004 handed to Implement as written; intent A-001/A-002 left for Gate 2 owner decision (recommendation: accept as written).

## Gate 2 readiness

Zero CRITICAL, coverage complete. Intent items A-001/002 are the Gate 2 owner's to confirm (recommendation: accept — consequence already recorded in spec Assumption; numbers will be re-measured in Polish).
