# Convergence: song-row focus ring is clipped at the list top

**Date**: 2026-11-22 · **Pass**: 1 · **Spec**: `specs/223-songrow-focus-ring-clip/spec.md`

## Phase 1: Convergence

Every traceability row was re-assessed against the present code by the method it declared. The
product diff is one declaration: `.ch__body` padding `0 0 8px` → `3px 0 8px` in
`static/styles/design/components.css:1669`.

| Requirement / scenario | Method | Result | Evidence |
| --- | --- | --- | --- |
| FR-001 full ring inside scrollport | test | pass | `test_the_first_rows_ring_fits_inside_the_scrollport`: gap 3px ≥ 2px needed; red before at 0px |
| FR-002 row box / pitch / fills unchanged | test | pass | `test_focus_does_not_change_the_row_box_or_its_states`; preview heights 38 / 57.5px, pitch 1px |
| FR-003 unfocused outline none | test | pass | the same case reads `outlineStyle === 'none'` before focus |
| FR-004 themes and viewports, last row | manual | pass with state caveat | 1440×900, 900×700, 390×844 in dark and light: gap 3px, `padding-bottom: 8px`; at 390×844 the drawer starts closed, so the list must be opened before a row can be focused — correction recorded below |
| FR-005 other surfaces unchanged | inspection + test | pass with accepted red | the diff contains no other product file; `tests.e2e.test_reading` 94/95 green — the one failure is the empty-view copy, identical on unmodified develop and already on the board as ITEM-137 |
| FR-006 candidate A only | inspection | pass | no `:focus-visible` declaration, no colour token, no selector change in the diff |
| US1 AC1 Tab focus | test | pass | `test_a_tabbed_first_row_gets_the_same_complete_ring` green after the fix, red before it |
| US1 AC2 key after pointer focus | test | pass | first case, pointer click then `a` |
| US1 AC3 unfocused / hover / selected | test | pass | third case compares `aria-current` title and background before/after |
| US1 AC4 bottom row | manual | pass | list scrolled to bottom, last row inside the 8px bottom padding |
| US1 AC5 themes and viewports | manual | pass with the same caveat | the four measurements above |
| US1 AC6 other surfaces | inspection + test | pass with accepted red | as FR-005 |
| Edge: not a scroll defect | test | pass | `scrollTop = 0`, `scrollHeight === clientHeight` before focus |
| Edge: three-line row | manual | pass | preview's three-line row keeps its 57.5px box; no clamp change in the diff |
| Edge: side padding sufficient | inspection | pass | `.ch__body ul` `padding: 0 10px` unchanged |
| SC-001 complete ring | test + manual | pass | geometry assertion green; visible-ring control: unfixed page loses the top band at y<130, fixed page paints it at y=130 |
| SC-002 not scrolled | test | pass | first case's preconditions |
| SC-003 geometry unchanged | test | pass | third case |
| SC-004 both focus paths | test | pass | first two cases |
| SC-005 no ring unfocused | test | pass | third case |

**Outcome**: converged, with one accepted red outside this slice's surface and one mechanical
clarification to the accepted spec.

## Findings and disposition

1. **Pre-existing regression, accepted.** `test_the_panel_shows_its_empty_view_when_no_songbook_exists`
   asserts `No matching songbooks.` and the page renders `No songbooks yet. Add a songbook to
   start collecting songs.`. The identical failure was reproduced on the clean `develop` checkout
   at `8bf20f69` with the same command and a separate database; `tests/e2e/test_reading.py` is
   unchanged between that commit and this branch's re-based base `e8e79dbb`. It is already represented by
   ITEM-137 on the board. Recasting the copy here would be unrequested work.
2. **Spec at fault, mechanically corrected.** FR-004, US1 AC5 and the preview's state list spoke of
   390×844 without saying the songs list is a drawer that starts closed. At that width `#chBody`
   is off-screen (`x = -379`) and no row is reachable by Tab until the drawer opens. The accepted
   spec now says "with the songs list open"; no behaviour changed, so Specify was not re-entered.
3. **Dark-theme UA ring, note.** In dark mode the browser's `auto 1px rgb(16,16,16)` outline paints
   so close to the canvas that a pixel diff cannot see it. The visible-ring control (3px red at a
   2px offset) isolates the geometry: before the fix its top band falls outside the scrollport,
   after it the band is drawn at y=130. The test asserts the clearance relationship, not a colour.
4. **Skipped Clarify, carried from analysis F1.** Candidate A was accepted at gate 1 as the recorded
   assumption; B remains a preview comparison. No further action.

**Verification run record**: red 2/3 failures with the exact assertion `the ring needs 2px above the
row, but only 0px is available`; green 3/3 OK; regression 95 cases with the single pre-existing
failure above. No full browser matrix was run; it is deferred to the push step as requested.

**After the base move** (slice 221 merged as `e8e79dbb`, `VERSION` 1.36.8): the branch was
fast-forwarded, the capability header conflict resolved, and the preview rebuilt from the new live
page. Re-run on the re-based tree: `tests.e2e.test_songrow_focus_ring` 3/3 OK in 6.311s and
`tests.e2e.test_deleted_stage` 7/7 OK in 21.312s. Live page at `:8767` still measures row top 133px
against host top 130px with the unchanged UA outline; the board and spec index each carry one
ITEM-238 / 223 row.
