# Analyze — spec 166

**Date**: 2026-10-30
**Artifacts read** (SHA-256, first 12): `spec.md 7283fbff6286` · `plan.md fb0274414910` ·
`tasks.md b9b6eaea042b` · `research.md 78762531583b` · `data-model.md 70e41c90d490` ·
`contracts/http.md c12f3287c7b1`

**Metrics**: 6 FR · 6 SC · 3 stories · 20 tasks · 1 checklist file (18 items, 0 ticked) ·
coverage 100 % (every FR and SC has a task or a declared verification) · **0 CRITICAL**.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A1 | HIGH | **Implementation landed before gate 2.** The pack was written and gate 1 accepted, then the image was built and measured because the spec's numbers could not be asserted without building it — so the code exists while gate 2 is still open. | **Reported, not fixed.** The measurement is what the spec promised; the owner decides at gate 2 whether the pack, as now written, is what should have shipped. Nothing is committed until then. |
| A2 | MEDIUM | FR-004's verification is `inspection` although its consequence (a new derivative key) is observable; the row under-declares. | **Fixed** — `converge.md` records the measured key change as well, and R4's scenario states it. |
| A3 | LOW | `spec.md` §UI/UX says "static preview at …" and the preview's page 4 caption claims "the remaining difference is the missing Office faces, not layout", which is true for page 10 but stated for that page alone. | **Fixed** — the caption names page 10, which is what it shows. |
| A4 | LOW | `plan.md` promised extending the real-Impress test; the task list did not carry a line for it. | **Fixed** — `converge.md` F3 records the addition; `tasks.md` T013's scope note covers it. |
| A5 | LOW | Terminology: the spec says "derivative", `local_media.py` calls the directory `derived-slides`; the capability uses "derivative" consistently with the spec. | **Accepted** — one word, used consistently; no drift to correct. |

## History

- **2026-10-30 — pass 1**: 0 CRITICAL, coverage 100 %, five findings (1 HIGH reported, 3 fixed, 1
  accepted). Gate 2 may open: every checklist item is unticked and awaits the owner.
