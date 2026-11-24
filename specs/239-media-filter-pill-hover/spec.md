# Feature Specification: hover feedback on Media Library filter pills

**Slice**: `specs/239-media-filter-pill-hover`
**Branch**: `feat/239-media-filter-pill-hover`
**Created**: 2026-11-24
**Status**: Accepted
**Input**: "can you add hover effects to media library page's filter pills?"
**Demand**: `ITEM-254` (new card)
**Capability**: `media-library/R6` (new)
**Preview**: live preview at `http://127.0.0.1:8767/media-library/` — open `/`, click the Media Library rail. If the server is down, run `DJANGO_DEVELOPMENT_MODE=true ../multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8767 --noreload` from `~/Projects/multimedia-gkps-klender-239`.

The Media Library's six filter pills — Images, Audio, Video, PDF, Slides and
Unused — are the only controls in the filter row with no hover treatment: the
adjacent sort button and the head icon buttons already take `--focus` border and
`--icon-hover-bg` fill on hover (`static/styles/design/components.css:607`), and
the same pair is the app's chip hover in `obs-dock.css:769`. This slice gives the
unpressed filter pills that same pair so the row reads consistently. A pressed
pill keeps its accent fill: hover must not make a selected filter look unselected.

## User Scenarios & Testing

### US1 — An unpressed pill answers the pointer (P1)

**Why this priority**: this is the reported surface. Without a hover change the
pills give no pre-click affordance, while the button immediately beside them
changes on hover.

**Independent Test**: on the live page, measure the Images pill at rest and under
a real mouse hover in light and dark themes; the border and fill change, the box
and label do not.

**Acceptance scenarios**

1. **Given** the Media Library page with no filter selected **When** the pointer
   moves over the Images, Audio, Video, PDF, Slides or Unused pill **Then** that
   pill's border reads `--focus` and its fill reads `--icon-hover-bg`.
2. **Given** the same pill in either theme **When** the pointer leaves it **Then**
   it returns to the transparent fill and `--divider` border it had at rest.
3. **Given** the pointer on one pill **When** it is measured **Then** its width,
   height, label colour and text are unchanged from rest.

### US2 — Selected state, focus and layout stay as they were (P2)

**Why this priority**: the pressed fill is how the operator sees which filter is
active; a competing hover tone would make the filter row ambiguous.

**Independent Test**: click Images, then hover the pill; read the same three
computed colours as at rest and confirm they are identical, and confirm the
existing `:focus-visible` outline still appears on keyboard focus.

**Acceptance scenarios**

1. **Given** a pressed pill **When** it is hovered **Then** its background,
   border and text colour are the same as when it is not hovered.
2. **Given** a pill reached by Tab **When** it has focus-visible **Then** the
   existing 2px `--focus` outline with 2px offset is still painted.
3. **Given** a pill at rest, hovered or pressed **When** its box is measured
   **Then** it is 63.36 × 30 px at 1440px and the filter row's gaps do not move.

### Edge Cases

- The centred dot between Slides and Unused is a `span`, not a button; it has no
  hover rule and stays `--head-ink`.
- The rule is a plain `:hover` selector, not wrapped in `@media (hover: hover)`;
  the machine's Playwright Chromium reports that media feature as false on a
  localhost origin, so a wrapper would make the shipped rule untestable there.
- No transition is added: the hover is a direct colour swap, matching the sort
  and icon buttons. Reduced-motion mode has nothing to suppress.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | Every unpressed `.media-library__chips button` SHALL take `border-color: var(--focus)` and `background: var(--icon-hover-bg)` while hovered. | `media-library/R6` |
| FR-002 | A pill with `aria-pressed="true"` SHALL keep its `--active-bg` fill, `--active-ink` text and matching border while hovered. | `media-library/R6` |
| FR-003 | The rule SHALL change only border and background; pill geometry, label, filter behaviour, focus-visible outline and the separator dot SHALL NOT change. | `media-library/R6` |
| FR-004 | No surface outside the Media Library's filter pills SHALL change. | `media-library/R6` |

### Key Entities

- **`.media-library__chips`** — the `role="group"` filter row in
  `multimedia/web/templates/reading/media_library.html`, holding five
  `[data-media-type]` buttons, the dot span and `#mediaUnusedFilter`.
- **`--focus` / `--icon-hover-bg`** — the existing theme tokens that carry the
  app's control-hover pair in both light and dark themes.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Unpressed pill hover changes border and fill | computed border/background at rest and after `locator.hover()`, in both themes |
| SC-002 | Pressed pill hover changes nothing | computed border/background/colour before and after hover on a clicked pill |
| SC-003 | Nothing else moves | pill box 63.36 × 30 px, label colour and filter-row gaps unchanged across all three states |
| SC-004 | Both themes agree | the same readouts under `color_scheme: light` and `dark` at 1440 × 900 |

## UI/UX

Live preview at `http://127.0.0.1:8767/media-library/`, 1440 × 900,
`device_scale_factor: 1`, both themes. "Before" is the same shipped page with
only the new rule deleted from the stylesheet in that page's CSSOM; the live
URL itself carries the rule. Probe: `specs/239-media-filter-pill-hover/preview/probe.py`.

| Pill / state | Background | Border | Text | Box |
| --- | --- | --- | --- | --- |
| Unpressed, rest — light | `rgba(0, 0, 0, 0)` | `rgb(217, 214, 205)` | `rgb(31, 31, 29)` | 63.36 × 30 px |
| Unpressed, hovered — light | `rgba(31, 31, 29, 0.08)` | `rgb(28, 92, 60)` | `rgb(31, 31, 29)` | 63.36 × 30 px |
| Unpressed, rest — dark | `rgba(0, 0, 0, 0)` | `rgb(58, 54, 47)` | `rgb(245, 243, 238)` | 63.36 × 30 px |
| Unpressed, hovered — dark | `rgba(255, 255, 255, 0.09)` | `rgb(124, 156, 240)` | `rgb(245, 243, 238)` | 63.36 × 30 px |
| Pressed, rest — light | `rgb(28, 92, 60)` | `rgb(28, 92, 60)` | `rgb(255, 255, 255)` | 63.36 × 30 px |
| Pressed, hovered — light | `rgb(28, 92, 60)` | `rgb(28, 92, 60)` | `rgb(255, 255, 255)` | 63.36 × 30 px |

States are reachable by hand: hover by pointing at any of the six pills, rest by
moving the pointer away, pressed by clicking a pill, focus-visible by Tabbing,
and both themes by the theme control. No animation or transition is added.
Responsive wrapping of the filter row is untouched.

## Assumptions

- The hover applies only to unpressed pills; the selected filter keeps its
  accent fill, because hover must not compete with the selected state.
- The treatment reuses the sort/icon-button hover pair rather than introducing a
  new colour, so light/dark themes need no new tokens.
- No transition is added, since the neighbouring sort and icon buttons swap
  their hover colours directly too.
- The request was silent about the pressed state, keyboard focus, motion and
  the separator dot, so the existing behaviour for each is preserved.
- The CSS rule was applied to the worktree before gate 1 under the live-preview
  practice, so you can review it on the real page; the "before" numbers are the
  same page with only that rule removed. The E2E module comes after the spec and
  is written against the shipped selector.
- `bump: patch` is expected for a user-visible change; the level is declared at
  Plan and reviewed at gate 2, not fixed here.
- The card is new (`ITEM-254`); the owner promotes it to `Ready` after gate 1.

## Clarifications

No clarifying questions were needed; no `[NEEDS CLARIFICATION]` markers remain.
