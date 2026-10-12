# Spec 068: Subtle surface for Tata Ibadah entries

- **ID:** 068
- **Status:** Accepted
- **Item:** ITEM-071
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make each entry's item area in the right-hand Tata Ibadah service editor discernible while retaining the restrained look approved in the live preview.

## Scope

### In scope

- `.tatib__item--acts` entry boxes and `.tatib__eos` section-break boxes in the new Tata Ibadah reading pane.
- Light and dark styling, including the system theme's resolved appearance.
- Padding and minimum height needed to match the approved preview.

### Out of scope

- The middle section list, sidebar, add rows, entry content, controls' appearance or reveal logic, and other reading pages.

## Visual details

- Resting fill: light `rgba(31, 31, 29, 0.012)`; dark `rgba(255, 255, 255, 0.012)`.
- Resting outline: 1px inset, light `rgba(31, 31, 29, 0.08)`; dark `rgba(255, 255, 255, 0.09)`. It must not change layout dimensions.
- Padding: 8px top, 8px right, 8px bottom, 12px left. Minimum box height: 56px. Existing corner radius: 9px.
- Floating Preview/Edit/Delete controls stay at `top: 8px; right: 8px` within the box.
- The established `--icon-hover-bg` replaces the resting fill on hover, deliberate keyboard focus, and modal-origin state. Quiet focus restoration remains quiet. Existing controls, links, text colors, and add-row behavior stay unchanged.
- The same visual treatment applies at narrow widths; text may wrap within the padded box without clipping or horizontal overflow. Reduced-motion behavior stays unchanged.

## Domain rules

- None; this is a visual style change.

## Acceptance scenarios

### Scenario: Resting surface in both themes

- **Given** a Tata Ibadah pane with ordinary entries and a section break
- **When** no entry is hovered or deliberately focused
- **Then** each box uses the approved theme-specific fill and 1px inset outline, with 8/8/8/12px padding and no layout shift from the outline.

### Scenario: Interaction states

- **Given** an entry or section break with the new resting surface
- **When** it is hovered, deliberately focused, or owns an open modal
- **Then** the existing stronger interaction fill and floating controls work as before; quiet focus restoration does not impersonate hover.

### Scenario: Long content and narrow viewport

- **Given** a long text entry, song entry, and section break
- **When** the pane is viewed at a narrow width
- **Then** content remains readable, wraps within the box, and does not clip or overflow horizontally; controls remain 8px from the top and right.

### Scenario: Unrelated panes

- **Given** the section list or another reading page
- **When** this styling is applied
- **Then** those areas retain their existing appearance.

## Traceability

- Domain/app tests: N/A; CSS only.
- E2E: `tests/e2e/test_tatib_entry_controls.py` checks both theme tokens, box padding, outline, floating controls, and narrow-width overflow; `tests/e2e/test_tatib_hover.py` checks quiet resting fill and interaction states; `tests/e2e/test_tatib_section_break.py` checks the resized divider and its controls.
- Implementation: `static/styles/design/components.css` applies the surface and 56px minimum height; `static/styles/design/tokens.css` supplies theme-specific fill and outline values.
