# Spec 079: One Text entry with a selectable default screen mode

- **ID:** 079
- **Status:** Accepted
- **Item:** ITEM-082
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

Use one Tata Ibadah Text entry for both Multi-line and Single-screen projection. Let an editor choose the default on creation and see or change the current screen arrangement in Preview.

## Scope

### In scope

- ServiceEntry Text records, their Create and Edit forms, Add Text actions, Preview footer, saved break controls, and projector screens.
- Migration of existing ordinary and Single-screen Text entries.
- Live projection updates and editor/viewer permission states.

### Out of scope

- Song, Scripture, and section-break data and workflows, legacy service items, and old OBS docks or web sources. Shared editor picker positioning may be adjusted to preserve existing modal behavior.
- A projector-screen preview inside the entry Preview dialog.

## Domain rules

- A Text entry has one stored default screen mode: Multi-line or Single-screen. The saved custom break list remains null when the default is active. A list, including an empty list, means Custom; Custom is never a selectable stored default.
- Multi-line default pairs nonempty lines and uses blank written lines as mandatory screen boundaries. Its custom breaks follow the existing Spec 069 rules, including first-action two-line cadence from an added boundary and removal of only a chosen default divider.
- Single-screen default fits the complete body onto one screen; blank written lines are paragraph spacing. Its first custom break creates exactly two fitted screens, adding no two-line cadence. Later clicks add or remove only the chosen boundary. Its custom boundaries may cross blank paragraph spacing, as in Spec 070.
- Clicking a gap or existing break in Preview is the only way to enter Custom. The icon-only middle segment indicates that state and cannot be clicked or keyboard-activated to enter it.
- While a default is active, choosing the other default changes the stored default and projector output immediately, without confirmation. The custom break list remains null.
- While Custom is active, choosing either default opens a confirmation naming the target mode and explaining that custom breaks will be removed. Cancel leaves mode and breaks untouched. Confirm atomically saves the target default and null breaks. This confirmation applies even if the custom list is empty.
- A saved gap click changes only the break list; it does not change the stored default mode. The selected default is therefore retained behind Custom until the editor explicitly chooses another default.
- Editing Title or Text does not offer a mode control. It retains the default mode; changing the line shape resets custom breaks under the existing rule and shows the existing Preview notice.
- A mode or break change succeeds only for an authorized editor. The server validates the default value, boundary positions for that default, and the text and screen state the Preview was opened with. Stale writes return a conflict without changing the entry. Anonymous Preview remains readable.
- Migrating existing Text rows preserves Multi-line mode; migrating existing Single-screen Text rows preserves Single-screen mode. Both become the same active Text kind with unchanged IDs, order, title, body, custom breaks, and projector screens. New rows use only that Text kind.
- A successful mode or break save refreshes the open reading page and projector through the existing live-edit path. Each Text entry still ends with its current built-in blank projector screen.

## UI details

