# Spec 052: Collapse the hidden add rows and tighten the section break

- **ID:** 052
- **Status:** Accepted
- **Item:** ITEM-054
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

The service pane shows empty space above every entry: each hidden add row reserves its full height
(~45px at a normal window width, ~71px when the buttons wrap), and the section-break rule adds 34px
of margin on each side. Above the first passage the two stack, so ~115px reads as loose spacing
with nothing in it. Collapse the hidden rows so they reserve nothing at rest, and tighten the
break's margins, without losing any way to reach the controls.

## Scope

### In scope

- `.entry__add` rows reserve no vertical space while hidden; they expand in place when revealed
  (item hover/focus per spec 037, own hover/focus per spec 036).
- A device without hover shows the add rows outright — it cannot hover-reveal them.
- The section-break rule keeps one clear separation with smaller margins (34px → 16px each side).
- The leading start bar (spec 030) stays always visible, unchanged.

### Out of scope

- The add actions, endpoints, reorder, and projection.
- The item's highlight and floating controls (specs 033, 034).
- The start bar's look, and anything on other panes.

## UI details

Approved preview: the live `/tatib/142/` session screenshots of 2026-10-10 (before / after-rest /
after-hover) that the owner OKed with "accept both".

- **Size / spacing:** a hidden add row is `height: 0` (grid track `0fr`; inner `min-height: 0;
  overflow: hidden`); a revealed row is its natural height (~38px single line, ~71px when the five
  buttons wrap at ~1280px) plus `padding-bottom: 10px`, applied only while revealed.
  `.tatib__eos` margins `16px 0` (was `34px 0`).
- **Position / layout:** rows stay direct siblings of the items, below each item's box (spec 036:
  no overlap); the five buttons keep their order inside the clipped inner element
  (`.entry__add-inner`, flex, `gap: 6px`, wrapping allowed).
- **Colors / typography:** unchanged — the existing `.entry__add-btn` dashed style.
- **States:** hidden = `opacity: 0` + collapsed track; revealed (item hover/focus per spec 037,
  own hover/focus per spec 036, `is-revealed` from `entries.js`) = `opacity: 1` + expanded track;
  coarse-pointer, no-hover devices = always revealed.
- **Responsive behavior:** the buttons wrap to a second line at narrow widths and the row expands
  to whatever height that needs (grid `1fr`, no fixed cap).
- **Motion:** `grid-template-rows`, `opacity`, and `padding-bottom` transition `140ms ease`, hide
  delayed `220ms`. The expanded box exists through the whole hide transition, so a travelling
  pointer can still enter the row.

## Domain rules

- **At rest, no dead space.** A hidden add row reserves no vertical space; consecutive entries sit
  as close together as with the editors off (the interposed row may block one margin collapse,
  which shows at most one paragraph margin).
- **Reveal expands in place.** Hovering or focusing an entry expands the add row above it and the
  one below it (spec 037); hovering or focusing a revealed row keeps only that row shown and never
  highlights the item above (spec 036).
- **No overlap survives.** A revealed row's box still lies entirely below its item's box.
- **Focus still reaches the rows.** Keyboard focus within an entry reveals the pair; moving focus
  into a revealed row keeps it open; tabbing onto a button inside a collapsed row expands that row.
- **Touch shows the rows.** On a coarse-pointer, no-hover device the add rows are always shown.
- **The break still divides, tighter.** A legacy END_OF_SECTION and a `section_break` entry render
  the same rule, now with 16px above and below — still far larger than the 2px between entries.

## Acceptance scenarios

### Scenario: Rest state

- **Given** a Tata Ibadah with entries
- **When** nothing is hovered or focused
- **Then** no add row is visible, and consecutive entries sit exactly as close together as
  they do with the editors turned off — no hidden element widens the gap

### Scenario: Hovering an entry

- **Given** an entry with hidden rows on both sides
- **When** I hover it
- **Then** the row above and the row below expand with their buttons, and the reveal settles:
  the entry stays under the pointer with its controls showing, and both rows are still open
  after the hide delay — no flicker. Opening the row above pushes the entry down once, by at
  most that row's height; the shift is bounded and never repeats while the entry stays hovered.
  An entry shorter than that push (the 2px section break) slides out from under a stationary
  pointer on the first hover; the reveal does not oscillate, and re-targeting the entry once
  finds it settled with its controls. Each row's box stays entirely below its item's box.

### Scenario: Moving onto a revealed row

- **Given** an entry hovered with both rows expanded
- **When** I move onto one of the rows
- **Then** only that row stays shown, and the entry above is not highlighted (spec 036)

### Scenario: Keyboard

- **Given** an entry holds keyboard focus
- **Then** the rows around it expand; focus moving into a revealed row keeps it open, and tabbing
  onto a button of a collapsed row expands that row before the focus lands visibly

### Scenario: A touch device

- **Given** a device without hover
- **Then** every add row is shown outright

### Scenario: The section break

- **Given** a section break between entries
- **Then** the same clear rule separates them, with 16px above and below instead of 34px

### Scenario: The first item

- **Given** the first entry in the service
- **Then** the leading start bar above it is still always visible (spec 030)

## Traceability

- Domain/app tests: N/A (pane layout and reveal; no server data).
- E2E: `tests/e2e/test_tatib_entry_controls.py`, `tests/e2e/test_entries.py`,
  `tests/e2e/test_reorder.py`, `tests/e2e/test_tatib_section_break.py`,
  `tests/e2e/test_old_rows.py`.
- Implementation: `static/styles/design/components.css`, `static/web/entries.js`,
  `multimedia/web/templates/reading/tatib.html` (the clipped inner element).
- Amends: spec 035 (the break's separation, now with smaller margins), specs 036 / 037 (the hidden
  row no longer reserves space, and a reveal that shifts a short item no longer oscillates; the
  reveal rules themselves are unchanged).
