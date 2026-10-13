# Spec 086: Separate the modals from the page behind them

- **ID:** 086
- **Status:** Accepted
- **Item:** ITEM-089
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make the entry Preview and the sidebar editor dialogs unmistakably the front plane, in both themes.

## Scope

### In scope

- The scrim behind the Editor and Preview dialogs, and behind the Preview's mode confirmation.
- The dialogs' border and elevation.

### Out of scope

- The dialogs' geometry, contents, focus, and dismissal behaviour.
- Blur or any filter over the page: the origin entry's highlight must stay readable behind the scrim.
- Tooltips, the drag copy, and the legacy OBS docks.

## Domain rules

- N/A — presentation only.

## UI details

- **Visual reference:** [Backdrop comparison preview](./preview.html) — the same dialog over the same
  page, current scrim beside the proposed one, in dark and light, with the opacity shown as a number.
- **Size / spacing / position:** unchanged. The scrim covers the viewport; the dialogs keep
  `width: min(44rem, 100vw - 32px)` (Preview) and their current sizes, paddings, and radii.
- **Colors / typography:** two new tokens, used by name rather than as literals:
  - `--backdrop`: `rgba(20, 20, 18, .52)` in light, `rgba(0, 0, 0, .68)` in dark.
  - `--shadow-dialog`: `0 20px 55px -24px rgba(20, 20, 18, .55)` in light,
    `0 26px 64px -26px rgba(0, 0, 0, .9)` in dark.
  Both dialogs take `border: 1px solid var(--divider)` (light `#D9D6CD`, dark `#3A362F`) and
  `box-shadow: var(--shadow-dialog)`. The scrim replaces the current `rgba(31, 31, 29, .38)` in
  `.editor::backdrop`, `.preview::backdrop`, and `.preview__confirm-layer`.
- **States:** no interactive state changes. The scrim stays non-interactive in the sense that a click on
  it still dismisses the Preview, and the Editor's existing behaviour is unchanged. The origin entry's
  `is-modal-origin` highlight remains visible through the darker scrim.
- **Responsive behavior:** unchanged; the scrim is a backdrop and the dialog keeps its existing narrow
  width rules.
- **Motion:** none added; the dialogs keep opening and closing as they do today.

## Acceptance scenarios

### Scenario: Dark theme separation

- **Given** the app is in dark mode and a page with content is behind
- **When** the operator opens an entry Preview or an editor
- **Then** the page behind is visibly dimmed toward black, the dialog reads as a distinct plane, and its
  1px outline and larger shadow are apparent.

### Scenario: Light theme separation

- **Given** the app is in light mode
- **When** a dialog opens
- **Then** the scrim is deeper than the current 38% but the page stays legible, and the dialog keeps a
  visible edge.

### Scenario: The origin entry stays readable

- **Given** an entry's Preview is open from the Tata Ibadah pane
- **When** the operator looks at that entry behind the scrim
- **Then** its highlight and controls are still discernible under the darker scrim.

### Scenario: The mode confirmation matches

- **Given** a Text entry's Preview shows the switch-to-default confirmation
- **When** the confirmation overlay covers the Preview
- **Then** it uses the same scrim token as the dialogs, so the two layers do not disagree.

### Scenario: Nothing else moves

- **Given** the change is applied
- **When** any dialog is opened and dismissed
- **Then** its size, radius, padding, contents, and dismissal behave exactly as before, and tooltips and
  the drag copy keep their existing shadow.

## Traceability

- Domain/app tests: N/A — `tests/test_design_tokens.py` keeps passing (it parses hex values only).
- E2E: `tests/e2e/test_editor.py` and `tests/e2e/test_entry_preview.py` — the dialog still opens, closes,
  and hit-tests; `::backdrop` computed background asserted in both themes.
- Implementation: `static/styles/design/tokens.css`, `static/styles/design/components.css`.
