# Tasks: Height-bound song caption type

- [X] T001 Set `.obs-overlay__caption { font-size: 5cqh }` and document the 5 %/2 % rule in `static/styles/design/obs-overlay.css`
- [X] T002 Replace the fixed `CAPTION_FLOOR = 11` with a per-paint `captionFloor()` reading 2 % of the stage in `static/web/obs-overlay.js`
- [X] T003 Write `tests/e2e/test_obs_caption_height.py` covering the rest at two heights, the shrink band, and the floor edge
- [X] T004 Update the clamp-parsing assertion in `tests/e2e/test_obs_overlay.py` for the single `cqh` value
- [X] T005 Update `docs/spec/overlay.md` R2 rules and scenarios with the measured numbers
- [X] T006 Add card ITEM-212 and its board row (renumbered after a collision with develop's ITEM-209)
- [X] T007 Append the `[Unreleased]` changelog line
- [X] T008 Run the new E2E suite; confirm red against the old CSS/JS and green with the change
- [X] T009 Run the existing overlay suites; confirm no regression
