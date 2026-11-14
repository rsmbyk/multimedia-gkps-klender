# Plan 073: Give song Preview verse tabs equal shapes

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-076
- **Bump:** patch

## Why

The numbered verse tabs in a song entry's Preview modal vary in width with the digits. The accepted preview shows equal circles. This is the song Preview, not the Bible reading UI.

## Scope / edges

**In:** numbered song verse tabs inside the Tata Ibadah service-entry Preview modal.

**Out:** Bible verse controls, passage picker, song editor's verse checklist, and Preview content or verse selection rules.

## Approach

Give `.preview__tab` equal 30px width and height with fixed flex basis and centered digits. Preserve the existing tablist, selected tokens, keyboard navigation, and horizontal overflow behavior.

## TDD

- Domain/app tests: N/A; geometry-only change.
- E2E: extend `tests/e2e/test_entry_preview.py` with bounding-box equality for one- and two-digit song verses and existing keyboard selection.

## Risks

- A long list of tabs still needs horizontal scrolling on narrow screens.
