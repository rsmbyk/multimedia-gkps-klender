# Spec 074: Drag service entries from the whole sidebar row

- **ID:** 074
- **Status:** Accepted
- **Item:** ITEM-077
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

Make service-entry reordering easy to start from anywhere on its sidebar row while preserving row navigation and keyboard reordering.

## Scope

### In scope

- Every movable ServiceEntry row in the Tata Ibadah contents sidebar, including section breaks.
- Pointer drag on the row, the visible grip cue, keyboard movement from that grip, and click-versus-drag behavior.

### Out of scope

- Legacy non-entry rows, Bible and song lists, the save API, and reading-stage drag behavior.

## Domain rules

- A primary mouse or pen press on a movable row's number, text, empty row area, or grip may start the existing reorder gesture after more than 3px of movement.
- On touch, keep the existing grip-only drag target so a vertical swipe on row text can scroll the sidebar. The grip remains a button for keyboard ArrowUp/ArrowDown reordering.
- Release before the threshold is a click: a text-row click still jumps to the corresponding stage entry. After a completed drag, consume the following click so it cannot jump or flash.
- Drop persists the same order immediately through the existing endpoint. Cancel, pointer loss, or failed save follows the existing rollback and status behavior.
- Only rows backed by ServiceEntry IDs are movable. Section-break rows use their whole visible divider row as the pointer target.

## UI details

- **Approved preview:** [Sidebar follow-ups interactive preview](../072-sidebar-idle-collapse/preview.html), “Tata Ibadah” scenario.
- **Size / position:** Retain current row height, 9px corners, number/text spacing, and grip placement at the right edge. No additional handle or control appears.
- **Colors / typography:** Keep existing resting, hover, selected, drag ghost, and drop-target tokens.
- **States:** The entire movable row shows `cursor: grab` for mouse/pen hover and `cursor: grabbing` while dragged. The six-dot grip remains visible at rest. Keyboard focus stays on the grip button or the link according to the existing focus path.
- **Responsive behavior:** The row remains a click target on narrow screens; touch text swipes scroll and the grip remains the reorder control.
- **Motion:** Keep existing reorder transition and respect reduced-motion behavior.

## Acceptance scenarios

### Scenario: Drag from the row

- **Given** two or more movable service entries
- **When** the operator drags one from its title, number, blank area, or grip and drops it elsewhere
- **Then** the same ghost/drop feedback appears and the new order is saved once.

### Scenario: Click versus drag

- **Given** a movable row
- **When** the operator clicks without crossing the drag threshold
- **Then** the row quicklink jumps to its stage entry; a completed drag causes no quicklink activation.

### Scenario: Keyboard and touch

- **Given** a movable row and a visible grip
- **When** the operator uses ArrowUp/ArrowDown on the grip or drags it by touch
- **Then** the existing reorder behavior remains available, while a touch swipe on the row body scrolls the sidebar.

### Scenario: Nonmovable rows

- **Given** a legacy row without a ServiceEntry ID
- **When** the operator presses or clicks it
- **Then** it cannot be dragged and keeps its normal quicklink behavior.

## Traceability

- E2E: `tests/e2e/test_reorder.py` covers drags from the row number, title, blank row area, grip, and section-break divider; short-click activation; cancel rollback; touch pointer pass-through; immediate save; keyboard movement; and legacy rows.
- Implementation: `multimedia/web/templates/reading/_toc.html` marks movable rows and prevents native link dragging; `static/web/reorder.js` owns pointer capture, short-click replay, drag suppression, and whole-row targeting; `static/styles/design/components.css` shows the grab/grabbing cursors while retaining the grip cue.
