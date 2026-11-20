# Feature Specification: a clicked service keeps its date

**Slice**: `specs/201-sidebar-date-focus`
**Branch**: `fix/201-sidebar-date-focus`
**Created**: 2026-11-19
**Status**: Accepted (Gate 1, 2026-11-19)
**Input**: the owner's report, 2026-11-19 — "when you click on the service on the service sidebar, its date wont show up even if you dont hover it anymore. only show up again if you click somewhere else"

The date-hide rule came in with spec 190 (FR-004) as part of the row-action reveal, and spec 195
added the Today badge to the same two selectors. The reveal's own controls deliberately avoid
`li:focus-within` (the comment at `components.css:484-486` records why); this slice brings the date
and badge onto the same rule, because a click on the row's link is not a reveal.

## User Scenarios & Testing

### US1 — A clicked service keeps its date after the pointer leaves (P1)

**Why this priority**: the date is the operator's way to tell which service a row is; after a click
it vanishes for as long as the row holds focus, with no action controls up to explain the absence.
The only way to get it back is to click somewhere else — which can navigate away or close a pane.

**Independent Test**: on the Tata Ibadah sidebar, click a dated service row, move the pointer to a
neutral part of the page, and read the row's date: today it is `display: none`; after the fix it is
`block` with the same text and box as before the click. Clicking elsewhere still leaves it `block`.

**Acceptance scenarios**

1. **Given** a dated service row at rest **When** its date is inspected **Then** it is painted with
   the base commit's type and ink, and the row's accessible name still carries it.
2. **Given** the row is hovered **When** the edit and delete controls are revealed **Then** the date
   is not painted, exactly as today.
3. **Given** the row's link is clicked **When** the pointer leaves the row **Then** the date paints
   again, and the row's controls are hidden — there is no reveal to justify hiding it.
4. **Given** a click elsewhere **When** focus leaves the row **Then** the date still paints; the
   fix must not change the already-working blur path.
5. **Given** a keyboard user tabs onto the row's link **When** the link has focus **Then** the date
   paints, because no action control is revealed.
6. **Given** a keyboard user tabs onto the row's pencil or trash **When** that control is
   focus-visible **Then** the date is not painted for exactly as long as the control is revealed, and
   paints again when focus moves away.

### US2 — The Today badge follows the same reveal as the date (P2)

**Why this priority**: spec 195 deliberately tied the badge to "the way the row's date is"; fixing
only the date would leave the Today row's badge stuck hidden after the same click, so the two
trailing-edge marks would disagree.

**Independent Test**: click a service row dated today, move the pointer away; the badge paints
again while its accessible name still ends `— today`, and it still steps aside on hover and on
action-button focus.

**Acceptance scenarios**

1. **Given** a Today row at rest **When** inspected **Then** the badge paints with its accepted
   accent fill and ink.
2. **Given** the row's link is clicked **When** the pointer leaves **Then** the badge paints again.
3. **Given** the row is hovered or its pencil/trash is focus-visible **When** the reveal is up
   **Then** the badge is not painted, unchanged from spec 195.

### Edge Cases

- **When** the pointer stays on the row after the click **Then** the hover reveal still holds and
  the date and badge stay hidden — the fix changes focus, not hover.
- **When** the row has no edit/delete controls (editing disabled) **Then** nothing hides the date
  on link focus; the visible behaviour is unchanged at rest and on hover.
- **When** a touch device has no hover **Then** the existing `@media (hover: none)` rules keep the
  controls drawn and the date/badge visible; this slice does not move those rules.
- **When** a modal closes and focus is restored quietly to a row action **Then** the control is
  still revealed, so the date and badge remain hidden until focus actually leaves the row.
- **When** a row's name is long enough to meet the controls **Then** the existing reserved padding
  on action rows is untouched; this slice changes only `display`, never geometry.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | On a hover-capable pointer, a dated Tata Ibadah service row SHALL not paint its displayed date while the row is hovered or while its own edit/delete control is focus-visible; the date SHALL paint in every other state, including when the row's link holds focus. | `reading/R41` (modified) |
| FR-002 | The Today badge SHALL follow the same reveal as the date: hidden on row hover or action-control focus-visible, painted otherwise, including when the row's link holds focus. | `reading/R9` (modified) |
| FR-003 | The rule changes SHALL be scoped to the action reveal and SHALL NOT change the `@media (hover: hover)` guard, the touch/`hover: none` rules, the row's accessible label, or any row geometry. | `reading/R41`, `reading/R9` |
| FR-004 | The date and badge SHALL remain present in the DOM and in the row's `aria-label` in every state — the rule hides painting only. | `reading/R41`, `reading/R9` |

### Key Entities

- **Sidebar service row** — the `<li data-editor-kind>` carrying the `.book` link, its `.book__n`
  name, optional `.book__today` badge, optional `.book__s` date, and the `.row-edit` / `.row-delete`
  action buttons; the reveal state is the row's hover or an action button's `:focus-visible`.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | After a click on a service row and the pointer leaving it, the row's date is painted again. | Playwright E2E: computed `display` of `.book__s` is `block`, with `li:focus-within` true. |
| SC-002 | Hover and keyboard action focus still hide the date and the Today badge. | Playwright E2E: computed `display` is `none` in both reveals, `block` after focus leaves. |
| SC-003 | No row geometry or accessible name moves. | E2E reads the row's box height and `aria-label` before and after the state changes; identical values. |

## UI/UX

Static preview at `specs/201-sidebar-date-focus/preview/index.html` (real sidebar group captured
from the running app, base commit's own `tokens.css` and `components.css`; the two candidate rule
blocks are the only difference between the panels). `preview/probe.py` asserts all four states in
both panels; its measured values are the ones below.

- **Layout / position**: the captured row is 38.0px tall in the 400px preview panel; only `display`
  changes between states, so the row's box, the name's line and the controls' positions are the same
  in all four.
- **Size / spacing**: date `font-size: 12.5px`, `line-height: 22px`, `color: var(--head-ink)`.
- **Colour / typography**: unchanged — the date and badge keep every base-commit declaration.
- **States**: at rest `display: block` (both panels); hover `display: none` (both); link clicked and
  pointer away — today `display: none`, proposal `display: block`; click elsewhere `display: block`
  (both). `li:focus-within` is `true` in the clicked state and `false` in the other three, which is
  the whole defect.
- **Motion**: none added; no transition on the date's `display`.
- **Responsive**: the change stays inside `@media (hover: hover)`; touch/`hover: none` rows keep
  their always-drawn controls and painted date.

## Assumptions

- The row's link receiving focus after a click is the state the report describes — confirmed by
  the live reproduction, where `li:focus-within` stayed true after the pointer left.
- "Focused for action reveal" in `reading/R41` and spec 195 means the edit/delete buttons, matching
  the reveal selectors already used for those buttons; the link itself is not an action reveal.
- The Today badge is in scope because spec 195 tied it to the date's reveal; the fix covers both
  selectors in the same rule.
- No server, template or script change is needed: the failure is a CSS selector, and the markup
  already keeps the date in `aria-label`.

## Clarifications

### Session 2026-11-19

- No open questions: the report, the live reproduction and the existing control-reveal selectors
  settle every state named above.
