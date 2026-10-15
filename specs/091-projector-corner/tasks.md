# Tasks 091: Quiet controls for the mirrored service projector

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)
- **Go To amendment:** Accepted
- **Search clear amendment:** Accepted
- **Untitled Text cue amendment:** Accepted
- **Corner cue typography amendment:** Accepted
- **Shared corner colors amendment:** Accepted
- **Go To morph amendment:** Accepted
- **Number-only Go To amendment:** Draft

## Checklist

- [x] Owner accepts this Draft spec; stop until then.
- [x] Confirm the current feature branch is based on `develop`; keep preview files as reference only.
- [x] Add targeted domain/application tests for boundaries, translation payloads, lookup, and detours.
- [x] Add projector state and payload helpers for service entries and baits.
- [x] Add targeted `tests/e2e/test_projector.py` cases for keyboard navigation, mouse jumps, overlay interception, and fitting.
- [x] Implement projector keyboard behavior, find, detours, and shortcut sheet.
- [x] Implement the corner HUD, mouse zones, entry list, inactivity, and responsive overlays from the accepted previews.
- [x] Run the targeted projector unit and browser classes (45 passing tests).
- [x] Fill test and implementation paths in `spec.md` traceability.
- [x] Set ITEM-094 to In review, update the board, version and changelog for the minor bump, and open a draft PR against `develop` in the same PR.
- [ ] Before merge, complete the required remote CI and E2E, mark ITEM-094 Done, and check off delivered tasks in the same PR.

## Done when

- [x] Targeted projector scenarios pass and mouse and keyboard operation both work.
- [x] Implemented geometry and interaction states follow the accepted preview.
- [x] ITEM, board, tasks, version, changelog, and PR all describe the same delivered slice.

## Accepted amendment: one-suggestion Go To

- [x] Owner approves the [single-suggestion interaction preview](./preview-goto-autocomplete.html), including normal projector typography.
- [x] Owner explicitly accepts the [amendment](./spec.md#accepted-amendment-one-suggestion-go-to).
- [x] Add targeted projector browser tests in `tests/e2e/test_projector.py` for one visible suggestion, full result count, Up/Down wraparound, query preservation, Enter/click selection, empty state, stale responses, and overlay dismissal.
- [x] Replace the G popup's list rendering and selection controls in `multimedia/web/templates/reading/projector.html`, `static/web/projector.js`, and `static/styles/design/projector.css`; keep J and lookup ranking unchanged.
- [x] Run the targeted projector tests and confirm the reference-size and smaller-viewport layout against the approved preview.
- [x] Update this task list and the Spec 091/ITEM-094/PR descriptions with the delivered amendment before merge.

## Accepted amendment: projector search clear controls

- [x] Owner approves the [interactive preview](./preview-search-clear.html) for J and G.
- [x] Owner explicitly accepts the [amendment](./spec.md#accepted-amendment-projector-search-clear-controls).
- [x] Add targeted projector browser tests for icon visibility, click and keyboard clear, live result reset, retained focus, and stale G responses.
- [x] Add the shared clear-button markup and projector styling to both fields, and wire the buttons to their existing input handlers.
- [x] Run the targeted projector browser class (33 passing) and update the Spec/ITEM/PR delivery record.

## Accepted amendment: running untitled Text cue labels

- [x] Owner approves the [revised running-text cue preview](./preview-cue-running-text.html); the prior clipping and one-pass animation previews informed this revision.
- [x] Owner explicitly accepts the [amendment](./spec.md#accepted-amendment-running-untitled-text-cue-labels).
- [x] Add targeted projector browser tests for the shared overflow-triggered limit, adjacent long entries, repeating hover/leave, reduced motion, preserved J labels/search, and narrow viewport geometry.
- [x] Add the running and clipped label states only to untitled Text labels in the HUD renderer; reserve the quiet gap before the keyboard button.
- [x] Run the targeted projector browser class (35 passing) and update the Spec/ITEM/PR delivery record.

## Accepted amendment: quieter corner cue typography

- [x] Owner approves the [550-weight preview](./preview-cue-running-text.html), including the quieter resting first-line labels.
- [x] Owner explicitly accepts the [amendment](./spec.md#accepted-amendment-quieter-corner-cue-typography).
- [x] Change only cue text weight and resting untitled Text label color, keeping hover and highlight states higher priority and the SVG keyboard button unchanged.
- [x] Run targeted projector browser checks for resting, hovered, highlighted, and narrow-viewport cue states.
- [x] Update the Spec/ITEM/PR delivery record after implementation.

## Accepted amendment: shared corner control colors

- [x] Owner approves the [revised cue preview](./preview-cue-running-text.html) at `#514D47` for all normal-state cue text.
- [x] Owner approves the [shared state preview](./preview-cue-state-colors.html), including the corrected highlighted split count.
- [x] Owner explicitly accepts the [amendment](./spec.md#accepted-amendment-shared-corner-control-colors).
- [x] Apply shared resting, hover, and highlight/pressed/open colors across cue text and controls; remove keyboard-button background fills.
- [x] Run targeted projector browser checks for passage, song, untitled Text, and detour cues, including keyboard, next-entry, bait, translation, list, and split-count states.
- [x] Update the Spec/ITEM/PR delivery record after implementation.

## Accepted amendment: Go To morph animation

- [x] Owner approves the [Go To motion preview](./preview-goto-morph.html).
- [x] Owner explicitly accepts the [amendment](./spec.md#accepted-amendment-go-to-morph-animation).
- [x] Add Go To opening/closing state and 180ms service-list-style panel keyframes, with reduced-motion fallback and overlay interception until fully closed.
- [x] Add targeted browser checks for open/close, rapid reopen, outside-click protection, and reduced motion.
- [x] Update the Spec/ITEM/PR delivery record after implementation.

## Draft amendment: number-only Go To substring search

- [x] Owner approves the [numeric search preview](./preview-goto-number-substring.html).
- [ ] Owner explicitly accepts the [amendment](./spec.md#draft-amendment-number-only-go-to-substring-search); stop before implementation until then.
- [ ] Match active numbered songs by numeric substring for bare-digit Go To queries, with exact/prefix/substring tiers and no 12-result cap.
- [ ] Add targeted application and projector browser checks for cross-book matches, ordering, full count/cycling, and unchanged book-qualified and title queries.
- [ ] Update the Spec/ITEM/PR delivery record after implementation.
