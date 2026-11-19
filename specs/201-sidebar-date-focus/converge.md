# Convergence: a clicked service keeps its date

**Spec**: `specs/201-sidebar-date-focus/spec.md`
**Passes**: 1 of 3

## Pass 1 — 2026-11-19

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| — | — | — | no gaps found |

Each traceability row was checked by the method it declared:

| Requirement | Method | Checked result |
| --- | --- | --- |
| FR-001 | `test` | `test_a_clicked_row_paints_its_date_again`, `test_keyboard_focus_on_an_action_hides_the_date_until_it_leaves`, `test_the_shipped_rule_uses_the_action_reveal_not_focus_within` — green; the first two were red on base `92edc752` for the reported reason |
| FR-002 | `test` | `test_the_today_badge_follows_the_date_reveal` — green, red on base |
| FR-003 | `inspection` — checked by inspection | diff of `components.css`: `@media (hover: hover)` guard kept; `hover: none` / touch rules at lines 3234-3248 untouched; no template change |
| FR-004 | `inspection` — checked by inspection | `_tatib_panel.html:8-10` untouched; `aria-label` asserted equal across rest/clicked/hover in `test_the_row_box_and_label_do_not_change_across_the_states` |
| SC-001 | `test` | computed `display: block` with `li:focus-within` true in `test_a_clicked_row_paints_its_date_again` |
| SC-002 | `test` | hover and pencil/trash `:focus-visible` give `none`; blur gives `block` |
| SC-003 | `test` | row box height and accessible label identical in rest, clicked and hover |
| US1/AC5 | `test` | focus on the row's link keeps the date painted |
| US2/Edge 3 | `test` | 390px touch context: controls at opacity 1, date not hidden |
| US1/AC3 | `manual` — checked by inspection | preview's *Click row (pointer away)* state: today `none`, proposal `block` (`preview/probe.py` assertions) |

**Outcome**: Converged — no task was appended; no accepted gaps.

## Pass 2 — 2026-11-19

A regression pass ran `tests.e2e.test_reading` and `tests.e2e.test_drawer_shell` beside the focused
module: 118 tests, one failure — `test_the_panel_shows_its_empty_view_when_no_songbook_exists`
expected `No matching songbooks.` and got `No songbooks yet. Add a songbook to start collecting
songs.`. The same test was run on unmodified `develop` (main checkout, local `16a7da8a`) and failed
identically — pre-existing, unrelated to this slice, and not fixed here. The preview probe still
passes after the CSS edit (its frozen base sheets keep today's column unchanged); the live
worktree server at `127.0.0.1:8871` serves the new selector.

**Outcome**: Converged — nothing remains from this slice; the one red is an accepted base failure.

## Accepted gaps

<!-- none -->

## Cap reached

<!-- not reached -->
