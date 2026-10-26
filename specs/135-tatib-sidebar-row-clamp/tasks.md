# Tasks: a Tata Ibadah sidebar row is three lines, ellipsized

**Slice**: `specs/135-tatib-sidebar-row-clamp` · **Branch**: `feat/135-tatib-sidebar-row-clamp`
**Order used**: T001 → T002–T004 → T005–T007 → T008–T010 → T011–T012 → T013–T016.
`[P]` marks order-independent work, not concurrency: one agent, one thread.

## Phase 1 — Setup

- [X] T001 Run the branch's suite as a baseline and record it — `multimedia/web`, then
  `tests/e2e/test_reading.py` and `tests/e2e/test_reorder.py` — so a later red is known to be this
  slice's.

## Phase 2 — Foundational (the payload every story consumes)

- [X] T002 [P] Write the failing payload tests in `multimedia/web/tests.py`: no 60-character cut
  (FR-002), an untitled text row's three body lines (FR-003), a titled text row's title alone
  (FR-004), a legacy row's two shapes (FR-007), a row that fits carrying no `…` (US1.2), and the
  filter's text keeping the whole entry (FR-010).
- [X] T003 Make T002 pass in `multimedia/web/reading/views.py::_tatib_stage`: drop `label[:60]` and
  the legacy `+ '…'`; build `label_lines` per kind (three body lines with a trailing `…` when
  `_clamped_paragraphs` reports clipped, the title alone when titled, the citation, the kind's name,
  the two song entries); set `label` to the space-joined lines; remove `two_line_label`.
- [X] T004 [P] Render `label_lines` in `multimedia/web/templates/reading/_toc.html`: one
  `.songrow__t` block with `<br>` between lines; the song branch keeps `.songrow__heading` and
  `.songrow__verses` as two blocks with no `<br>`; the `two_line_label` branch goes.

## Phase 3 — US1: every kind is three lines and ellipsized

- [X] T005 [P] [US1] Write the failing E2E in `tests/e2e/test_reading.py`:
  `test_a_contents_row_is_three_lines_and_ellipsized` and
  `test_every_row_kind_stays_within_three_lines` — a long text body, a 64-character title, a long
  media filename and a legacy body each paint ≤ 3 line boxes at 1440×900, 1280×800 and 390×844, and a
  row that hides text ends `…` (FR-001, FR-006, SC-001, SC-002).
- [X] T006 [P] [US1] Write the failing E2E in `tests/e2e/test_reading.py`:
  `test_no_row_label_overflows_the_panel` — a 64-character unbroken title in every kind and the
  81-character Drive link report `scrollWidth == clientWidth` at the three widths (FR-008, SC-005).
- [X] T007 [US1] Add the clamp in `static/styles/design/components.css` until T005 and T006 pass:
  `.songrow__t` becomes the three-line box with `overflow-wrap: anywhere`; `.songrow__t--lines`'s
  flex column and `.songrow__line--blank` go.

## Phase 4 — US2: a song keeps its `Bait …` line

- [X] T008 [P] [US2] Write the failing payload test in `multimedia/web/tests.py`:
  `test_a_song_row_sends_its_heading_and_bait_line_separately`, and
  `test_a_song_without_a_verse_line_has_three_lines_for_its_heading` (FR-005, US2.4).
- [X] T009 [US2] Write the failing E2E in `tests/e2e/test_reading.py`:
  `test_a_song_row_keeps_its_bait_line_under_a_long_heading` — a heading needing three lines is
  capped at two ending `…`, `Bait …` is the third, and the label box is 60px rather than 80px
  (FR-005, US2.1–US2.3).
- [X] T010 [US2] Make T008 and T009 pass: the `:has(.songrow__verses)` heading clamp in
  `components.css`, and the two-block song row in `_toc.html`.

## Phase 5 — US3: the saved copy draws the same rows

- [X] T011 [P] [US3] Write the failing E2E in `tests/e2e/test_saved_render_parity.py`:
  `test_a_saved_service_row_matches_the_server_row` — the saved row's line count, wrapping and
  trailing `…` equal the server row's (FR-009, SC-004).
- [X] T012 [US3] Mirror the template in `static/web/offline-render.js::servicePage`: `label_lines`
  joined with `<br>`; the song row's two blocks with no `<br>`; drop the `two_line_label` branch.

## Phase 6 — Polish and delivery

- [ ] T013 Re-run the full matrix (unit, E2E, the three preview scripts) and record the numbers.
- [X] T014 Fold the capability — `docs/spec/reading.md` gains `R11` — and write `fold.md`
  (added: one requirement; the header moves `last folded` to 2026-10-26 and prepends `135`).
- [X] T015 Apply `bump: patch` in the pre-merge commit: `VERSION` `1.20.12` → `1.20.13`, one
  `CHANGELOG.md` line under `## [Unreleased]`, and the card's `release_version` left empty.
- [ ] T016 Write the PR title and body, move the card to `In review` once the push has created the
  PR (the owner's word governs the push itself).
