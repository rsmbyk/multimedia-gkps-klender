# Feature Specification: Match the Tata Ibadah date header to the songbook header

**Slice**: `specs/123-tatib-date-header-parity`
**Branch**: `fix/123-tatib-date-header-parity`
**Created**: 2026-10-24
**Status**: Accepted (owner, gate 1, 2026-10-24)
**Input**: "the dates in service page (image 1) should have the same style as the songbook name header (image 2)"

## User Scenarios & Testing

### US1 — A service page leads with the same header as a song page (P1)

**Why this priority**: The date is the first thing on a service page and it currently reads as a different
element from every other reading page's header; the operator recognises a page by that header.
**Independent Test**: Open a dated service and a song side by side and compare the eyebrow above each
title — size, weight, tracking, colour, and height must agree.

**Acceptance scenarios**

1. **Given** a service dated 25 Oktober 2026 **When** I open its Tata Ibadah page **Then** the date above
   the title is 16.5px / weight 600 / .12em tracking / ink at .78 opacity, and measures the same as the
   Kidung page's songbook header
2. **Given** the same page **When** the Project action is beside the date **Then** both sit on one row,
   vertically centred with each other, the date left of the action
3. **Given** an undated service **When** I open it **Then** its `Tata Ibadah` label carries the same style

### US2 — The header degrades without losing the date (P2)

**Why this priority**: The row now holds a taller date; at a narrow stage it must not clip or shrink it.
**Independent Test**: Squeeze the stage below the width that holds both items and check the date is
complete, uncut, and the page does not scroll sideways.

**Acceptance scenarios**

1. **Given** a stage too narrow for the date and the Project action together **When** the page renders
   **Then** the Project action wraps beneath the date, which keeps its full size and is never clipped, and
   the page does not scroll sideways

### US3 — Saved service pages match the live ones (P3)

**Why this priority**: A service opened from the saved library renders through the same classes, so a
style that only reached the server page would split the two views.
**Independent Test**: Open the same service online and from the saved library and compare the eyebrow.

**Acceptance scenarios**

1. **Given** the saved library **When** I open a dated service from the Tata Ibadah panel **Then** the
   date eyebrow carries the same style as the server page

### Edge Cases

- **When** the service has no date **Then** its `Tata Ibadah` label uses the same style (the label, not
  the size, is what differs).
- **When** the date is longer than the sample (`30 September 2026`) **Then** the header reflows by the
  same rule — the row needs the date's own width, not a fixed one.
- **When** a Bible, Kidung, or Media Library page renders **Then** its eyebrow is unchanged; the change is
  scoped to the service page.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A dated service page's date eyebrow SHALL use the shared reading eyebrow typography — 16.5px, weight 600, line-height 1.65, letter-spacing .12em, uppercase, ink at .78 opacity — so it is indistinguishable from the Kidung page's songbook header | `new: reading header` |
| FR-002 | The date and the Project action SHALL share one row and stay vertically centred with each other while they fit, with the date left of the action | `new: reading header` |
| FR-003 | When the row cannot hold both items, the date SHALL keep the FR-001 typography and stay unclipped, the Project action SHALL wrap beneath it, and the page SHALL NOT scroll horizontally | `new: reading header` |
| FR-004 | The saved/offline render of the same service SHALL carry the same eyebrow style | `new: reading header` |
| FR-005 | The Bible, Kidung, and Media Library eyebrows SHALL keep their current computed style | `new: reading header` |
| FR-006 | The eyebrow's text, its `margin-bottom: 0` inside a service head, and the Project / update / transfer controls SHALL be unchanged | `new: reading header` |

### Key Entities

None — the change touches no model, view, endpoint, or payload; it is a stylesheet rule scoped to the
service page's header.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The service date and the songbook header are indistinguishable | Computed `font-size`, `letter-spacing`, `line-height`, `font-weight`, and colour equal on the running pages |
| SC-002 | The header row still holds both items where it does today | `.read__head-top` height 34px and date/button centre delta ≤ 1px at 1440px and 390px window widths |
| SC-003 | A narrow stage loses neither the date nor the layout | No horizontal document overflow from 1542px down to 1180px; the date's rendered box equals its full text width |
| SC-004 | No other reading page changes | Bible and Kidung eyebrows' computed values identical before and after |

## UI/UX

Frozen from the preview (`preview/README.md`): the running app from this branch, a dated service opened by
click from `/` → **Tata Ibadah** → the 25 Oktober 2026 service, against `/songs/1351/` as the reference.

| Window / stage | Header row | Row height | Date box | Centre delta | Page overflow |
| --- | --- | --- | --- | --- | --- |
| 1440px, both sidebars open | 400px | 34px (one row) | 171 × 27px | 0.00px | 0px |
| 1280px, both sidebars open | 240px | 69px (wrapped) | 171 × 27px | Project sits 38.61px below | 0px |
| 390px, mobile shell, opened from the panel | 290px | 34px (one row) | 171 × 27px | 0.00px | 0px |
| undated template service | 400px | 34px (one row) | 127 × 27px (`Tata Ibadah`) | 0.00px | 0px |

- **Layout / position**: the eyebrow is the first item of `.read__head-top`, sharing the row with the
  Project action; `margin-bottom: 0` so its box centres with the 34px button.
- **Size / spacing**: 16.5px / 1.65 (27.225px) / weight 600 / .12em (1.98px); the date `25 Oktober 2026`
  measures 171 × 27px, against 108 × 18px today. One row needs 171 + 12 (gap) + 88 (button) = 271px of
  header width; wrapped rows use an 8px gap and grow the row from 34px to 69px.
- **Colour / typography**: ink `#1f1f1d` at opacity .78, uppercase, the app's sans stack — identical to
  `/songs/1351/` (both measured `rgb(31, 31, 29)` at `.78`).
- **States**: hover · focus · active · disabled · empty · error · loading — none; the date is static text.
- **Motion**: none.
- **Responsive**: the `≤600px` `.read__project { max-width: 100% }` rule stays; the wrap rule applies at
  every width, so the header reflows by comparing the date's own width with the row, not by a breakpoint.

## Assumptions

- The reference is the Kidung page's eyebrow — the songbook name above the song title — because it renders
  through the shared `.read__eyebrow` rule that every reading page uses.
- This slice reverses the 11px / .08em override that Spec 112 added to the same selector for its header row;
  nothing else from Spec 112 changes.
- Spec 102's recorded eyebrow values (16.5px, weight 600, .12em, .78 ink, `margin-bottom: 0` inside a
  service head) are the target, not a new look.
- The saved/offline renderer needs no code change, because it writes the same classes.

## Clarifications

### Session 2026-10-24

- Q: When the stage is too narrow for the date and the Project action on one row, does the Project action
  wrap beneath the date, or should the date step down in size to keep one row? → A: the Project action
  wraps beneath the date; the date keeps its full size (owner, 2026-10-24)
