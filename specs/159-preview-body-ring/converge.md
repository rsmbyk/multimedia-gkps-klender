# Converge: a preview's play shortcut paints nothing on the dialog's edge

**Spec**: `specs/159-preview-body-ring/spec.md` · **Passes run**: 1

## Pass 1 — 2026-10-29

**What was checked**: every row of `plan.md`'s traceability table against the code in the tree, by the
method the row declares. The module was run against the product files as they are, then against the
same files reverted to `develop` (`git checkout -- static/styles/design/components.css
static/web/preview.js`), so each claim about before and after is a run and not an inference.

**Findings**

| # | Row | Type | Evidence | Outcome |
| --- | --- | --- | --- | --- |
| 1 | FR-001, US1 AC1–AC3, SC-002 | none | `tests.e2e.test_preview_body_ring` — 7 cases, green on three consecutive runs (23.8 s / 20.2 s / 23.8 s) | met |
| 2 | FR-002, US2 AC1, SC-003 | none | `test_tab_brings_the_ring_back_after_a_space_press`: the outline reads `2px solid rgb(28, 92, 60) offset -2px` after a Tab | met |
| 3 | Edge: the next preview gets its ring back | none | `test_the_next_preview_gets_its_ring_back`, green | met |
| 4 | **FR-003, US2 AC2** | **missing evidence** | the row named `test_entry_preview.py::test_clicking_long_preview_text_allows_arrow_key_scrolling` and `::test_short_preview_arrow_keys_do_not_scroll_the_page`. Both **error on develop**, with my files reverted: `<aside id="chapters">` intercepts the pointer, 62 retries, Playwright timeout. The same three errors appear with and without this slice's diff (33.9 s either way) | **substituted**: two cases added to this slice's module — `test_a_space_press_leaves_focus_on_the_body` (the invariant that makes arrows work) and `test_arrow_keys_still_scroll_a_long_text_preview` (scroll down, return to top, with the new rule in place). Both green. The pre-existing reds are not this slice's and are reported below |
| 5 | FR-004, SC-002, edge: Escape, edge: seek | none | `test_audio_display` — `test_preview_plays_seeks_and_closes` green; the module's one red is `test_untitled_preview_and_projector_idle_display_off`, which is board card ITEM-140 ("identical on develop") and fails identically with this slice's files reverted | met; the red is a known gap, not this slice's |
| 6 | Edge: image and PDF previews unchanged | none | `test_image_display` and `test_pdf_display` ran green inside the 26-test sweep that produced only the four failures above (audio ×1, entry_preview ×3) | met |
| 7 | SC-001, SC-004 (manual) | not run | post-merge rows; compose serves `develop` and a worktree server is refused by the companion's origin allow-list | **accepted gap**, carried as T016 |

**Unrequested work**: none. The two added cases (finding 4) trace to FR-003, whose planned evidence
proved unusable.

**Outcome**: converged with one accepted gap (the two manual rows, which cannot run before the merge).
No `contradicts` findings. No code gap remains.

## Reported, not fixed — three reds outside this slice

`tests.e2e.test_entry_preview` errors on **three** cases, identically on unmodified `develop`:

- `test_short_preview_arrow_keys_do_not_scroll_the_page`
- `test_clicking_long_preview_text_allows_arrow_key_scrolling`
- `test_the_preview_header_stays_put_while_the_body_scrolls`

All three fail the same way: a hover is intercepted by `<aside id="chapters">` and Playwright retries 62
times. They are not in `backlog/board.md` — ITEM-184 collects three different reds — so they need a card
of their own. Proposed title: *"Three preview E2E tests cannot reach the reading pane: the chapters
sidebar intercepts the pointer"*.
