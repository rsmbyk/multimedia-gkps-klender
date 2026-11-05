# Converge — pass 1

**Spec**: `specs/187-keyboard-parity/spec.md` (17 FRs · 14 SCs · 13 stories)
**Plan's traceability**: `specs/187-keyboard-parity/plan.md`
**Run**: 2026-11-05 · `tests.e2e.test_dock_keys`, `test_projector_keys`, `test_goto_shared_state`,
`test_dock_goto`, `test_obs_dock`, `test_display_session`, `test_image_display` — **79 tests, all
green**, one run, `--keepdb` against the throwaway `gkps187` database.

## What was checked

Every row of the traceability table by the method it declared: 29 `test` rows through the seven
modules above, 2 `inspection` rows by reading the code and the markup (named below). Nothing was
checked by memory.

| Requirement | Method | Evidence |
| --- | --- | --- |
| FR-001 | test | `test_a_tap_of_escape_moves_nothing_and_a_hold_returns_to_the_picker`, `test_escape_closes_the_sheet_and_the_band_on_the_tap` |
| FR-002 | test | `test_g_opens_the_band_on_the_picker`; the head's find control shares `openFind` with the `G` key — checked by inspection (`obs-dock.js` `findBtn.addEventListener`) |
| FR-003 | test | `test_the_picker_go_to_stands_alone_and_back_returns_to_the_picker`, `test_a_picker_go_to_stands_alone_and_paints_on_both_surfaces` |
| FR-004 | test | `test_the_picker_go_to_stands_alone_and_back_returns_to_the_picker`, `test_the_runner_band_still_adopts_the_browsed_service` |
| FR-005 | test | `test_the_go_to_steps_a_verse_a_chapter_and_a_book` |
| FR-006 | test | `test_the_picker_moves_on_up_and_down_only` |
| FR-007 | test | `test_the_sheet_is_a_layer_and_closes_on_its_frame`, `test_k_opens_the_sheet_and_the_picker_group_rides_with_the_view`; the close control calls the same `setKeysOpen(false)` — checked by inspection |
| FR-008 | test | `test_k_opens_the_sheet_and_the_picker_group_rides_with_the_view` (groups, row counts, the picker group's rise and fall, the dock-only labels); the verbatim projector wording and per-group order are also pinned by `preview/probe.py` |
| FR-009 | test | `test_no_key_changes_what_is_on_air_while_a_go_to_fetches` |
| FR-010 | test | `test_meta_and_control_take_the_same_step`, `test_meta_with_a_letter_leaves_the_browser_its_shortcut` |
| FR-011 | test | `test_a_picker_go_to_stands_alone_and_paints_on_both_surfaces` |
| FR-012 | test | `test_home_and_end_act_on_the_bait_or_entry`, `test_shift_home_does_nothing_on_a_text_entry` — **see finding C1** |
| FR-013 | test | `test_the_sheet_carries_one_display_group_and_one_find_group` |
| FR-014 | test | `test_audio_and_video_are_one_group_in_the_left_column`, `test_the_passage_group_merges_verses_chapters_and_books`, `test_the_sheet_measures_its_tallest_column_and_scrolls_at_720` |
| FR-015 | test | `test_the_band_keeps_the_keyboard_when_the_window_returns` |
| FR-016 | test | `test_a_refresh_opens_the_service_on_air`, `test_a_refresh_with_nothing_on_air_keeps_the_picker`, `test_a_refresh_brings_back_a_go_to_that_stands_alone` |
| FR-017 | test | `test_a_narrow_window_draws_one_scrolling_column`, `test_the_corner_cue_stays_out_of_the_sheet` |
| SC-001 … SC-014 | test | as the plan's rows name; each of the fourteen ran green in the run above |

## Findings

### C1 — `contradicts` · FR-012's parity sentence against the projector's own code (spec at fault)

FR-012 says two things that cannot both be true:

1. "`Shift+Home`/`End` SHALL take the live entry's first or last bait and **move nothing on an entry
   with none**" — and US8/AC3 and SC-010 pin that: on a text entry the chord moves 0 rows.
2. "The arithmetic SHALL be the projector's own `unitBoundary`, so the two surfaces land on the same
   screen for the same chord."

The projector's `unitBoundary` does not move nothing. For an entry that is not a song it falls
through the song branch and runs `moveTo(last ? Math.max(entry.start, entry.end - (blank ? 1 : 0))
: entry.start)` (`projector.js`, `unitBoundary`), so `Shift+Home` takes the entry's first screen and
`Shift+End` its last. The dock implements clause 1, so this one chord is the only place the two
surfaces disagree — by construction, not by accident.

Root cause: the spec, not the code. The build follows the clause the owner accepted and the tests
pin; the parity sentence is the part that cannot be met while that clause stands.

**Consequence under the grammar**: a spec-at-fault contradiction reopens the slice at Specify for
this requirement. The alternative the grammar also allows is to record it as an accepted gap and
fold the rest. The owner was asked; the answer is recorded below.

## The owner's answer to C1

**Match the projector.** On a text entry, `Shift+Home`/`End` takes that entry's first or last screen
(a blank trailing rest skipped) — the projector's own fall-through. FR-012, US8/AC3 and SC-010 were
reworded to say so, and the dock's `unitBoundary` lost the early return that held the chord still.

## Pass 2 — after the answer

- `static/web/obs-dock.js` — `unitBoundary` now falls through from the song branch to the text entry's
  ends, the identical expression the projector runs.
- `tests/e2e/test_dock_keys.py` — `test_shift_home_does_nothing_on_a_text_entry` became
  `test_shift_home_and_end_take_a_text_entrys_ends`, which reads the entry's own screens from the DOM
  (including whether the last is a rest) and asserts the same screen the projector's arithmetic gives.
- `spec.md` — FR-012, US8/AC3, SC-010 reworded; the Clarifications session records the decision.
- Verified: `tests.e2e.test_dock_keys` — 16 tests, green; the seven-module run repeated for Fold's
  green tree.

## Outcome

**Converged.** 17 FRs · 14 SCs checked; 0 `missing`, 0 `partial`, 1 `contradicts` (C1) resolved by
reopening the one affected clause at the owner's word and building the projector's behaviour;
0 `unrequested`. One pass found it, one pass closed it.
