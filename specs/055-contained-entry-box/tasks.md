# Tasks 055: Give each entry a containing box with centred words and equal add-row gaps

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/055-contained-entry-box`)
- [x] Red — E2E rewrites (`tests/e2e/test_tatib_entry_controls.py`):
      `test_the_controls_never_sit_on_the_words` → containment + centring;
      `test_the_item_height_includes_the_controls` → the 52px box;
      `test_the_band_tracks_the_controls_exactly` → `min-height: 52px`, `padding-top: 0px`;
      `test_at_rest_the_add_rows_reserve_no_space` → uniform 12px rhythm, rows/bar 0-high;
      `test_hovering_an_entry_settles_with_both_rows_open` → 8/8 gaps, re-bound shift.
- [x] Red — E2E new: start bar collapses/reveals (8px under the heading, 8px above the first
      words); a gap-equality audit across first entry / card / one-liner / divider / focus
      (8/8); a centring audit (top ≈ bottom); touch rule covers the bar.
- [x] Red — regression files: `tests/e2e/test_reorder.py` (reveal the bar before clicking it),
      `tests/e2e/test_tatib_section_break.py` (margins 0, rule centred, box 52px),
      `tests/e2e/test_tatib_hover.py` (the bar's one-time first-entry shift), `tests/e2e/test_entries.py`
      (click-through with the collapsed bar).
- [x] Green — implementation (`static/styles/design/components.css`: box, row margins/padding,
      bar collapse + pull-up, `.tatib__eos` box, coarse-pointer block; `static/web/entries.js`:
      bar sync alongside the neighbours reveal; `multimedia/web/templates/reading/tatib.html`:
      `.entry__start-inner` wrap).
- [x] Green — targeted E2E runs (the files above); full suite is the push step.
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
