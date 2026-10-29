# Tasks: a passage and a song carry their own kind mark

**Slice**: `specs/144-passage-song-icons` · **Plan**: [`plan.md`](./plan.md) · **Bump**: `patch`

`[P]` means order-independent, not concurrent — run in one thread. The preview (specs 142/143's habit)
existed before the pack; the template, the stylesheet and the tests are this slice's own work, tests
first.

## Phase 1 — Setup

- [X] T001 [US1] Write `tests/e2e/test_stage_kind_marks.py`: a fixture service with one passage, four songs (two sharing the long `HAL 7` title), one text entry and three media entries, plus helpers for a row's box and a computed property; its first assertion is `test_a_passage_row_carries_the_passage_mark`. Run it against the pre-change tree and record the failure as the **absent `.entry__kind-icon`**, not an import or fixture error (`tests/e2e/test_stage_kind_marks.py`)

## Phase 2 — US1: a passage and a song are recognisable without reading (P1)

- [X] T002 [US1] Add the kind class to the stage row (`tatib__item--scripture` / `tatib__item--song`, beside the existing `tatib__item--media`) and the mark as the **heading's first child**, before `.entry__jump`, with the passage glyph inline. Provenance: research D1/D2/D6 (`multimedia/web/templates/reading/tatib.html`)
- [X] T003 [US1] Add the stylesheet seat: `.entry__kind-icon` at `left: 24px; top: 50%; transform: translateY(-50%); width: 20px; height: 20px`, its `svg` at 100%, and `padding-left: 64px` on the two kind classes — the media row's own column (`static/styles/design/components.css`)
- [X] T004 [US1] Add the song glyph (single flagged note) and `test_a_song_row_carries_the_song_mark`, asserting the two kinds carry **different path data**, not merely different `data-kind-icon` values
- [X] T005 [US1] Add `test_only_passage_and_song_rows_are_marked` and `test_a_text_row_carries_no_mark`, counting the mark per kind — the text entry, the section break and the media rows must not have one (FR-004, SC-001)

## Phase 3 — US2: a media file is never mistaken for a passage or a song (P1)

- [X] T006 [US2] Add `test_the_mark_is_not_a_media_chip`: the mark's box is **20 × 20** against the chip's **42 × 42**, its background is transparent where the chip has one, and its colour is `--head-ink` where the chip's is `--focus` (FR-003, SC-002, US2.2)
- [X] T007 [US2] Set the glyph's colour to `--head-ink` and add `test_the_mark_holds_contrast_in_both_themes`: compute the ratio from the painted colours on the canvas and on the hover fill, both themes, and assert **≥ 4.5:1** (FR-007, US3.3)
- [X] T008 [US2] Add `test_the_sidebar_and_dock_keep_their_own_rows`: no `.entry__kind-icon` inside `#chList`, and none on `/obs/dock/` (FR-008)

## Phase 4 — US3: the stage keeps its rhythm and its text column (P2)

- [X] T009 [US3] Add `test_a_passage_row_keeps_its_56px_box` and confirm it fails if the mark is moved to be the section's first child — the heading regains its 30px margin and the row measures **69.8px** — then keep the heading as the seat (research D1, FR-005, SC-004, US3.1)
- [X] T010 [US3] Add `test_no_other_block_moves`: every `.tatib__item`'s document top and the page's scroll height before and after the change, with the only permitted deltas being the declared song wraps (SC-003)
- [X] T011 [US3] Add `test_the_declared_wraps_at_the_400px_pane`: the four songs' boxes at the 400px pane are **86.3px** (`HAL 7` titles) and the passage stays **56px**; at the 1920px pane no title wraps (US3.2)
- [X] T012 [US3] Add `test_the_mark_is_decorative`: `aria-hidden="true"`, no text content, no `tabindex`, and the heading's accessible name equals the title's (FR-006, SC-005)
- [X] T013 [US3] Inspection: the mark's rule block declares no `transition`, and `prefers-reduced-motion` has nothing to switch off (US3.4)

## Phase 5 — Polish

- [X] T014 Regenerate `preview/preview.html`, `preview/compare.html` and the shots; correct `preview/README.md`'s table if any number moved (`specs/144-passage-song-icons/preview/`)
- [X] T015 Card `ITEM-160` (status, spec, branch), its board row, and the `specs/README.md` index row (`backlog/`, `specs/README.md`)
- [X] T016 Bump `VERSION` 1.22.7 → **1.22.8** and append the `## [Unreleased]` line — *a passage and a song now carry a mark of their own, in the media row's own column* (`VERSION`, `CHANGELOG.md`)
- [X] T017 Fold `docs/spec/reading.md`: one requirement added (the kind mark), with its scenarios (`docs/spec/reading.md`)

## Acceptance

- `tests.e2e.test_stage_kind_marks` — the slice's own module, fully green
- `tests.e2e.test_tatib_entry_controls`, `tests.e2e.test_text_wrap`, `tests.e2e.test_media_library`,
  `tests.e2e.test_song_label_typography` — re-run, since they measure the same rows
- `tests.e2e.test_tatib_hover`, `tests.e2e.test_entries`, `tests/e2e/test_reading.py` — the stage's
  neighbours, re-run for the same reason
- Known-red-on-develop modules are not this slice's evidence: see `backlog/board.md` Backlog
