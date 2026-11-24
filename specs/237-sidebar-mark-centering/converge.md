# Convergence: sidebar mark centring

**Spec**: `specs/237-sidebar-mark-centering/spec.md`
**Plan**: `specs/237-sidebar-mark-centering/plan.md`
**Tasks**: `specs/237-sidebar-mark-centering/tasks.md`

## Pass 1: 2026-11-24

Checked every traceability row by the method it declared. Test evidence: the new
`tests/e2e/test_sidebar_mark_centring.py` ran red on the base rule at −4px (one-line),
−22px (wrapped song) and 13px (slot badge), then 4/4 green after restoring the edit;
`tests.e2e.test_sidebar_kind_marks` ran 12/12 green. A throwaway database (`gkps237`)
isolated both runs from other sessions.

| Requirement | Method | Evidence | Result |
| --- | --- | --- | --- |
| US1/AC1 | test | `test_mark_centre_matches_number_on_every_row` — all 12 live rows and every fixture marked row at centre 0px | met |
| US1/AC2 | inspection | live page: mark colour `rgb(100,99,87)` light / `rgb(156,154,145)` dark; no new colour or motion rule in the diff | met |
| US2/AC1 | test | `test_columns_heights_and_clamp_are_unchanged` — x 42/66px, 16px mark, 38/53px rows, ≤3 lines | met |
| US2/AC2 | test | `test_wrapped_song_row_keeps_centred_mark` — 390px, 74px row, centre 0px, clamp intact | met |
| US3/AC1 | test | `test_slot_badge_follows_the_mark` — badge bottom 9px, x 50px | met |
| US3/AC2 | inspection | `reorder.js:268` stamps the ghost from the row's `innerHTML`; a DOM clone with `.reorder__ghost` reads `align-self: center` on both mark and number | met |
| FR-001 | test | `test_mark_centre_matches_number_on_every_row` | met |
| FR-002 | test | `test_columns_heights_and_clamp_are_unchanged` | met |
| FR-003 | inspection | `.reorder__ghost .songrow__mark` selector beside the number's; ghost clone readout `center` | met |
| FR-004 | inspection | CSS diff is two selectors only; `/songs/` renders 0 `.songrow__mark`; `test_dock_and_projector_keep_their_own_rows` passes | met |
| SC-001 | test | red at −4/−11.5/−22px; green at 0px | met |
| SC-002 | test | geometry and badge tests pass with unchanged x/heights | met |
| SC-003 | inspection | ghost mark and number both compute `align-self: center` | met |
| SC-004 | inspection | probe readouts at 1440/1024/390px in both themes: centre 0px, x 42/66px, badge 13 → 9px | met |

**Outcome: Converged** — 0 gaps (missing / partial / contradicts / unrequested) on pass 1.
No task was re-opened. T014 (version, changelog, card close) remains a delivery step and
is deliberately not checked here.
