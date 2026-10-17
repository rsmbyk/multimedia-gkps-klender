# Plan 109: Show distinct connection icons in the Media Library status row

- **Status:** Accepted (2026-10-17)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-109
- **Bump:** patch

## Why

The local Media Library status popover currently communicates its Connection state with text alone. The approved preview adds a small state icon so Connected and Unavailable can be scanned quickly, while keeping Unavailable calm and non-alarming.

## Scope / edges

**In:** The inline icon and alignment in the Connection row of the Media Library status popover.

**Out:** The status button's dot, connection detection and refresh behavior, the Connected/Unavailable labels, file-count and total-size visibility, companion API, errors, and other Media Library controls.

## Approach

Follow the accepted [Media Library preview](./preview.html). Add a decorative 17 px SVG icon before the existing state label, with a 7 px gap. Use a green outlined check-circle for Connected and a neutral outlined rounded square with a horizontal dash for Unavailable. Use the app's `--head-ink` token for the neutral icon (the preview's equivalent is `--muted`). Keep the existing label and its typography, preserve the hidden inventory rows while unavailable, and leave the status-button dot and all connection logic unchanged.

## TDD

- Domain/app tests: N/A; connection rules and persistence do not change.
- E2E: extend `tests/e2e/test_media_library.py` to verify the correct visible icon and state label for connected and unavailable responses, including a state refresh without stale icons.

## Risks

Unavailable is not necessarily a failure. Its icon must use the existing muted theme color and must not use danger styling. The SVG must be hidden from assistive technology so the existing text remains the accessible state.
