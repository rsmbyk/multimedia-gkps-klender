# Spec 072: Collapse an idle matching sidebar

- **ID:** 072
- **Status:** Accepted
- **Item:** ITEM-075
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

Recover reading space after the operator leaves the sidebar idle, while preserving deliberate browsing of another section.

## Scope

### In scope

- Main icon rail and first sidebar in the new reading shell.
- A 60-second inactivity interval, as shown by the accepted preview's “Simulate 60s idle” action.
- Existing Bible mini-panel state and existing Kidung/Tata Ibadah first-panel collapse behavior.

### Out of scope

- Second sidebar content, the reading stage, global search results, and legacy docks/webs.
- A new persistent timeout setting or a notification about auto-collapse.

## Domain rules

- Start or reset the idle interval while the first panel is open. Pointer use, keyboard use, focus changes, or scrolling in the main rail or first panel counts as activity.
- On expiry, collapse only if the first panel's section matches the section of the page currently shown on the reading stage. A landing/search page or a sidebar showing a different section is ineligible.
- Defer collapse while a control inside the panel has focus, a modal is open, or a drag gesture is underway; restart the interval when that interaction ends.
- For Alkitab, set the first panel to its existing mini state. For Kidung and Tata Ibadah, use the current manual collapse state. Do not navigate the reading page.
- Opening a panel again starts a fresh interval. A timer from a previous section or closed panel cannot affect the new state.

## UI details

- **Approved preview:** [Sidebar follow-ups interactive preview](./preview.html), “Simulate 60s idle” scenario.
- **Size / position:** Reuse current rail and panel widths, collapse control placement, and section-specific mini/closed dimensions. No new control.
- **Colors / typography:** Preserve current light/dark tokens and selected rail icon.
- **States:** The first panel remains visually unchanged during the 60-second wait. At expiry it takes the same state as its existing manual collapse action; focus is moved to the owning rail button if needed.
- **Responsive behavior:** Apply only where the first panel can remain open alongside the stage. Keep the existing narrow-screen panel behavior.
- **Motion:** Use the existing panel transition and reduced-motion handling.

## Acceptance scenarios

### Scenario: Idle on the currently read section

- **Given** an open first sidebar for the same section as the reading stage
- **When** 60 seconds pass without rail or first-panel activity and no control is in active use
- **Then** the sidebar collapses using that section's existing manual state, with Alkitab in mini mode and the reading page unchanged.

### Scenario: Activity and active controls

- **Given** an eligible open sidebar
- **When** the operator interacts with the rail or first panel before expiry, or is using a focused control, modal, or drag gesture
- **Then** the sidebar does not close during that interaction and a fresh idle interval follows it.

### Scenario: Browsing a different section

- **Given** the stage displays one section while the first sidebar lists another
- **When** the interval expires
- **Then** the sidebar stays open.

### Scenario: Reopen

- **Given** a sidebar collapsed by inactivity
- **When** the operator opens it through the rail
- **Then** it opens normally with a fresh interval and the current reading page is still shown.

## Traceability

- Domain/app tests: N/A.
- E2E: `tests/e2e/test_reading.py` uses Playwright's fake clock to cover Bible mini mode, Tata Ibadah close mode, rail activity reset, focused-filter/modal/drag deferral, mismatched section, and narrow layout.
- Implementation: planned `static/web/reading.js`; existing panel styles in `static/styles/design/components.css`.
