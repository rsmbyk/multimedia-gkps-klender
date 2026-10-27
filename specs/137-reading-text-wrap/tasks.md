# Tasks: a reading page's text wraps at its pane

**Slice**: `specs/137-reading-text-wrap` · **Branch**: `feat/137-reading-text-wrap`
**Order used**: T001 → T002 → T003–T006 → T007–T009 → T010–T011 → T012–T013 → T014–T017.
`[P]` marks order-independent work, not concurrency: one agent, one thread.

## Phase 1 — Setup

- [X] T001 Run the branch's neighbouring suites as a baseline and record them —
  `tests.e2e.test_reading`, `tests.e2e.test_song_label_typography`, `tests.e2e.test_media_library` —
  so a later red is known to be this slice's.

## Phase 2 — Foundational (the measuring helper every story consumes)

- [X] T002 Write `tests/e2e/test_text_wrap.py`: the class `ReadingTextWrapE2ETests` on
  `StaticLiveServerTestCase`, its `setUp` fixtures — a service named as a 64-character unbroken
  run holding a Text entry whose body is a long Drive URL, a song whose title is a long unbroken run
  followed by a name, a service and song with ordinary short names, a Bible chapter with a long
  pericope heading and a long verse — and one helper, `spill(selector)`, returning how far an
  element's painted text runs past its own box (range rectangles vs the padding box) plus the
  document's `scrollWidth - clientWidth`.

## Phase 3 — US1: the page title wraps inside the reading pane

- [X] T003 [P] [US1] Write the failing E2E `test_a_long_title_wraps_inside_the_pane`: the Tata
  Ibadah and song titles report 0px of spill, the document reports 0 horizontal overflow, and the
  title's computed `overflow-wrap` is `break-word` on the nested name span, at 1440×900, 1280×800
  and 390×844 (FR-001, FR-009, SC-002, US1.1, US1.2, US1.4).
- [X] T004 [US1] Write the guard `test_a_short_title_is_unchanged`: an ordinary service, song and
  Bible chapter keep one title line and the same box height the slice found, and a title with spaces
  still wraps at its spaces (FR-008, SC-003, the "spaces" and "no long text" edges). A guard, not a
  red-first test — it fails only if a later change disturbs the title's type or flow.
- [X] T005 [P] [US1] Write the failing E2E `test_the_title_keeps_its_box_and_the_toggle_its_line`:
  on a Bible chapter with the TB/SIM toggle in the title's row, measure the title's box width and the
  toggle's `y` with the rule in force, then set `overflow-wrap: normal` on `.read` in the page and
  measure again — both unchanged at 1440×900, 1280×800, 820×900 and 390×844 (FR-007, SC-005, the
  toggle edge).
- [X] T006 [US1] Make T003 and T005 pass: the rule `.read, .search-results, .preview {
  overflow-wrap: break-word; }` in `static/styles/design/components.css`, beside the other
  reading-root rules. Keep `break-word` rather than `anywhere` — if the widths in T005 differ, the
  value is the cause and the rule changes, not the test. The live preview already carries the rule
  (SDD-06), so this task confirms it rather than inventing it.

## Phase 4 — US2: every other reading surface wraps the same way

- [X] T007 [P] [US2] Write the failing E2E `test_no_reading_route_scrolls_sideways`: eight routes —
  a Tata Ibadah service, a song, a songbook, a Bible chapter, the search results, the media library,
  the Tata Ibadah list and the songs list — report `document.scrollWidth == clientWidth` at 1440×900,
  1280×800, 820×900 and 390×844 (FR-005, SC-001).
- [X] T008 [P] [US2] Write the failing E2E `test_a_body_paragraph_holding_a_link_wraps` and
  `test_a_bible_heading_and_verse_wrap`: the Text entry's Drive URL reports 0px of spill at 1440×900
  and 390×844; the chapter's `.read__sec` and `.v` report 0px at 1280×800 and 390×844
  (FR-002, SC-006, SC-007, US2.1, US2.2).
- [X] T009 [US2] Make T008 pass — the inherited rule reaches both surfaces through `.read`; no
  per-element declaration is added.
- [X] T010 [P] [US2] Write the failing E2E `test_a_search_result_title_wraps` and
  `test_preview_lines_wrap`: a search whose hit carries the long service name reports 0 horizontal
  overflow and 0px of spill on `.result-row__title`; the Preview modal opened on the Text entry
  reports 0px of spill on `.preview__line` (FR-003, FR-004, US2.3, US2.4, the hidden-`.read` edge).
- [X] T011 [US2] Make T010 pass: the `.search-results` and `.preview` roots of the same rule. If the
  modal's line does not inherit, the dialog is rendering outside the root and the selector is wrong.

## Phase 5 — US3: the truncating surfaces keep their cut

- [X] T012 [P] [US3] Write `test_a_truncating_row_still_truncates`: the sidebar's long service name
  is one line with `white-space: nowrap` and `text-overflow: ellipsis`, its `clientHeight` unchanged
  by the slice; a contents row keeps `-webkit-line-clamp: 3` (FR-006, SC-004, US3.1, US3.3, the
  `nowrap` edge). A guard: prove it is wired by temporarily removing `.book__n`'s `nowrap`, watching
  it fail, and restoring the rule.
- [X] T013 [US3] Make T012 pass: nothing to change. If it fails, a root selector has grown too wide
  and the fix is the selector, not the truncating rule.

## Phase 6 — Polish and delivery

- [X] T014 Re-run the matrix (T001's modules, `tests.e2e.test_text_wrap`, the three preview scripts)
  and record the numbers.
- [X] T015 Fold the capability — `docs/spec/reading.md` gains `R13` — and write `fold.md` (added: one
  requirement; the header moves `last folded` to 2026-10-27 and prepends `137-reading-text-wrap`).
- [X] T016 Apply `bump: patch` in the pre-merge commit: `VERSION` `1.21.0` → `1.21.1`, one
  `CHANGELOG.md` line under `## [Unreleased]`, the card's `release_version` left empty.
- [ ] T017 Write the PR title and body; move the card to `In review` once the push has created the
  PR (the owner's word governs the push itself), and `Done` before the merge.