- **Visual reference:** [Revised Create/Edit forms](./preview-form-light.png), [light Preview footer](./preview-footer-light.png), and [dark Preview footer](./preview-footer-dark.png).
- **Create form:** Keep the existing modal title, Title, Text, Save, and Cancel geometry. Center a two-way segmented control beneath “New text”: up to 308px wide and 42px high, 3px outer padding, 9px outer radius, and two 36px-high options. Each option pairs a 15–17px icon with a 13px label, “Multi-line” or “Single-screen”. New entries start on Multi-line. A centered 12px helper line 14px below the control reads “Two lines per screen by default” or “One fitted screen by default”. Use one Add Text action in each add row and empty-service state.
- **Edit form:** Show “Edit text”, Title, Text, Save, and Cancel. There is no default-mode switch, custom indicator, or break-loss confirmation in this form.
- **Preview footer:** Keep the existing sticky footer, its 12px by 22px padding, and the current dialog width of min(44rem, 100vw - 32px). Replace both Reset breaks and the “Screen breaks” badge with one centered segmented control, at most 363px wide and 42px high with 3px inner padding and 9px radius. Left and right are icon-labeled 36px-high buttons; the middle is a 53px-wide icon-only status segment with the accessible name and hover/focus tooltip “Custom breaks”. Use the stacked-lines, screen-break, and framed-screen icons from the mockups.
- **Colors / typography:** Use --rail-bg for the control track, --divider for its 1px outline, --active-bg and --active-ink for the selected segment, --head-ink for unselected text/icons, and the current 13px sans-serif labels. Keep existing neutral default break lines, stronger Custom break lines, accent dotted Add break hover, danger Remove break hover, and serif Preview text. The light accent is #1C5C3C and dark accent is #7C9CF0.
- **States:** Default buttons expose their selected state to assistive technology and have a 2px --focus keyboard outline. The middle Custom segment is non-interactive; its tooltip describes the state and never offers an action. Disable writes while a save is pending. For viewers, show the current mode in the same footer without editable buttons or break controls.
- **Confirmation:** Overlay Preview with a centered dialog up to 468px wide, 12px radius, title “Switch to Multi-line?” or “Switch to Single-screen?”, message “Your custom screen breaks will be removed.”, and “Keep custom” and “Switch & remove” buttons. Keep custom and Escape cancel. Focus enters the confirmation, stays within it, then returns to the selected default button after dismissal.
- **Responsive behavior:** At narrow widths, the footer control takes the available width and keeps all three segments on one line; below 420px use 12px footer side padding and labels no smaller than 12px. The confirmation fits within the viewport with at least 16px on each side. Preview text still scrolls under its fixed footer.
- **Motion:** Use the existing 200ms design-token ease for the selected thumb. Remove the transition under reduced motion. Break-line and projector transitions keep their current behavior.

## Acceptance scenarios

### Scenario: Existing rows retain their screens

- **Given** existing ordinary and Single-screen Text entries, each with or without custom breaks
- **When** the migration runs
- **Then** every row keeps its ID, service order, words, default behavior, saved custom breaks, and sequence of projector screens, while both use the active Text kind.

### Scenario: Create one Text kind

- **Given** the editor opens Add Text
- **When** they leave Multi-line selected or choose Single-screen and save
- **Then** the entry stores the chosen default on one Text kind, and its projector starts with paired lines or one fitted screen respectively.

### Scenario: Edit only the words

- **Given** an entry has either default or Custom
- **When** its Edit modal opens and the editor saves Title or Text
- **Then** the form has no mode switch and keeps the saved default; an altered line shape resets custom breaks with the existing notice.

### Scenario: Switch defaults in Preview

- **Given** a Text entry is using Multi-line or Single-screen default
- **When** the editor selects the other default in the Preview footer
- **Then** no confirmation appears, the selected segment and saved mode change, and an open projector refreshes to the new grouping.

### Scenario: Enter Custom from a line gap

- **Given** the entry uses a default mode
- **When** the editor adds or removes a break between written lines
- **Then** the middle Custom segment selects itself without being directly activatable; Multi-line follows Spec 069’s first-action cadence and Single-screen adds only the chosen first break.

### Scenario: Leave Custom deliberately

- **Given** the entry has a custom break list, including an empty list
- **When** the editor clicks Multi-line or Single-screen
- **Then** the confirmation names that target mode; “Keep custom” preserves the arrangement, while “Switch & remove” clears it and projects the selected default.

### Scenario: Permissions and stale state

- **Given** a viewer opens Preview, or an editor has a Preview whose text or screen state has since changed elsewhere
- **When** they attempt to change mode or breaks
- **Then** viewers have no editable control, and stale editor writes fail without overwriting the newer state.

## Traceability

- Domain and migration tests: `multimedia/tatib/tests.py`.
- Application and projector tests: `multimedia/web/tests.py`.
- Browser acceptance: `tests/e2e/test_unified_text_screen_mode.py`, with the existing Text break browser suites updated for the new footer.
- Implementation: `multimedia/tatib/models.py`, `multimedia/tatib/migrations/0009_unify_text_screen_modes.py`, `multimedia/web/reading/entries.py`, `multimedia/web/reading/views.py`, the reading templates, `static/web/preview.js`, `static/web/entries.js`, and `static/styles/design/components.css`.
- Shared editor picker anchoring: `static/web/entries.js` follows the dialog during its post-scroll centering; `tests/e2e/test_entry_pickers.py` verifies the existing anchored-menu behavior.
