# Converge: a Tata Ibadah sidebar row is three lines, ellipsized

**Slice**: `specs/135-tatib-sidebar-row-clamp` · **Date**: 2026-10-26

## Pass 1

Checked the code against `plan.md`'s traceability table, row by row, by the method each row declared.

| Row group | Method | Evidence |
| --- | --- | --- |
| FR-002, FR-003, FR-004, FR-007, FR-010, US1.2 | `test` | `multimedia.web.tests.ServiceEntryViewTests` — 12 new tests, the whole class green (125 tests) |
| FR-001, FR-005, FR-006, FR-008, SC-001, SC-002, SC-005, US1.1–US1.5, US2.1–US2.3 | `test` | `tests.e2e.test_reading.ReadingE2ETests` — three new tests green at 1440×900 and 390×844 |
| FR-009, SC-004, US3.1 | `test` | `tests.e2e.test_saved_render_parity.SavedRenderParityTests.test_a_saved_service_row_matches_the_server_row` — green |
| US2.4 | `test` | `test_a_song_without_a_verse_line_has_three_lines_for_its_heading` — green |
| Edge: blank body line | `inspection` (upgraded) | wrote `test_a_blank_body_line_keeps_its_line` and the E2E blank-row measurement instead; both green |
| Edge: stage pane untouched | `inspection` | `PANE_TEXT_LINES` still 3 and `_clamped_paragraphs` unchanged; `multimedia.web` green |
| Edge: hover/selected/focus keep the height | `manual` | the rules add no height on state; `preview/cases.html`'s selected row measures the same 65.25px |

### Live check on the real routes (the worktree's server, changed code)

| Route | Rows | Over three lines | Overlapping its pane | `Bait …` hidden |
| --- | --- | --- | --- | --- |
| `/tatib/144/` at 1440×900 | 9 | 0 | 0 | 0 |
| `/tatib/144/` at 390×844 | 9 | 0 | 0 | 0 |
| `/tatib/143/` (the pasted Drive link) at 1440×900 | 1 | 2 lines, wrapped | 0 | — |
| `/tatib/143/` at 390×844 | 1 | 3 lines, wrapped | 0 | — |

### Findings

| # | Type | Finding | Outcome |
| --- | --- | --- | --- |
| C1 | `unrequested` | the honesty of the old test's shape: the E2E test asserting `.songrow__line` spans no longer described the markup, so it was rewritten to measure line boxes instead. | folded into T005/T007; the test now measures what the spec says |
| C2 | `partial` | T013's "full matrix" was run as the modules this slice touches (`multimedia.web` 343, three E2E modules 14, the three new E2E tests, `tests.e2e.test_reorder`) rather than the whole suite, which belongs to the push step by the owner's standing preference. | recorded; the remaining matrix is the pre-merge run, not a gap in behaviour |

### Outcome

**Converged** on pass 1: every requirement, success criterion and scenario in the traceability table has its
declared evidence and none contradicts the spec. The one `partial` is a scheduling fact, not a behaviour gap; it is
listed above rather than carried silently.

### Order note

The run wrote the Fold artifacts (`docs/spec/reading.md` `R11`, `fold.md`, `VERSION`, `CHANGELOG.md`) in the same
working session as this pass; the code they describe is the code this pass measured. Nothing in Fold changed the
implementation.
