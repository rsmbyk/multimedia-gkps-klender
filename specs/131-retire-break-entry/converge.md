# Converge: The Break kind retires, and the breaks already written stay

**Spec**: `specs/131-retire-break-entry/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-10-25

Every requirement re-read against the shipped diff, not against its checkbox.

| Requirement | Check | Evidence |
| --- | --- | --- |
| FR-001 | no Break control in any server surface, four tile tracks | `grep -rn 'section_break' multimedia/web/templates` → only `views.py`'s render path, no template; `ServiceEntryKindRetirementTests::test_no_page_offers_a_break` and `…::test_an_empty_service_offers_four_tiles` green; probe `--shipped`: 4 buttons in the add row, 4 tiles 238px wide |
| FR-002 | the rebuild offers the same four | `tests.e2e.test_entries` (22 tests with `test_edit_request_feedback`) green, including the rebuilt-row count `4` |
| FR-003 | the saved renderer offers the same four | `tests.e2e.test_saved_render_parity` 7 OK (`icon_count` 4, tile count 4, tile metrics compared saved vs server) |
| FR-004 | the writing endpoints refuse a create | `…::test_the_break_kind_cannot_be_created` — three POST shapes (`bare`, `after=start`, with title) → `404, 404, 404`, row count unchanged; the new-form GET is `404` |
| FR-005 | the edit form and save refuse an existing break | `…::test_an_existing_break_cannot_be_edited` — GET `404`, POST `404`, row re-read: kind 3, title and text `''` |
| FR-006 | the divider, sidebar row and projector screen unchanged | `tests.e2e.test_tatib_section_break` 6 OK (`56px` box, centred rule, no label, Delete only); `tests.e2e.test_projector` 44 of 47 on the first run — see the flake note below — and the three re-run green |
| FR-007 | Delete still removes it and closes the order | new `…::test_a_break_deletes_from_its_divider`: dialog → `POST /editor/entry/<pk>/delete/` → `200`, one divider fewer, `break_pk` gone, remaining entries renumbered `1, 2` |
| FR-008 | reorder unchanged | `tests.e2e.test_reorder` 31 OK, including the break-drag test |
| FR-009 | the saved page draws an existing break as the server route does | `tests.e2e.test_saved_render_parity` 7 OK; `tests.e2e.test_offline_library` 20 of 21 — see the note below |
| FR-010 | the kind, its value and its display name survive | `…::test_the_kind_and_its_rows_survive` — `int(SECTION_BREAK) == 3`, display `Section Break`, two dividers in the pane, the break's Delete present, its `toc__eos` row present |
| FR-011 | the legacy row keeps both controls | `…::test_the_legacy_row_keeps_both_its_controls` green; `tests.e2e.test_tatib_section_break`'s legacy-note assertion green |
| SC-001 | no surface offers one | the three markup/saved runs above: four `data-entry-open` values, none `section_break`; probe `--shipped` shows four buttons and four tiles |
| SC-002 | a direct save cannot create one | three POSTs → `404`, `service_entries` unchanged |
| SC-003 | reading, projecting, deleting | the three suites above + the delete E2E |
| SC-004 | nothing else moved | probe `--shipped` at 1440×900: add row 400px block, buttons 84 / 64 / 58 / 71px × 28px, 6px gaps, row centre offset 0; empty tiles 52px × 52px, 10px gaps, 238px wide, centre 1176px; divider box `56px` (existing E2E) |
| SC-005 | the four remaining kinds untouched | `manage.py test multimedia.web` **320 OK**; entries/feedback **22 OK**; reorder **31 OK**; section break **6 OK** |

**Outcome**: no `missing`, `contradicts` or `unrequested` gap. Three deliberate removals, each recorded:

- **a test with its behaviour** — `tests/e2e/test_edit_request_feedback.py::test_non_modal_break_write_disables_only_its_initiating_button`
  guarded the direct non-modal write of a break. No non-modal write exists now, so the behaviour is gone (TDD-07).
  The shared toast path it exercised is still covered by that module's song-picker and reorder tests.
- **two tests repointed** — the two "instant break lands after its add row" tests became the same tests for a
  Text entry, because the insertion behaviour they guard still exists and was never break-specific.
- **the empty row's fifth track** — dropped with the tile, since leaving it would put four tiles 26px left of
  centre (measured: 238px of tiles in a 300px row).

**Two failures that are not this slice's:**

- `tests.e2e.test_projector` — `test_moving_and_toggling_morph_rather_than_jump`,
  `test_goto_morph_blocks_clicks_during_close_and_survives_rapid_reopen` and
  `test_open_popups_keep_hud_visible_and_goto_has_clear_click_overlay` failed on the full suite under load
  (385s wall) on animation-timing assertions, and all three passed when re-run alone in 11.1s. Pre-existing
  flakiness, unrelated files.
- `tests.e2e.test_offline_library::test_saved_content_and_projector_survive_disconnection` failed with
  `ERR_INTERNET_DISCONNECTED` on navigating to the projector after the browser is set offline. Reproduced on
  `develop` at `3a360d06` in the main checkout, same error, same test: environmental, pre-existing.

## Pass 2 — 2026-10-25

After the fold, the changelog line and the bump: every requirement re-read once more against the tree.

- `manage.py test multimedia.web` — **320 OK** (re-run after `docs/spec/reading.md`, `CHANGELOG.md` and
  `VERSION` were written; no source file had changed since pass 1).
- `tests.e2e.test_tatib_section_break` — **6 OK** after the fold.
- The probe was re-run with `--shipped` on the folded tree and still reads four buttons, four tiles, 238px,
  centre 1176; frames `add-row-after-shipped.png` and `empty-before-shipped.png` were saved from that run.
- `grep -rn 'section_break' multimedia/web/templates static/web` → no hits: no creation surface carries the
  kind's name any more, and both scripts lost their maps for it.

No requirement moved between the passes. No gap is accepted.
