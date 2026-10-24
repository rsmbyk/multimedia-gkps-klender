# Tasks: Keep a chapter's verse text when the reading page updates in place

**Spec**: `specs/124-bible-edition-block-identity/spec.md`
**Plan**: `specs/124-bible-edition-block-identity/plan.md`
**Verification split**: 9 test · 1 inspection · 0 manual

## Phase 1 — Setup

- [ ] T001 [P] [US1] Add `test_same_name_edition_blocks_keep_the_verse_text` to
      `tests/e2e/test_reading.py` (`ReadingE2ETests`), with a fixture that creates a book whose TB and SIM
      translations share the name `Rut` and two chapters with verses in both. The test opens Matius 5 through
      the sidebar, then opens Rut 1 in place: expects two `#readBody .read__ed` blocks (TB visible, SIM
      hidden), the Rut verse text visible, and the URL at `/bible/<pk>/1/`; then opens chapter 2 and expects
      its text with both blocks still mounted; then selects SIM and TB and expects each translation's own
      text. Red against today's collapse. *(FR-001–FR-003, SC-001, SC-002, US1/AC1–AC3)*

## Phase 2 — Foundational

- [ ] T002 `n/a — nothing is shared beyond Phase 1's pin.`

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: a chapter of a same-name book reads normally after any in-place move.
**Independent test**: T001 alone.

- [ ] T003 [US1] In `static/web/reading.js`, rank `data-ed` above `data-name` in `nodeIdentity`'s attribute
      list, with a comment naming the shared-label case. No other key changes: `data-ed` occurs only on
      `#readBody .read__ed` (server template `bible.html` and `static/web/offline-render.js`).
      *(FR-001–FR-003)*
- [ ] T004 [US1] Re-run T001 green; confirm the chapter-move and switch legs. *(SC-001, SC-002)*

## Phase 4 — US2 (P2)

**Goal**: books whose names differ, direct loads, and the saved copy behave exactly as before.
**Independent test**: the existing edition and navigation classes, re-run unchanged.

- [ ] T005 [US2] Re-run `test_shell_navigates_in_place`,
      `test_bible_sidebar_labels_follow_edition_and_reset_on_refresh`,
      `test_sim_codes_titles_labels_and_fallback_follow_selected_edition`,
      `test_bible_edition_survives_menu_switches_and_history`,
      `test_the_translation_switch_fills_the_hovered_option`, `tests.e2e.test_targeted_reading_updates`,
      `tests.e2e.test_navigation_freshness` — all green. *(FR-004, SC-003, US2/AC1–AC2)*
- [ ] T006 [US2] Inspect `static/web/offline-render.js` `edition()`: it emits `data-ed`, so no edit is
      expected; re-run `tests.e2e.test_saved_render_parity` as its guard. *(FR-004, US2/AC3)*

## Phase 5 — Polish

- [ ] T007 Write `backlog/items/ITEM-125-bible-edition-block-identity.md` and its `backlog/board.md` row.
- [ ] T008 Bump `VERSION` with a patch and add the changelog entry (take develop's current number at merge
      time; the neighbouring slice bumps the same level).
- [ ] T009 Tick this list, fill `analysis.md`'s dispositions, open the draft PR with the repository's body
      template, and link the spec.

## Phase N+1 — Convergence

<!-- written by Converge only; absent until it runs -->
