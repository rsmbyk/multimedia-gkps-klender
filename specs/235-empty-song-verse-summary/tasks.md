# Tasks: An empty song names itself in the Verses section

**Goal**: the Verses section names a picked song with no live verses, collapsed to its summary row.
**Independent test**: Add Song → pick the empty song → `Verses` + a small panel reading only
`This song has no verses`; no song still hides the field; a song with verses still shows the full picker.

## Phase 1 — Setup

- [X] T001 Worktree `~/Projects/multimedia-gkps-klender-235` on `fix/235-empty-song-verse-summary` off `be9863d2` (`develop`, VERSION 1.36.19); spec 235 and ITEM-250 checked free across all local refs.
- [X] T002 [P] `specs/235-empty-song-verse-summary/` — spec, preview (accepted Gate 1 2026-11-24), checklist, research, data-model, contracts, quickstart, plan; `backlog/items/ITEM-250-empty-song-verse-summary.md` and its In progress row.

## Phase 2 — Foundational (red first)

- [X] T003 [P] [US1] `tests/e2e/test_entries.py` — write `test_an_empty_song_shows_only_the_verse_summary` (FR-001, FR-002, SC-001, SC-002): from the home URL, open a service, Add Song, assert the panel is 0px with no song, pick the verse-less song, assert the label and panel are visible, the panel's only visible content is `This song has no verses`, no visible checkbox/tile/helper/All/Clear, summary bottom rule `0px`, and the panel measures about 39px. Confirm it fails on the unchanged product.
- [X] T004 [P] [US1] `multimedia/web/tests.py` — extend `ServiceEntryViewTests::test_an_edit_form_for_a_verse_less_song_states_it_in_the_markup` for FR-003: the panel is **not** `hidden`, carries `data-empty="true"`, and the summary still reads `This song has no verses`. Confirm it fails on the unchanged template.
- [X] T005 [US1] `tests/e2e/test_entries.py` — update `test_a_song_with_no_verses_is_named_and_cannot_be_saved`: the existing 0px assertion after the pick becomes the summary-only state; keep the no-song 0px assertion, the zero-checkbox count and the exact save refusal (FR-001, FR-005).

## Phase 3 — US1 (P1)

**Goal**: an empty song is named in the section, with nothing unusable drawn.

- [X] T006 [US1] `multimedia/web/templates/reading/_entry_form.html` — hide the panel only when no song is picked; add `data-empty="true"` when `form.song_has_no_verses`, keeping `data-settled="true"` so the first paint shows the panel. Passes T004.
- [X] T007 [US1] `static/web/entries.js` — in `verseSummary()` set `shouldHide = !songPicked`, derive `panel.dataset.empty` from `songPicked && !boxes.length`, and leave the reveal branch byte-identical. Passes T003 and T005's state assertions.
- [X] T008 [US1] `static/styles/design/components.css` — under `.editor__verse-panel[data-empty="true"]`, hide `.editor__verse-quick`, `.editor__verses` and `.editor__verse-readout`, and zero the summary's margin-bottom, padding-bottom and bottom border. Passes T003's geometry assertions.

## Phase 4 — US2 (P2)

**Goal**: the full picker and every other state survive unchanged.

- [X] T009 [P] [US2] `tests/e2e/test_entries.py` — extend the new test with an empty → populated swap: pick a song with verses after the empty one, assert no `data-empty`, ten tiles, verse 1 ticked and summary `Bait 1`; then re-pick the empty song and assert the summary-only state returns (FR-004, US2/AC1).
- [X] T010 [US2] Run the existing pins `test_the_song_pick_searches_and_the_verses_start_all_checked` and `test_single_verse_song_keeps_checked_verse_and_disables_picker` unchanged; fix any regression caused by the `data-empty` branch (US2/AC2–3, FR-004).

## Phase 5 — Polish and delivery

- [X] T011 Run `multimedia.web.tests.ServiceEntryViewTests` and `tests.e2e.test_entries.EntryModalE2ETests` with the shared DB; record counts and any pre-existing reds.
- [X] T012 [P] `docs/spec/reading.md` — Fold `reading/R30` (modified: the picked-but-empty state shows the section's summary row instead of hiding it, with the previous hidden-section answer kept as superseded) and `reading/R48` (modified: the empty state collapses the body rows under `data-empty`); update the header date and slice list; write `fold.md`.
- [X] T013 [P] `VERSION` 1.36.19 → 1.36.20 and a `CHANGELOG.md` `[Unreleased]` line for the change (bump declared in `plan.md`).
- [X] T014 `backlog/board.md` + `backlog/items/ITEM-250-…md` — move the row to In review with the PR number once the push returns it; in the pre-merge commit set the card `status: done`, `closed_at`, `closed_reason: merged into develop (PR #N)` and move the row to Done with `develop via [#N]`. Spec and board close on the same PR.
- [ ] T015 Write `converge.md` from the traceability table, then report the closing summary and ask before pushing. No push without the owner's word.
