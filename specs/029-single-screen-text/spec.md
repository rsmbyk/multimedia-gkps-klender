# Spec 029: Single-screen text entry

- **ID:** 029
- **Status:** Accepted
- **Item:** ITEM-031
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

Add a service entry kind — **Single-Screen Text** — that shows its entire body on one projector
screen, shrinking the font until it fits, and only ellipsizing when it cannot shrink further. The
existing **Text** kind keeps splitting into two-line screens.

## Scope

### In scope

- A `SINGLE_SCREEN_TEXT` entry kind, edited like a text entry (a title and a body).
- One projector screen per entry, carrying the whole body; blank lines are paragraph breaks on that
  screen, not new screens.
- Font shrinking until the body fits; a hard truncation with a trailing "…" only when it cannot fit
  at the smallest size the loop reaches.
- The reading pane shows the entry like a text entry.

### Out of scope

- The existing **Text** kind and `_line_pairs()` (spec 006).
- Scripture, song, and section break rendering.
- The OBS dock / source pages.

## Domain rules

- **The body is one screen.** A single-screen text is never split by `_line_pairs()`; its blank
  lines are paragraph breaks within that one screen.
- **A text is required.** Like a text entry, this kind rejects an empty body.
- **Fit first, ellipsize last.** The font shrinks until the body fits. There is no readable minimum
  (the loop goes as small as it will); only if the body still overflows at that smallest size is it
  hard-truncated with a trailing "…", and it never overflows the screen.
- **Nothing else moves.** The kind is additive: existing kinds, splitting, and projection behave as
  before.

## Acceptance scenarios

### Scenario: It is offered and edited like a text

- **Given** the editor is open on a Tata Ibadah
- **Then** a **Single-Screen Text** action is offered beside the other kinds
- **When** I save one with a title and a body
- **Then** it is stored as a `SINGLE_SCREEN_TEXT` entry, and saving it with an empty body is refused

### Scenario: The whole body is one screen

- **Given** a single-screen text whose body has several lines and a blank line between them
- **When** the projector shows it
- **Then** it is a single screen carrying every line, with the blank line as a paragraph break, not a
  second screen

### Scenario: The font shrinks to fit

- **Given** a single-screen text longer than the display at the ordinary size
- **Then** its font shrinks until the whole body fits the screen

### Scenario: It ellipsizes rather than overflow

- **Given** a single-screen text that still does not fit at the smallest size the fit loop reaches
- **Then** the text is truncated with a trailing "…" and does not overflow the screen

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: `tests/e2e/test_projector.py`.
- Implementation: `multimedia/tatib/models.py`, `multimedia/web/reading/entries.py`,
  `multimedia/web/reading/views.py`, `multimedia/web/templates/reading/tatib.html`,
  `multimedia/web/templates/reading/projector.html`, `static/web/projector.js`,
  `static/web/entries.js`.
