# Convergence — A text entry's form is the media modal's large frame

## Pass 1 — 2026-10-25

**What was checked**: every row of `plan.md`'s traceability table, each by the method it declares. The
suite was run first (`multimedia.web` + `tests.test_design_tokens`, 340 tests), then the browser module
this slice adds (4 tests), then the two modules it claims to leave alone (16 tests), then each
`inspection` row by reading the running branch's measured values from `preview/probe_modal_frame.py`.

| Requirement | Method | Evidence | Outcome |
| --- | --- | --- | --- |
| FR-001 the box | test | `multimedia.web.tests.ServiceEntryViewTests::test_the_large_frame_is_marked_for_both_text_forms` (green; red before the template change with `Couldn't find 'data-editor-size="large"'`); `tests.e2e.test_entry_modal_frame::test_new_text_dialog_matches_new_media` (green; red on the old CSS with `AssertionError: 480 != 840`) | met |
| FR-002 the chrome | inspection | probe at 1440×900: text and media both `titleStyle.padding='20px 26px'`, `font-size=21px`, `border-bottom=1px`, `content padding=0px`, `fields[0]` at `x=326 w=788`, `actionsStyle.margin='14px 26px 20px'`, `border-top=0px` | met |
| FR-003 the Text box fills | test | `::test_text_box_fills_the_frame` — textarea bottom + 14 == action row y, height 419 (create) and 507 (edit) | met |
| FR-004 the other forms | test | `…::test_the_large_frame_is_not_marked_for_the_other_forms` — new passage, new song, edit passage and edit media carry no `data-editor-size`; media create does; `data-editor-grow` only on text | met |
| FR-005 the 650px breakpoint | test | `::test_narrow_window_uses_the_small_gutters` — 352×760, `titlePadding='16px 18px'`, first field 18px from the dialog's edge | met |
| FR-006 behaviour unchanged | test | `tests.e2e.test_unified_text_screen_mode` (2) + `tests.e2e.test_entries` (14) re-run unmodified: 16 green. `git diff` touches neither `entries.js` nor `editor.js` | met |
| FR-007 placed against the window | test | `::test_dialog_is_centred_on_a_scrolled_page` — page scrolled to the bottom, dialog y == (900 − 760) / 2 = 70, top ≥ 0, bottom ≤ 900 | met |
| SC-001 the two dialogs match | test | six values compared between `+ Text` and `+ Media` in `test_new_text_dialog_matches_new_media`; all equal | met |
| SC-002 never clips, never scrolls | inspection | probe rows: 1440×900 → 840×760 at (300, 70); 1280×800 → (220, 20); 1280×600 → 840×568 at (220, 16); 390×844 → 352×760 at (19, 42); `scrolls: false` in every state it opens | met |
| SC-003 centred at any scroll | test | FR-007's test, at scrollY 556; the probe's edit row at scrollY 0 gives the same y=70 | met |
| SC-004 no other form changes | inspection | probe: passage form 480×422.8 centred at y=238.6 with the stage scrolled 400px; media create still 840×760 at (300, 70) | met |
| US1/AC1, AC3–AC5 | test | the four rows above; AC4/AC5 are the unchanged modules | met |
| US2/AC1–AC3 | test | marker present on the edit path (unit test), 507px Text box (E2E), other forms unmarked (unit test) | met |
| US3/AC1–AC3 | test + inspection | AC1 by the E2E; AC2 by inspection — the date popover opens 8px under its trigger (504.3 against a 496.25 trigger bottom) and inside the window; AC3 by the passage form's y=238.6 | met |

**Typed gaps**

- `missing` — none.
- `partial` — none.
- `contradicts` — none. One code-versus-intent question was settled before this pass and is recorded in
  `research.md` D004: the dialog's `position: relative` was wrong for a 760px frame, and the spec
  (US3/FR-007) says so.
- `unrequested` — none. The `position: fixed` change is not extra work: US2 cannot be satisfied without
  it, because an entry's Edit always sits below the fold.

**Outcome**: converged on pass 1. No open task, no requirement resting on nothing.

## Push-step evidence — the browser suites

| Suite | Result |
| --- | --- |
| `tests.e2e.test_entry_modal_frame` (4 tests, new) | green — box parity, Text box fill, narrow gutters, scrolled placement |
| `tests.e2e.test_unified_text_screen_mode` (2) + `tests.e2e.test_entries` (14) | green, unmodified — the switch, the help line, the hidden `default_screen_mode` field and the Save guard |
| `multimedia.web` + `tests.test_design_tokens` (340) | green |

The repository's full matrix (all ten browser modules) is the CI step that follows the push, not a local
run; this slice ran the modules its own rows name, plus the two it claims to leave untouched.
