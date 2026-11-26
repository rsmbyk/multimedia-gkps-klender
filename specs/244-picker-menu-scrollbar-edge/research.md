# Research: picker popout scrollbar edge

**Spec**: `specs/244-picker-menu-scrollbar-edge/spec.md`
**Unknowns remaining**: 0

## D001 — Move the scrollport, not the options

- **Decision**: keep the menu's 8px padding for the filter and first option, and widen
  `.editor__picker-options` with `margin: 0 -8px -8px; padding: 0 8px 8px`.
- **Rationale**: the engine paints the bar against the scroll container's box. Measured on the live
  base at 1440×900, the Book menu's border box ends at x 938 / y 892 and its scrollport at 929 / 883
  — 9px (8px padding + 1px border) of canvas between bar and border. The negative margin takes the
  scrollport to 937 / 891 (1px border); the equal padding keeps the first option's box at
  x 511→929, y 464.1→503.1 and the chapter filter at x 511→929, y 510.1→548.1.
- **Alternatives considered**: (a) remove the menu's padding and re-pad every child — touches three
  child types and their gaps, so more moving parts for the same pixels; (b) custom-styled overlay
  scrollbar with a pseudo-element — a separate scroll mechanism that would break spec 087's
  5px bare bar and the browser's native keyboard scrolling; (c) shrink the menu's padding to 0px
  only on the inline end — leaves the bottom lane 8px short and the corner still painted over.
- **Provenance**: research — measured live, with spec 152's accepted negative-margin fix as precedent.

## D002 — Clip at the menu's radius

- **Decision**: add `overflow: clip` to `.editor__picker-menu`.
- **Rationale**: with the scrollport reaching the border, the bar's rounded tip would paint over the
  menu's 10px corner. `clip` follows the border radius; unlike `hidden` it does not make the menu a
  scroll container that a focus move could scroll. Computed `overflow` is `clip` after the change.
- **Alternatives considered**: `overflow: hidden` (creates a scroll container); `border-radius` on
  the scrollport alone (would square off the top corners where the filter sits and still need
  separate corner masks); leaving the corner untouched (bar paints past the radius).
- **Provenance**: research — spec 152's Transfers dialog uses the same mechanism for the same reason.

## D003 — CSS-only, no JavaScript or template change

- **Decision**: change only `static/styles/design/components.css`; leave `placeMenu()`, filter
  wiring and markup untouched.
- **Rationale**: the fixed menu's box, width and viewport cap come from `placeMenu()`; the measured
  436px chapter and 213px verse menus keep those boxes. Filtering, highlight scroll-follow and Tab
  commit live in `static/web/entries.js` and are already accepted in spec 238.
- **Alternatives considered**: recompute the menu's inline `maxHeight` for the extra 8px in JS —
  couples the visual fix to layout code and would make the before/after menu heights differ.
- **Provenance**: research — code path traced to `entries.js:387-410` and `components.css:2683-2693`.

## D004 — Evidence: live geometry before, browser E2E at push

- **Decision**: freeze the before/after boxes from the real page on the slice dev server for gate 1;
  write a targeted Playwright E2E during Implement and run the accepted spec 238 modules at the push
  step, not between gates.
- **Rationale**: a visual report names a symptom, not a cause. Box measurements on the live page show
  exactly which element carries the bar and prove the content did not move; the E2E pins it.
- **Alternatives considered**: a static preview copied from the templates — it cannot exercise the
  eager menu placement and filtering; screenshots alone — too faint at the 5px bar to measure.
- **Provenance**: owner preference (targeted verification between gates, heavy suites at push) and
  research (live probe output in `preview/README.md`).

## Open

<!-- empty when Phase 0 is finished; anything here blocks Phase 1 -->
