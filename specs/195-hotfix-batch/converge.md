# Converge — spec 195

## Pass 1 — 2026-11-15

**Checked**: every traceability row against the working tree, by its declared method.

| Row | Finding | Type | Outcome |
| --- | --- | --- | --- |
| FR-001 (US1 badge hide) | Rule served under `@media (hover: hover)` with the exact selector set; the harness browser reports `(hover: none)` so the live reveal could not fire here. Selector semantics proven: with the row hovered (`matches(':hover')` true) and the same declarations active, the badge paints `display: none`; the shipped rule sits under the same gate as spec 190's date hide, which works in production. | `inspection` | `checked by inspection` — full reveal E2E lands at the push step (declared `test` row covers it) |
| FR-002 (US2 header) | Measured on the live edit modal: flex / space-between / gap 16px, rule 1px under, title margin 0, button 34×138 (spec: 137.8×34), flush right, one row. Confirmation flow opens and cancels as before. | `inspection` | pass |
| FR-003 (US3 picker) | Deep-link path binds at boot; sidebar-click swap path binds via `shell:page`; calendar opens on the trigger, day pick fills the field (22 November 2026). | `manual` + `test` | pass; E2E written at push |
| FR-004 (US4 id contract) | Fresh pick saves (stage shows "Bait 1, 3"); summary reads numbers from `data-number` in both renders; view/form/widget tests green (130 in `ServiceEntryViewTests`). | `test` + `manual` | pass |
| FR-005 (US4 checklist parity) | The server-rendered checklist already shares the client's styling block (`.editor__verses > div` + `.editor__verses label`): computed `inline-flex / center / 7px gap / 14px` on a server-rendered row. No CSS change was needed — plan's T06 resolves as inspection, not code. | `inspection` | pass — no change (the planned CSS task was unnecessary) |
| FR-006 (US4 preserved states) | Empty checklist refused with "Keep at least one verse in the service."; "This song has no verses" path untouched (tests). | `test` | pass |
| FR-007 (US5 fit) | Live overlay: wrapping lyric painted 29.0852px / 2.00 visual lines; short lyric untouched at the sheet's 54px / 1 line, no inline override. | `manual` | pass |
| FR-008 (US6 re-read) | Edit made by curl (outside the browser — no channel, no storage event): overlay repainted within one 10 s tick (MutationObserver caught exactly one stage change); dock's step list followed. Both surfaces guard on `document.hidden`, so a background tab does not fetch — OBS paints its sources continuously, so the guard is inactive there. | `manual` + `inspection` | pass |

**Findings requiring code**: none. **Passes**: 1. Converged.
