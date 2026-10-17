# Plan 104: Polish media picker layout and tab feedback

- **Status:** Accepted (2026-10-17)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-104
- **Bump:** patch

## Why

The New media modal currently shrinks when the Media Library tab has no files, so its empty-state preview loses the tall layout used by the Upload tab. In the Upload tab, the broad bold-text rule also makes “Supported files:” larger than the adjacent supported-types text. The Upload and Media Library tabs also lack the hover feedback used by the app's other segmented switches. Stable modal sizing, consistent typography, and matching tab feedback will make both tabs feel like parts of one form.

## Scope / edges

**In:**

- The connected-but-empty Media Library panel in the Tata Ibadah New media modal.
- Keep the New media modal at the same tall size on both tabs, subject to available viewport height; let the active panel use the remaining space while keeping the title and footer in place.
- The quiet, centered empty state with generous surrounding space and no call-to-action.
- Make the “Supported files:” label bold at the same 12 px size as the rest of its line.
- Add the existing-switch hover treatment to the inactive Upload/Media Library tab.

**Out:**

- The top-level Media Library page's empty state.
- Upload behavior, file management, selection behavior, and companion/API changes.
- A call-to-action button in the empty state.
- Changes to the existing disconnected-library message or modal open/close motion.

## Approach

Use [preview.png](./preview.png) for the connected-empty library tab, [upload-typography-preview.png](./upload-typography-preview.png) for the Upload-tab text correction, and [tab-hover-preview.png](./tab-hover-preview.png) for the inactive-tab hover state. Give the create modal a fixed available height capped at 760 px, while allowing the active file panel to scroll internally. Render the quiet empty state only after a successful connection and empty-list response; retain the existing unavailable message on connection failure. Match the hover fill, text color, and transition used by the app's segmented switches.

## TDD

- Domain/app tests: N/A; this is presentation of existing response states.
- E2E: extend `tests/e2e/test_media_library.py` to cover connected-empty and unavailable states, disabled Save, matching modal geometry across tabs, matching supported-files font size, and the inactive-tab hover state.

## Risks

- An empty response must not be confused with a failed companion request. Keep the two states separate and cover both in E2E.
- The fixed available height must still fit short viewports; keep overflow inside the active panel so the entry-title field, Save, and Cancel remain usable.
