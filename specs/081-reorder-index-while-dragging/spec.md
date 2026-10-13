# Spec 081: Renumber the drag copy while a row is being reordered

- **ID:** 081
- **Status:** Accepted
- **Item:** ITEM-084
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

While a Tata Ibadah entry is dragged through the contents list, the row in the operator's hand shows
the number it is about to take, not the number it had when it was picked up.

## Scope

### In scope

- The number painted on the drag copy (`.reorder__ghost`) in the Tata Ibadah contents list.
- The value it shows, and the moment it changes during a pointer drag.

### Out of scope

- The keyboard arrow move, which has no drag copy.
- The ghost's geometry, cover, shadow, and opacity; the persist payload; the reading pane.
- Every other list's numbers (Bible chapters, songbooks, songs).

## Domain rules

- While a row is dragged, the drag copy shows that entry's current 1-based position in the list, and
  it changes on the same placement step that reorders the list.
- The number counts exactly as the list already counts: every movable entry row and every section
  break row takes one position, in the order shown, and a section break paints no number — so a row
  that passes an invisible break reads `4` where the row above reads `2`. That gap is the list's
  existing rule and is left alone here.
- The number on the drag copy always equals the number the same row shows when the gesture ends.
- A cancelled gesture restores the original order and the original numbers, with the drag copy gone.
- A drag that starts and ends without moving (a short press) leaves every number as it was.
- Nothing is written to the server because of this: the number is presentation, and the order is
  written by the existing drop path.

## UI details

- **Visual reference:** [Renumbering preview](./preview.html) — drag a row with "Current build" off:
  the copy in hand counts as it moves. Turn "Current build" on to see the reported jump.
- **Size / typography:** unchanged — `560 13px/1.4 ui-sans-serif`, tabular numerals, `min-width:
  3.4rem`, centered on the whole row per spec 064. Only the text node's value changes.
- **Colors:** unchanged; the copy keeps `--ink` on the ghost's `--canvas` fill.
- **States:** the copy's number is not a control: no hover, focus, or selected state. It never
  becomes interactive, and the copy stays `aria-hidden` and `inert`.
- **Responsive behavior:** unchanged at every width; the copy is a fixed-position box measured from
  the grabbed row.
- **Motion:** none for the number itself. The copy already carries `transition: none !important` and
  the other rows keep their morph (160ms in place, 60ms mid-drag).

## Acceptance scenarios

### Scenario: The number in hand follows the row

- **Given** a Tata Ibadah service with at least four entries
- **When** the operator drags the second entry down past the third and fourth
- **Then** the drag copy reads 3, then 4, on the same steps that the rows part, and reads 4 when the
  drop lands.

### Scenario: Dragging upwards

- **Given** the fourth entry is grabbed
- **When** it is dragged above the first
- **Then** the copy reads 3, 2, then 1 as it passes each row.

### Scenario: A section break counts but shows no number

- **Given** a section break sits between two entries and the entry below it is dragged above the break
- **When** the copy passes the break
- **Then** the copy's number advances by the break's position while the break itself still paints no
  number.

### Scenario: Cancel and no-op presses

- **Given** a drag in progress
- **When** the gesture is cancelled, or the pointer is pressed and released without moving
- **Then** every row shows its original number again and no copy remains.

### Scenario: Keyboard move is unaffected

- **Given** the focus is on a row's grip
- **When** the operator moves the row with the arrow keys
- **Then** the numbers follow as they do today, with no drag copy in the document.

## Traceability

- Domain/app tests: N/A — client-side presentation only.
- E2E: `tests/e2e/test_reorder.py` (drag, cancel, no-op press, break position) and
  `tests/e2e/test_toc_number_centering.py`.
- Implementation: `static/web/reorder.js`.
