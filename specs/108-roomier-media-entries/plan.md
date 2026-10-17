# Plan 108: Give Tata Ibadah media entries more breathing room

- **Status:** Accepted (2026-10-17)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-108
- **Bump:** patch

## Why

Media entries currently have little vertical space around their icon, title, and file details. In a service order with text and break rows nearby, they look cramped. The accepted preview gives the media card more height and room inside it while leaving other entry types as they are.

## Scope / edges

**In:** Tata Ibadah media-entry card height, vertical padding, and spacing between consecutive service rows.

**Out:** File icon design, title alignment rules, media metadata, text-entry and break-entry geometry, hover/focus surfaces, and entry actions.

## Approach

Follow the accepted [media entry spacing preview](./preview.html). Set media rows to an 80 px minimum height with 16 px vertical padding and keep the 42 px file icon centered. Preserve the existing 12 px gap between service rows and text/break row heights. At 520 px and below, reduce the media row's left offset to 60 px and right padding to 12 px so long filenames wrap within the available width.

## TDD

- Domain/app tests: N/A; no domain or persistence rules change.
- E2E: update or add targeted Tata Ibadah browser coverage for media-row geometry, neighboring text/break rows, and narrow-screen overflow.

## Risks

The rule must override the shared 56 px entry-card minimum for media rows without changing the service row's existing hover gutter, controls, or action visibility.
