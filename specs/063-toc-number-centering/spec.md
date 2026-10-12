# Spec: Center entry numbers vertically in the Tata Ibadah contents list

- **ID:** 063
- **Status:** Accepted
- **Item:** ITEM-064
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make the Tata Ibadah contents list easier to scan by placing each entry number at
the vertical middle of its row, instead of beside the first line of text.

## Scope

### In scope

- The entry number (`.songrow__c`) in every Tata Ibadah contents row: untitled
  text entries, two-line labels, song entries with a verse line, and single-line rows.
- The drag copy of a row while reordering.

### Out of scope

- The songbook song list, which shares the row style.
- Text alignment, wrapping, row height, padding, typography, colors, the drag
  handle, section-break rows, markup, and behavior.

## Domain rules

- None. Presentation only.

## UI details

- **Approved preview:** [preview.html](./preview.html), approved by the project
  owner on 2026-10-12. The project owner accepted this Draft on 2026-10-12.
- **Size / spacing:** unchanged — row `min-height: 38px`, padding `7px 10px`,
  gap `10px`, radius `9px`; number cell `min-width: 3.4rem`; label
  `padding-right: 30px` for the drag handle.
- **Position / layout:** the number's vertical center equals the row's content-box
  vertical center (±1px) for rows of any line count. The text keeps its current
  position (±0.5px). Horizontal positions are unchanged.
- **Colors / typography:** unchanged — number `560 13px/1.4` system sans-serif,
  tabular figures; existing ink, muted, and selected tokens.
- **States:** hover, selected (`aria-current="true"`), keyboard focus, filtered,
  and the drag copy all keep the centered number; light and dark themes.
- **Responsive behavior:** holds at contents-panel widths of 404px and 280px,
  where labels wrap to more lines.
- **Motion:** none.

## Acceptance scenarios

### Scenario: Multi-line rows

- **Given** a service with an untitled text entry whose label wraps to two lines,
  a song entry with `Bait 1-3` beneath its title, and a two-line text label,
- **When** the contents list displays them,
- **Then** each row's number is vertically centered on the row within 1px
- **And** each row's text sits where it did before the change.

### Scenario: Single-line rows

- **Given** a single-line entry such as `Votum`,
- **When** it is displayed,
- **Then** its number is vertically centered on the row within 1px and the row
  height is unchanged.

### Scenario: Narrow panel, states, and themes

- **Given** the contents panel at 404px and 280px, in light and dark themes,
- **When** a row is hovered or selected,
- **Then** its number stays vertically centered on the row within 1px.

### Scenario: Reordering

- **Given** a multi-line entry,
- **When** I drag it by its handle,
- **Then** the drag copy shows the number vertically centered on the copy within 1px.

### Scenario: Songbook list unchanged

- **Given** the songbook song list,
- **When** it is displayed,
- **Then** its number cells keep their current baseline alignment.

## Traceability

- Domain/app tests: N/A.
- E2E: `DJANGO_DEVELOPMENT_MODE=True python manage.py test
  tests.e2e.test_toc_number_centering --noinput -v 1` — `TocNumberCenteringE2ETests`,
  4 tests. Red on 2026-10-12 before the rule (numbers 10–19px above the row center);
  green after it. The neighboring `test_song_label_typography` and `test_reorder`
  modules (20 tests) also pass locally.
- Implementation: `static/styles/design/components.css` — `align-self: center` on
  `.songrow__c` under `:root[data-section="tatib"] #chList` and `.reorder__ghost`.
