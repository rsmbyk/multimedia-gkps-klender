# Spec 070: Manual breaks for Single-screen Text entries

- **ID:** 070
- **Status:** Accepted
- **Item:** ITEM-073
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

Let an editor split a Single-screen Text entry across projector screens from its preview modal while keeping one screen as the default.

## Scope

### In scope

- The Spec 069 preview-modal break interaction on every Single-screen Text entry, including short entries that are not clipped in the reading pane.
- A per-entry custom arrangement saved without opening Create/Edit, used by the projector and live refresh.
- A one-screen default and a footer Reset breaks action that restores it.

### Out of scope

- The ordinary Text entry's two-line default or its mandatory blank-line boundaries.
- Song, Scripture, legacy, and section-break entries.
- Changes to text content, entry naming, projector typography controls, or the existing trailing blank screen.

## Domain rules

- A content line is a nonempty newline-delimited line in the entry. Blank written lines are paragraph spacing, not automatic screen breaks for this kind.
- **Default mode:** `screen_breaks = null` projects the complete Single-screen body on one screen, including its paragraph spacing, with the existing fitting and overflow safeguard. Preview shows no active break dividers and labels the mode `Default · 1 screen`.
- **Custom mode:** adding the first break saves an ordered set of boundaries and changes the mode to `Custom`. Anchor that first break, then add breaks every two content lines in both directions from it. A break may be placed between consecutive content lines even when blank written lines separate them. Later clicks add or remove only the chosen break. Removing the last break leaves a custom one-screen arrangement until Reset breaks is clicked.
- A boundary separates two content lines. Every content line belongs to exactly one generated group in written order. Blank lines remain paragraph spacing when both neighboring content lines share a screen. If a boundary separates those paragraphs, the blank lines at that boundary do not create a blank screen or an empty row at the edge of either content screen.
- Every content line belongs to exactly one generated screen in written order. Every resulting content screen retains the entry title. Speaker cues are parsed across the complete body before grouping so a cue continues correctly on later screens. Each resulting screen uses the existing Single-screen fitting and overflow safeguard, which may shorten an overfull group. One built-in blank screen follows the entry, as before.
- The modal and projector read the same saved boundaries. Saving a change refreshes an already open projector. A request with an outdated text signature is rejected and asks the editor to reopen Preview.
- A later Create/Edit save that changes the pattern of content and blank lines clears custom boundaries and returns to default mode; Preview explains the reset. A wording-only edit that preserves that pattern keeps the boundaries.
- Only an authorized editor may save or reset breaks. Viewers may read the preview but cannot use the break controls.

## UI details

The [Draft interaction preview](./preview.html) adapts the approved [Spec 069 preview](../069-manual-text-screen-breaks/preview.html). The implemented modal reuses the current app's styling and interaction; only the default mode and blank-line meaning differ.

- **Size / spacing:** Keep the dialog width `min(44rem, 100vw - 32px)`, max height `100vh - 48px`, 22px body padding, and sticky footer padding of 12px vertically and 22px horizontally. Use one text row per written content line with 5px vertical row padding; blank written lines add 12px paragraph spacing. Each selectable gap is 18px high and spans the available row width.
- **Position / layout:** Keep the entry title above the rows. Keep Reset breaks at the start of the sticky footer and `Screen breaks` plus the mode badge immediately to its right, separated by 12px. The modal has no Close button. The default has no visible divider. A break across paragraphs is shown in their visual gap.
- **Colors / typography:** Reuse theme tokens from Spec 069: neutral `--head-ink` for custom break lines, `--active-bg` for the Add break dots and label (light `#1C5C3C`, dark `#7C9CF0`), and `--danger` for the hovered Remove break line and label. Rows keep the preview's serif text. The footer mode label is 12px; its badge has a 1px `--divider` border and 2px by 8px padding.
- **States:** An empty gap is invisible at rest. Hover or keyboard focus shows regular round dots spaced 6px apart and a centered `Add break` label. A saved break is one uninterrupted neutral line at rest; hover or focus changes it to danger and reveals `Remove break` at the center. A pending save disables break targets and Reset breaks. The mode changes to `Custom` after the first successful save and back to `Default · 1 screen` after Reset breaks. Escape or a backdrop click dismisses Preview.
- **Responsive behavior:** At narrow viewports, keep the same 16px minimum side clearance and scroll only the modal body while its footer stays visible.
- **Motion:** No animation for the divider or mode change; feedback appears on hover/focus and after the save response.

## Acceptance scenarios

### Scenario: Preserve the existing single screen

- **Given** a Single-screen Text entry with six content lines and no custom breaks
- **When** it is previewed and projected
- **Then** Preview shows `Default · 1 screen` with no active divider
- **And** the projector shows one fitted content screen, with the existing overflow shortening if needed, followed by its built-in blank screen.

### Scenario: First custom break sets the cadence

- **Given** a Single-screen Text entry with six content lines in default mode
- **When** an editor adds a break after line one in Preview
- **Then** Preview changes to `Custom` and shows breaks after lines one, three, and five
- **And** the projector shows line 1, lines 2–3, lines 4–5, and line 6 on consecutive content screens
- **And** the written text is unchanged.

### Scenario: Toggle one break and reset

- **Given** a custom Single-screen Text arrangement with several breaks
- **When** the editor removes one divider or adds one at another gap
- **Then** only that boundary changes and the new projector sequence is saved
- **When** the editor clicks Reset breaks
- **Then** Preview returns to `Default · 1 screen` and the projector returns to one fitted content screen.

### Scenario: Split at a paragraph boundary

- **Given** two paragraphs separated by a blank written line
- **When** the editor adds a break between their final and first content lines
- **Then** the paragraphs appear on separate screens without an extra blank screen between them
- **And** the same blank line remains paragraph spacing whenever those paragraphs share one content screen.

### Scenario: Keep title, voices, and live display

- **Given** an entry with a title and a speaker cue that continues across a chosen break, with its projector open
- **When** the editor saves a custom break
- **Then** each resulting screen has the title, each line keeps its correct voice, and the open projector refreshes to the saved sequence.

### Scenario: Guard edits and permissions

- **Given** an entry with saved custom breaks
- **When** its content/blank-line pattern changes in Create/Edit
- **Then** those breaks reset to default and Preview explains why
- **And** a stale save request or a viewer without edit permission cannot overwrite the entry's breaks.

## Traceability

- Domain/app tests: `multimedia/tatib/tests.py` (kind-specific validation and boundaries), `multimedia/web/tests.py` (save/reset, projector grouping, edits, permissions), `multimedia/web/test_speaker_voices.py` (continued cues).
- E2E: `tests/e2e/test_single_screen_text_breaks.py` (Preview controls, cadence, reset, and live projector refresh).
- Implementation: `multimedia/tatib/models.py`, `multimedia/tatib/screen_breaks.py`, `multimedia/web/reading/entries.py`, `multimedia/web/reading/views.py`, `multimedia/web/templates/reading/tatib.html`, `static/web/preview.js`, and existing preview styles.
