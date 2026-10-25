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

## Push-step evidence — the full matrix

This repository has **no CI**: the GitHub Actions workflow was removed on 2026-10-24 in #371 ("chore(ci):
remove the GitHub Actions pipeline"), leaving only the E2E-tag invariant for the local fast lane. The full
matrix is therefore a **manual** run before the merge, and it was run in full:

| Run | Result |
| --- | --- |
| `manage.py test` (everything, all ten browser modules) | **912 tests in 1895s — 4 failures, 3 errors** |
| `multimedia` (every app) + `tests.test_design_tokens` | 419 green |
| `tests.e2e.test_entry_modal_frame` (new) | 4 green |
| `tests.e2e.test_unified_text_screen_mode` + `tests.e2e.test_entries` | 16 green, unmodified |

**None of the seven reds belongs to this slice, and each was proved on the target branch.** The same
seven test ids were run in a checkout of `develop` `ffa5c340` under the same environment, command,
database and browser: **identical 4 failures and 3 errors**, same assertions. They are pre-existing on
the base this slice was cut from, so they are carded rather than folded into this pack:

| Test | What it does | Card |
| --- | --- | --- |
| `test_offline_library…::test_saved_content_and_projector_survive_disconnection`, `test_pdf_display…::test_saved_projector_renders_pdf_while_django_is_offline`, `test_powerpoint_display…::test_saved_projector_renders_slides_while_django_is_offline` | `Page.goto: net::ERR_INTERNET_DISCONNECTED` — Playwright's offline emulation blocks loopback, so the projector never loads | `ITEM-139` |
| `test_audio_display…::test_untitled_preview_and_projector_idle_display_off`, `test_video_display…::test_navigation_and_display_off_stop_and_reset_video` | the projector's `<body>` keeps `data-showing="true"` after display-off | `ITEM-140` |
| `test_reading…::test_bible_edition_preference_returns_after_unavailable_chapter` | `Garam ni dunia.` is absent after the unavailable chapter — the preference or the seed moved | `ITEM-141` |
| `test_reading…::test_the_panel_shows_its_empty_view_when_no_songbook_exists` | expects `No matching songbooks.` where spec 129 requires the empty copy | already `ITEM-137` |

A red suite nobody owns is the one the next session inherits, so the four cards carry the evidence and the
`develop` reproduction in their Notes.
