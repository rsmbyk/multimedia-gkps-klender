# Converge: a reading page's text wraps at its pane

**Slice**: `specs/137-reading-text-wrap` · **Date**: 2026-10-27

## Pass 1

Checked the code against `plan.md`'s traceability table, row by row, by the method each row declared.

| Row group | Method | Evidence |
| --- | --- | --- |
| FR-001, FR-009, SC-002, US1.1–US1.2, US1.4 | `test` | `tests.e2e.test_text_wrap::test_a_long_title_wraps_inside_the_pane` — green; 0px spill and 0 document overflow for the 64-character Tata Ibadah and song titles at 1440×900, 1280×800, 390×844; the nested `#readName` span computes `overflow-wrap: break-word` (the inheritance the row is about) |
| FR-007, SC-005, the toggle edge | `test` | `test_the_title_keeps_its_box_and_the_toggle_its_line` — green at 1440×900, 1280×800, 820×900, 390×844; the title's box width and the toggle's line are identical with and without the rule |
| FR-002, SC-006, SC-007, US2.1–US2.2 | `test` | `test_a_body_paragraph_holding_a_link_wraps` (0px from 215px at 1440×900), `test_a_bible_heading_and_verse_wrap` (`.read__sec` and `.v` 0px at 1280×800 and 390×844) — green |
| FR-003, FR-004, US2.3–US2.4, the hidden-`.read` edge | `test` | `test_a_search_result_title_wraps` (0 document overflow at 820 and 390), `test_preview_lines_wrap` (0px spill inside the dialog) — green |
| FR-005, SC-001 | `test` | `test_no_reading_route_scrolls_sideways` — eight routes × four widths, `scrollWidth == clientWidth` everywhere — green |
| FR-006, SC-004, US3.1, the `nowrap` edge | `test` | `test_a_truncating_row_still_truncates` — the sidebar row is one line with `nowrap` + `ellipsis` and still clips; the contents row still reports `-webkit-line-clamp: 3` |
| FR-008, SC-003, the "spaces" and "no long text" edges | `test` | `test_a_short_title_is_unchanged` — the same height and width with and without the rule on a short service and song at three widths; a 57-character spaced title still wraps |
| US3.2, the one-character edge | `inspection` | `.media-library__filename` and `.book__n` untouched in `components.css`; the media-library preview page draws the same one-line row |

### The red the tests were written against

| State of the rule | Result |
| --- | --- |
| `overflow-wrap: normal` (today's value) | **8 of 9 red** — every wrap test above failed on 100–1,200px of spill and a sideways-scrolling document; the truncation guard stayed green |
| `overflow-wrap: anywhere` | `test_the_title_keeps_its_box_and_the_toggle_its_line` red — the title's box measured 278px where the shipped value gives 284px at 390×844, the min-content collapse the value was chosen to avoid |
| `overflow-wrap: break-word` (shipped) | **9 of 9 green** in 42.9s |

### Neighbouring modules (T014)

| Module | Tests | Result |
| --- | --- | --- |
| `tests.e2e.test_text_wrap` | 9 | OK |
| `tests.e2e.test_song_label_typography` + `tests.e2e.test_media_library` | 24 | OK |
| `tests.e2e.test_reading` | 86 | 1 failure — `test_the_panel_shows_its_empty_view_when_no_songbook_exists`, the known red of ITEM-137 |
| the four together | 119 | 1 failure — the same one |

### Live check on the real routes (the worktree's server, changed code)

From `preview/probe_wrap.py`, rebuilt against the shipped rule:

| Route | Document overflow before → after (1440 / 1280 / 390) | The run that overflowed |
| --- | --- | --- |
| `/tatib/149/` | 1,033 / 1,193 / 571 → 0 / 0 / 0 | title 1,082 → 0px; body link 215 → 0px |
| `/songs/1817/` | 380 / 540 / 257 → 0 / 0 / 0 | title 444 → 0px |
| `/bible/1/1/` | 0 / 79 / 376 → 0 / 0 / 0 | pericope heading 143 → 0px at 1280 |
| `/search?q=…` | 467 / 547 / 996 → 0 / 0 / 0 | result title 614 → 0px |

The sidebar row still hides 281px inside its 293px box, one line, before and after — the truncation
the slice must not touch.

### Findings

| # | Type | Finding | Outcome |
| --- | --- | --- | --- |
| C1 | `contradicts` (spec side) | The spec called the fixture a *1,000-character* title. `TataIbadah.name` and `Song.title` are `max_length=64`, and both live records are exactly 64 characters — a longer value cannot be stored. The requirement and every measured number hold; only the illustration was wrong. | Corrected in `spec.md`, `plan.md`, `data-model.md`, `tasks.md`, the card and the preview README; the test fixtures use the real maxima (64 / 32 / 128). Requirement unchanged, so the spec's Accepted text was edited only where it named the length; recorded here and in `checklists/requirements.md` as CHK012. |
| C2 | `partial` | FR-007's second clause — "the language toggle keeps the position it takes today" — cannot hold pixel for pixel: a title that now wraps is taller, and whatever sits under it moves down with it (109px → 136px at 390×844). | Read as **the slot, not the pixel**: the toggle keeps the line it takes (its own line, below the title), which is the layout decision `anywhere` would have changed. `test_the_title_keeps_its_box_and_the_toggle_its_line` asserts that reading. Flagged for the owner rather than reworded after gate 1. |
| C3 | `note` | The first combined run reported two failures; its tail retained one. A re-run of the identical command reported one. | The second failure did not reproduce in two later runs of the same modules. Recorded, not dismissed: if it recurs it is a flake in this repository's browser suite, not a behaviour gap. |
| C4 | `none` | The single persistent red, `test_the_panel_shows_its_empty_view_when_no_songbook_exists`, was run on the untouched `develop` checkout: it fails there with the identical assertion (`'No songbooks yet…' != 'No matching songbooks.'`). | Pre-existing, carried by ITEM-137. Not this slice's, and not fixed by it. |

### Outcome

**Converged** on pass 1. Every row in the traceability table has its declared evidence, the test
written for each row was shown failing before it passed, and the one `contradicts` was a fact about a
column limit rather than a behaviour — corrected with its delta stated. C2 is the only open reading,
and it is a wording question for the owner, not a gap in the code.

### Order note

Fold ran in the same working session as this pass, against the code this pass measured: the
capability delta (`reading/R13`), `fold.md`, `VERSION` and `CHANGELOG.md` are written after it and
change no implementation.
