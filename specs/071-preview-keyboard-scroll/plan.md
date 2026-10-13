# Plan 071: Scroll Preview text with arrow keys

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-074
- **Bump:** patch

## Why

The Preview dialog scrolls its body while keeping the footer fixed. After a pointer click on non-interactive text, focus stays on the dialog, so ArrowDown and ArrowUp do not scroll that body. The owner asked to use the arrow keys after clicking text.

## Scope / edges

**In:** Focus the shared Preview scroll region when its non-interactive content is clicked; support native arrow-key scrolling across Text, Single-screen Text, passage, and song previews. Keep buttons, links, tabs, Escape, backdrop dismissal, and focus restoration working.

**Out:** Changing Preview content, break placement, projection, scrollbar styling, page scrolling outside the dialog, or the Text-entry mode redesign discussed separately.

## Approach

Make the Preview body keyboard-focusable. When a click lands on plain content, focus that body without moving its scroll position. Leave focus on interactive descendants so their normal keyboard behavior remains. Let the browser handle ArrowUp, ArrowDown, PageUp, and PageDown natively while the body can move. At its top or bottom, cancel only the key that would scroll the page behind the dialog; add no custom scroll distance.

The owner accepted this behavior preview. It was a temporary browser-only trial against the local app at a 900 × 380 viewport. Before the trial, clicking text left focus on `previewModal` and ArrowDown kept `scrollTop` at 0. With the proposed focus behavior, clicking text focused `previewContent`; ArrowDown moved `scrollTop` 0 → 40 px, ArrowUp moved it 40 → 0 px, and Escape closed the dialog. No product files changed during the trial.

## TDD

- Domain/app tests: N/A; this is browser focus and native scrolling behavior.
- E2E: Extend `tests/e2e/test_entry_preview.py` with a long Preview body and short viewport. Assert clicked text focuses the body and ArrowDown/ArrowUp change its `scrollTop`; verify a Preview control keeps keyboard focus and Escape closes the dialog.

## Risks

- A click on a button, link, tab, or form control must not be stolen by the scroll body.
- Native arrow scrolling can chain to the page at the body edge, so guard only those edge keystrokes.
- Pointer focus must not cause a jump in the body, and keyboard users must retain a visible focus cue when tabbing to it.
