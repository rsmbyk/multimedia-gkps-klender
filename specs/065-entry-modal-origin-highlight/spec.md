# Spec 065: Hold the service entry highlight while its modal is open

- **ID:** 065
- **Status:** Accepted
- **Item:** ITEM-068
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

The service entry whose Preview, Edit, or Delete control opened a modal keeps
its hover appearance (background fill and floating controls) for as long as that
modal is open, and returns to the spec 061 after-close behaviour only once the
modal closes.

## Scope

### In scope

- Service entries (`.tatib__item`, `.tatib__eos`) and applicable legacy rows
  while their Preview, Edit, or Delete modal is open.
- Pointer-opened and keyboard-opened modals, in both themes.

### Out of scope

- Add rows and the start bar (`is-revealed`) around the entry.
- Add-row openers, sidebar editors, and modal contents.
- After-close behaviour (spec 061), stored content, deletion, projection, layout.

## Domain rules

- Opening an entry modal holds that entry's hover appearance until the modal
  closes, wherever the pointer or focus is meanwhile.
- Only the entry that owns the opening control is held; no other entry changes.
- The hold starts when the modal actually opens. An Edit whose fragment fails
  to load never opens the modal and leaves nothing held.
- Closing the modal by any route (Close/Cancel, backdrop, Escape, Save, or a
  confirmed Delete) releases the hold. Spec 061's quiet pointer restoration and
  visible keyboard return then apply unchanged.

## UI details

- **Approved preview:** [preview.html](./preview.html), approved by the project
  owner on 2026-10-12.
- **Size / spacing / position:** unchanged — entry minimum height 52px, padding
  10px, margins -10px, radius 9px; control group absolute at top 8px/right 8px,
  gap 4px, padding 3px, border 1px, radius 9px. No text displacement.
- **Colors / typography:** held background is the hover token `--icon-hover-bg`
  (light `rgba(31,31,29,.08)`, dark `rgba(255,255,255,.09)`), seen through the
  existing modal backdrop. Existing typography and link tokens unchanged.
- **States:** while its modal is open, the origin entry shows the hover fill and
  control opacity 1. After close, the entry follows spec 061 (pointer-opened:
  transparent and controls at opacity 0 once the pointer is elsewhere;
  keyboard-opened: visible keyboard focus).
- **Responsive behavior:** same across breakpoints. Under
  `(hover: none) and (pointer: coarse)`, controls stay visible as today.
- **Motion:** existing `--ease` (200ms cubic-bezier(.32,.72,.28,1)) for
  background and control opacity; reduced-motion behaviour unchanged.

## Acceptance scenarios

### Scenario: Pointer-opened modal holds the entry

- **Given** an entry with Preview, Edit, and Delete controls on a hover-capable device
- **When** I click each control in turn and move the pointer onto the modal backdrop
- **Then** while the modal is open the entry keeps the hover fill and its controls are visible
- **When** I dismiss the modal with the pointer away from the entry
- **Then** after the existing transition the entry is transparent and its controls hidden.

### Scenario: Keyboard-opened modal holds the entry

- **Given** I activate an entry control from the keyboard
- **Then** while the modal is open the entry keeps the hover fill and visible controls
- **When** I close the modal from the keyboard
- **Then** focus returns visibly to the entry control as in spec 061.

### Scenario: Only the origin entry is held

- **Given** several entries on the stage
- **When** I open a modal from one entry
- **Then** no other entry shows the fill or controls.

### Scenario: Legacy rows

- **Given** a legacy row with Edit and Delete controls
- **When** I open its Edit modal by pointer and move the pointer away
- **Then** the row stays held until the modal closes, then rests.

## Traceability

- Domain/app tests: N/A; visual interaction only.
- Targeted E2E: `DJANGO_DEVELOPMENT_MODE=True python manage.py test
  tests.e2e.test_tatib_hover.TatibHoverE2ETests --noinput -v 1` — 14 tests passed
  locally on 2026-10-12, including the pointer hold for Preview/Edit/Delete in both
  themes, the keyboard hold, only-origin held, legacy rows, the failed-load guard,
  and every spec 061 after-close test. `tests.e2e.test_entry_preview` and
  `tests.e2e.test_tatib_entry_controls` also passed (25 tests).
- Implementation: `static/styles/design/components.css` adds the
  `is-modal-origin` state to the entry background and control selectors;
  `static/web/preview.js` and `static/web/entries.js` mark the origin entry when
  the modal opens and release it on close.
- Related: specs 034 (highlight), 033 (controls), 055 (box), 061 (after close).
