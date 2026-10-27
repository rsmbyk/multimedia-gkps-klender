# Convergence: The landing search field sits on the window's middle

**Slice**: `specs/139-home-search-center` · **Date**: 2026-10-27

## Pass 1 — code against Plan's traceability table

Every row was re-read against the code and its declared method, not against a checkbox.

| Row | Method | Evidence | Outcome |
| --- | --- | --- | --- |
| FR-001, SC-001, US1.1–US1.4 | `test` | `test_the_field_is_on_the_window_middle` — 11 windows, `|cy − innerHeight/2| ≤ 1`; green | matches |
| FR-002, SC-003, US1.2, edge 320×568 | `test` | `test_the_logo_stays_whole_above_the_field` — logo top ≥ 0, gap 26px at 11 windows; green | matches |
| FR-003, SC-002 | `test` | `test_the_landing_page_is_one_window_tall` — `scrollHeight == innerHeight`, `scrollWidth == clientWidth`; green | matches |
| FR-004 | `test` | `test_the_phone_layout_centres_too` — section equals the stage's content box and the field is on the middle at 720/600/390/320; green | matches |
| FR-005, SC-004, US2.1, edge "never recentres" | `test` | `test_the_results_bar_keeps_its_place` — field top 46 / 82, bar 88, results 128 / 164, unchanged after a resize; green | matches |
| FR-005, SC-004, US2.2 | `test` | `test_the_reading_page_is_unchanged` — the section is not painted and `.read` sits on the stage content box; green | matches |
| FR-006 | `test` | `test_the_field_does_not_travel` — `scrollY == 0`, `transitionDuration` starts `0s`, centre unchanged after 400ms; green | matches |

Module run: `Ran 7 tests … OK` (74.191s), isolated `test_gkps139` so no neighbouring session shares the
database. Neighbouring suites after the change — `tests.e2e.test_drawer_shell`,
`tests.e2e.test_reading` — `Ran 114 tests … FAILED (failures=1)`: the one red is
`test_the_panel_shows_its_empty_view_when_no_songbook_exists`, the pre-existing failure already carried
by **ITEM-137**, identical in the pre-change baseline run. No new red, no error.

The shipped stylesheet was measured on the branch's own server (`:8775`, cwd confirmed as this worktree):
field centre equals the window's middle to **0.0px** at 1920×1000, 1440×900, 1280×800, 1024×768,
834×1112, 720×900, 390×844 and 320×568 — the same numbers the static preview predicted from `after.css`,
now read off `components.css` itself.

## Findings

| # | Type | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | mechanical | T014 said "move ITEM-149 to In review" and the card was moved there — contradicting C-SDD-BOARD and C-BOARD-GIT, which put that move at delivery, once a push has created the PR (`pr:` cannot be written before its number exists). A card in `In review` with no `pr:` is a card nobody can check. | **Fixed** — the card is `status: in-progress` in the board's `Ready` row with `branch:` set and `pr:` empty; `tasks.md` T014 now states the rule and names this correction. |
| F2 | missing | T013 requires the numbers to come from the shipped stylesheet, but `preview/probe_preview.py` could only measure the two static pages. | **Fixed** — the probe takes `--url <url>` and measures a running instance; the run above is its output. |
| F3 | unrequested | The stylesheet change also made `.search-home__form`'s `grid-row: 2` explicit on its existing one-line rule rather than adding a separate rule. | **Kept** — same declarations, no behaviour; it keeps the grid's anatomy in one place. |
| F4 | inspection | The stage's `padding` shorthand is now token-based, so a rule that sets one side must not rely on the shorthand: `@media print` (`padding: 0 !important`), the narrow-width `padding-left/right` blocks, and `[data-read="on"] .stage { padding-bottom: 0 }` all still win by specificity and `!important`. Read, not assumed. | **No change** — verified by inspection of the three rules. |

## Outcome

**Converged**, pass 1: every row of the traceability table is met by the method it declared, the
capability delta is ready to fold, and no gap is left accepted. No pass 2 was needed.
