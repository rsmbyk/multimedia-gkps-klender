# Convergence: the preview's verse tabs get their own row

**Spec**: `specs/153-preview-tabs-row/spec.md` · **Plan**: `specs/153-preview-tabs-row/plan.md`

## Pass 1 — 2026-10-29

**What was checked.** Every row of the plan's traceability table by the method it declares: the seven new
E2E cases and the two cases whose locators moved (`tests/e2e/test_entry_preview.py`, 9/9 green), the
module's remaining pre-existing cases, the worktree's live page at `127.0.0.1:8832/tatib/144/`, the static
preview at 1440 and 390, and the code the table names (`_preview_modal.html`, `components.css:2076`,
`preview.js:324/509/571`).

**Measured on the live worktree page** (1440×900, dpr 1, the report's song):

| What | Value |
| --- | --- |
| dialog | 704 × 439.3 (was 704 × 401.3) |
| title band | 704 × 52, `border-bottom-width: 0px` (was 704 × 59, 1px) |
| title box | 660px, ellipsized from its 730px string (was 569.6px) |
| tab band | top 52px, 45px tall, `border-bottom-width: 1px` (was inside the header at 14px) |
| first tab | 22px from the dialog's left edge (was 605.6px) |
| body top | 97px (was 59px); first lyric line 22px below the rule |
| focus on open | `previewContent`; `:focus-visible` false on every tab |
| keyboard open | `previewContent` with its own ring; no tab ring |
| Tab / Shift+Tab | body → selected tab (`aria-selected="true"`) → body |
| a passage preview | 704 × 52 header, its own 1px rule, body at 52px, focus on `previewContent` — unchanged |

**Findings.**

| ID | Type | Finding | Disposition |
| --- | --- | --- | --- |
| C001 | partial | US3 AC3 ("a passage preview still focuses the body") pointed at a case that opens a passage but never asserts the focus. | **fixed in this pass** — `test_a_passage_preview_keeps_its_header_box_and_rule` now asserts `document.activeElement.id === 'previewContent'`, and the case is green. |
| C002 | — (not a gap) | US1 AC3 was declared `inspection`; the same behaviour is pinned by `test_a_song_preview_puts_its_verse_tabs_under_the_header`, whose fixture song's title fits the header. | checked by test, stronger than declared; recorded here. |
| C003 | — (not a gap) | Three cases in the module are red on unmodified `develop` at `24a6d6d2` — `test_the_preview_header_stays_put_while_the_body_scrolls`, `test_short_preview_arrow_keys_do_not_scroll_the_page`, `test_clicking_long_preview_text_allows_arrow_key_scrolling` — because at 900×380 the chapter drawer covers the entry and `item.hover()` times out after 62 retries. | not rows of this table; filed as **ITEM-163**. Reproduced on develop with the three cases run alone (three errors, 101s). |

**Related modules re-run** in this pass, for the surfaces the CSS/JS touch: `multimedia.web.tests`,
`tests.e2e.test_unified_text_screen_mode`, `test_single_screen_text_breaks`, `test_text_screen_breaks`,
`test_edit_request_feedback` — 305 tests, all green. (The first attempt reported six `ServiceReorderPaneTests`
errors; they were the local manifest trap — the run started before `collectstatic` had written `_static/` —
and disappeared on the re-run. Not a product finding.)

**Deferred to the delivery run**, per the owner's standing instruction to keep heavy browser suites at the
push step: the remaining preview-touching modules (`test_image_display`, `test_audio_display`,
`test_video_display`, `test_pdf_display`, `test_powerpoint_display`, `test_tatib_hover`, `test_text_wrap`)
and the full suite.

**Outcome.** Converged on the first pass: no `missing`, no `contradicts`, no `unrequested`; the one
`partial` was fixed inside the pass and its case re-run green. No accepted gaps. Passes used: 1 of 3.
