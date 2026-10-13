# Tasks 087: Slimmer, softer scrollbars with no stepper buttons

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`chore/087-scrollbar-refinement`)
- [x] Red — app test: `tests/test_design_scrollbars.py` (new) asserts that `scrollbar-width` /
      `scrollbar-color` appear **only** inside the `@supports not selector(::-webkit-scrollbar)` block,
      that no stray standard width survives elsewhere, and that `::-webkit-scrollbar-button` is
      suppressed with a transparent track and corner
- [x] Red — E2E: `tests/e2e/test_reading.py::ScrollbarE2ETests`
      - [x] on the panel scroller, `offsetWidth - clientWidth` minus borders is 5px
      - [x] the scroller's computed `scrollbar-width` is `auto` (the native bar is not in use)
      - [x] a screenshot of the bar's top end carries no stepper glyph (it matches the surface beside
            it), with the native path as a control that the measurement discriminates
      - [x] the same in dark mode
      - [x] the mini panel and the entry list still draw no scrollbar — a CSS-text assertion, since a
            hidden bar is not observable in the headless browser
- [x] Green — `components.css`: the standard properties wrapped in the `@supports` gate, the
      `::-webkit-scrollbar` track/thumb taken to 5px, the button/corner suppression added, and the
      stray `scrollbar-width: thin` on the panel list removed (it forced Blink back onto the native
      bar for that list alone); `tokens.css`: the four thumb values per the spec's table
- [x] Confirm `tests/test_design_tokens.py` still passes unchanged
- [x] Run the targeted suites only: `tests/test_design_scrollbars.py`, `tests/test_design_tokens.py`
      and `tests/e2e/test_reading.py` (the scrollbar class)
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open;
      Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in this PR
