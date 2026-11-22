# Feature Specification: Keep Add song when the songbooks sidebar is closed

**Slice**: `specs/222-add-song-parent-closed`
**Branch**: `fix/222-add-song-parent-closed`
**Created**: 2026-11-22
**Status**: Accepted (Gate 1 2026-11-22)
**Input**: "when you close only the songbooks sidebar while the songs sidebar is open, the 'Add song' button disappear"
**Demand**: `ITEM-237`
**Capability**: adds `reading/R51`

## User Scenarios & Testing

### US1 — The songs list keeps its add control when its parent is closed (P1)

**Why this priority**: a reader can collapse the songbooks sidebar to give the songs list more
room. The list is still on screen and usable, but the button for adding a song to the open
songbook is not — the workflow stops for a CSS state, not for a data rule.

**Independent Test**: in a browser at 1440×900, open a reading page, open Kidung, open a real
(not hymn) songbook, click the first sidebar's collapse control, then check that `#songAdd` is
still visible and clicking it opens the "New song" editor. Compare with the first sidebar's
`#panelAdd`, which must still be hidden.

**Acceptance scenarios**

1. **Given** a Kidung reading page with both sidebars open and a real songbook selected **When**
   the songbooks sidebar is collapsed with its own collapse control **Then** `data-nav="closed"`,
   `data-ch="open"`, and `#songAdd` remains visible at its existing size and position.
2. **Given** the state in scenario 1 **When** `#songAdd` is clicked **Then** the same song editor
   opens with that songbook preselected, exactly as it does with both sidebars open.
3. **Given** a Kidung reading page with a real songbook selected **When** the first sidebar is
   mini instead of closed while the songs list is open **Then** `#songAdd` is visible.
4. **Given** the songbooks sidebar is collapsed or mini **When** the songs list itself is closed
   **Then** no add control is visible: the songs sidebar is not painted.
5. **Given** a collapsed or mini songbooks sidebar **When** the first sidebar's own add control is
   checked **Then** `#panelAdd` stays hidden — the fix is scoped to the second sidebar.
6. **Given** a hymn songbook **When** its songs list is open and the first sidebar is collapsed
   **Then** no `Add song` control is rendered at all, as before.

### Edge Cases

- At the below-1272px drawer breakpoint the lower level covers its parent; closing only the
  parent must not put a live control behind the visible sheet.
- At the phone toolbar breakpoint the same rule applies: the add control follows the visible
  songs list, not the hidden parent.
- A disabled `Add song` (no songbook selected) stays disabled and visible when the parent is
  closed; the change is about visibility, not enablement.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The rule that hides add controls for a mini or closed first sidebar SHALL apply only to controls inside the first sidebar (`.panel`). It SHALL NOT match the second-level song list's `.ch__add .editor-add`. | `new: reading/R51` |
| FR-002 | With `data-nav="closed"` or `data-nav="mini"` and `data-ch="open"`, the songs list's `Add song` button SHALL have the same computed display, box and behaviour it has with `data-nav="open"`. | `reading/R51` |
| FR-003 | The first sidebar's `Add songbook` and `Add Tata Ibadah` controls SHALL remain hidden whenever that sidebar is mini or closed. | `reading/R51` |
| FR-004 | When the songs list is closed, or on a section where the second-level add control is not rendered, no add control SHALL become visible through this change. | `reading/R51` |
| FR-005 | The editor dialog, its form, permissions, hymn-book read-only behaviour, and the disabled no-songbook state SHALL be unchanged. | `reading/R51` |

### Key Entities

None. The change is a CSS selector boundary over existing controls.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Collapsing only the songbooks sidebar leaves `Add song` visible with its original 38px height. | Playwright E2E: `#panelCollapse.click()` from `data-nav="open"`, `data-ch="open"`; assert `getComputedStyle(#songAdd).display === 'flex'` and its rect height is 38px. |
| SC-002 | The restored control still opens the song editor for the current songbook. | Playwright E2E: click `#songAdd` in that state; `dialog[open]` and `#editorTitle` read "New song". |
| SC-003 | The first sidebar's own add control stays hidden. | Playwright E2E: in the same state assert `#panelAdd` has `display: none`. |
| SC-004 | No add control appears when the songs list is closed. | Playwright E2E: close the songs list after the parent; assert no visible `.editor-add`. |
| SC-005 | The rule holds through the drawer and phone breakpoints. | Playwright E2E at 1440×900, 1000×800 and 390×844: with the songs list visible and the parent collapsed, `#songAdd` is visible. |

## UI/UX

`static preview at specs/222-add-song-parent-closed/preview/index.html` — the real reading-shell
markup and stylesheets, with buttons to close only the parent sidebar and to compare the current
and proposed CSS.

- **Before**: `data-nav="open"`, `data-ch="open"` — `#songAdd` computes `display: flex`, 38px tall.
  Click "Close songbooks only": `data-nav="closed"`, `data-ch="open"`, `#chapters` still visible,
  but `#songAdd` computes `display: none` with a 0×0 box.
- **After**: the same clicks leave `#songAdd` at `display: flex`, 38px tall, unchanged 12px
  horizontal inset inside `.ch__add`, 15px icon, 13.5px/1 label; `#panelAdd` still `display: none`.
- **States**: parent open / mini / closed; songs list open / closed; hymn book (no control
  rendered); disabled no-songbook control; 1440×900 desktop, 1000×800 drawer, 390×844 phone.
- **Motion**: none added or removed; the sidebars keep their existing transforms.
- **Colour / typography**: unchanged; no new token, colour or font.

## Assumptions

- "Close only the songbooks sidebar" means the first sidebar's collapse control while the
  second-level songs list stays open (`data-nav="closed"`, `data-ch="open"`); measured on the local
  reading page at 1440×900 on 2026-11-22.
- The hidden button is a CSS rule, not a server condition: the node stays in the DOM with its
  `data-editor-book` intact, so no fetch or template change is involved.
- The same hide rule covers `data-nav="mini"`, so a mini parent with a visible songs list gets the
  same fix; a state the report did not name but that shares the exact root cause.
- Add controls on the search landing and on other sidebar kinds are outside this change.
- No `[NEEDS CLARIFICATION]` markers remain.
