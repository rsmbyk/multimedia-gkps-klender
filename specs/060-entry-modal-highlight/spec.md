# Spec 060: Clear stale service entry highlight after modal dismissal

- **ID:** 060
- **Status:** Accepted
- **Item:** ITEM-062
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

An unhovered service entry must return to its resting appearance after a
pointer-opened Preview, Edit, or Delete modal closes, while keyboard users keep
visible and usable focus.

## Scope

### In scope

- Service entry highlight and floating controls after Preview dismissal,
  Edit cancellation/save, and Delete cancellation.
- Applicable legacy rows using the same selectors and modal handlers.
- Real hover and keyboard interaction after restoration, in both themes.

### Out of scope

- New controls on entry kinds that do not have them; sidebar styling; add rows.
- Changes to stored content, deletion semantics, projection, or layout.
- Redesigning modal contents or global focus handling outside service entries.

## Domain rules

- Focus restored after a pointer-opened modal does not count as hover or
  deliberate keyboard navigation, even when Escape is used to dismiss it.
- Keep DOM focus at the existing usable restoration target; never fix the
  visual state by discarding focus or using a hidden sink.
- Genuine hover always reveals the entry background and available controls.
- Tab/Shift+Tab into available controls shows normal keyboard focus and controls.
- Returning from a keyboard-opened entry modal preserves visible keyboard focus.
  This narrowly refines spec 025 for these entry modals; pointer restoration
  stays quiet. Spec 034's keyboard highlighting and no-stale-state rules remain.
- Successful deletion uses the existing surviving focus target and must not
  leave an unrelated unhovered entry highlighted by automatic restoration.

## UI details

- **Approved preview:** [preview.html](./preview.html), copied from the state
  preview presented in this task and approved on 2026-10-12. The project owner
  accepted this Draft on 2026-10-12.
- **Size / spacing:** existing entry minimum height 52px, horizontal padding
  10px, horizontal margins -10px, corner radius 9px. No new reserved space.
- **Position / layout:** control group stays absolute at top 8px/right 8px;
  gap 4px, padding 3px, border 1px, radius 9px. No text displacement on state change.
- **Colors / typography:** resting background transparent; active hover/keyboard
  background `--icon-hover-bg` (light `rgba(31,31,29,.08)`, dark
  `rgba(255,255,255,.09)`). Existing typography and link tokens remain authoritative;
  the preview illustrates states, not replacement font/color tokens.
- **States:** pointer-restored, unhovered entries have transparent backgrounds
  and control opacity 0; actual hover or deliberate keyboard focus restores
  the existing highlight and control opacity 1. Existing active/disabled control
  styles remain. Focus indication remains visible for keyboard navigation.
- **Responsive behavior:** same rules across existing breakpoints. Under
  `(hover: none) and (pointer: coarse)`, controls remain visible as today.
- **Motion:** existing `--ease`, 200ms cubic-bezier(.32,.72,.28,1), for background
  and control opacity; retain existing reduced-motion behavior.

## Acceptance scenarios

### Scenario: Each pointer-opened modal returns to rest

- **Given** an entry with Preview, Edit, and Delete controls on a hover-capable device
- **When** I click each control in turn and dismiss its modal with the pointer away
  from the entry, using each supported close/cancel, backdrop, or Escape route
- **Then** after the existing transition its background is transparent and its
  controls are hidden
- **And** focus remains on a usable restoration target and no content changes.

### Scenario: Editing and refresh

- **Given** I open an entry editor by pointer
- **When** I save a valid change and the stage refresh settles, with the pointer elsewhere
- **Then** the saved entry has no stale highlight or revealed controls from restored focus.

### Scenario: Hover remains authoritative

- **Given** focus has been restored quietly after a modal closes
- **When** I move the pointer over the entry and then away
- **Then** its background and controls appear on hover and disappear on departure
- **And** the text does not shift as those visual states change.

### Scenario: Keyboard access and return

- **Given** a modal has closed after pointer opening
- **When** I use Tab/Shift+Tab to reach entry controls
- **Then** the focused control and entry have their normal visible keyboard state
- **When** I open and close an entry modal using the keyboard
- **Then** focus returns visibly to a usable entry target and keyboard navigation continues.

### Scenario: Deletion

- **Given** I open Delete by pointer on a disposable test entry
- **When** I confirm deletion and the refresh settles with the pointer elsewhere
- **Then** the existing deletion behavior succeeds and automatic focus does not
  leave an unrelated entry highlighted or its idle controls revealed.

### Scenario: Themes and touch

- **Given** either light or dark theme
- **Then** the above resting, hover, and keyboard rules hold with the existing tokens
- **Given** a coarse touch device with no hover
- **Then** available entry controls remain visible and usable after modal dismissal.

## Traceability

- Domain/app tests: N/A; visual interaction only.
- Targeted E2E: `DJANGO_DEVELOPMENT_MODE=True python manage.py test
  tests.e2e.test_tatib_hover.TatibHoverE2ETests --noinput -v 1` — 10 tests passed
  locally on 2026-10-12, including all pointer dismissal paths, keyboard close/save/delete,
  touch controls, edit refresh, themes, and legacy rows.
- Implementation: `static/styles/design/components.css` distinguishes deliberately
  focused descendants from quiet restoration; `static/web/preview.js` and
  `static/web/entries.js` retain opener modality; `static/web/reading.js` carries
  keyboard focus through entry save/delete refresh.
- Related: specs 025 (quiet restoration), 033 (controls), 034 (highlight), 055 (box).
