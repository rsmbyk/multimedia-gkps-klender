# Spec 085: Show the entry's identity in the Preview dialog's header

- **ID:** 085
- **Status:** Accepted
- **Item:** ITEM-088
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

The entry Preview dialog names what it is showing in a fixed header, so the identity of the entry no
longer scrolls away with its content — and a song's verse tabs sit in that header.

## Scope

### In scope

- The Preview dialog: a header region carrying the entry's identity for every preview kind.
- Text title, passage reference, song heading, and the song verse tabs.
- The dialog's accessible name and the script's tab wiring.

### Out of scope

- The body's text, the screen-break gaps and the footer controls (spec 069, spec 070, spec 079), and the
  focus and highlight behaviour of spec 025 / spec 065.
- A close button: the dialog keeps dismissing through Escape, the overlay, and the entry pane, as the
  editor dialog does.
- The reading pane, the sidebars, and the search page.

## Domain rules

- Every preview kind shows its identity in the header: a Text entry its title, a passage its reference,
  a song its `HAL 3 — Sai puji Naibata` heading.
- A Text entry with no title has no header: the dialog opens straight into its content, exactly as it
  does today, rather than showing an empty bar.
- A song with more than one verse keeps its verse tabs, in the header, above the verse text; a song with
  a single verse shows a header with no tabs.
- The identity line is shown once: it leaves the body when it moves to the header.
- The header does not scroll: the body keeps the scroll, the existing padding, its focus behaviour, and
  its arrow-key handling.
- The dialog's accessible name is the identity it shows; when there is none it keeps the current
  `Preview` label.
- Reading and dismissal behaviour is unchanged: the same trigger highlights the same origin entry, the
  same scroll offset is restored, and Escape, the overlay, and closing the page still work.
- Viewers and editors see the same header; only the footer's editability differs as it does now.

## UI details

- **Visual reference:** [Preview header preview](./preview.html) — switch between Text, Song, and
  Passage, and between light and dark.
- **Size / spacing / position:** the dialog keeps `width: min(44rem, 100vw - 32px)`, `max-height:
  calc(100vh - 48px)`, radius 14px, and a flex column. The header is the first row: `padding: 14px 22px`,
  `min-height: 52px`, `display: flex; align-items: center; gap: 14px`, with a 1px `--divider` bottom
  border and the canvas background. The body keeps its `22px` padding and takes the remaining height.
- **Colors / typography:** identity text uses the current `.preview__ref` / `.preview__song` style —
  `font: 640 16px/1.3 ui-sans-serif, system-ui, sans-serif`, `color: var(--ink)`. The header's background
  is `var(--canvas)` and its border `var(--divider)`. The verse tabs keep their spec-073 look: 30px
  circles, 1px `--divider` outline, `--active-bg` / `--active-ink` when selected.
- **States:** the identity line is static text — no hover, focus, or selected state, and it is not a
  control. The tabs keep their click, keyboard, focus-ring, and `aria-selected` behaviour. Long
  identities truncate with an ellipsis instead of pushing the tabs away.
- **Responsive behavior:** at 44rem and above, the identity sits left and the tabs right on one row. At
  narrow widths the tabs wrap to a second line inside the header and scroll horizontally when they
  exceed the width, keeping their fixed 30px circles (spec 073). Below 420px the header keeps 14px side
  padding and the identity is limited to one line. The dialog's existing narrow-width rules are
  unchanged.
- **Motion:** none. The header appears with the dialog; opening, dismissing, and the existing
  reduced-motion clamp are untouched.

## Acceptance scenarios

### Scenario: A titled Text entry

- **Given** a Text entry titled "Votum" with content
- **When** its Preview opens
- **Then** "Votum" is shown in the header, it does not scroll with the body, and the body no longer
  repeats it.

### Scenario: An untitled Text entry

- **Given** a Text entry with no title
- **When** its Preview opens
- **Then** no header is shown and the dialog keeps the accessible name "Preview".

### Scenario: A passage

- **Given** a scripture entry such as Imamat 2:1-16
- **When** its Preview opens
- **Then** the reference is shown in the header and the body shows the passage text only.

### Scenario: A song with several verses

- **Given** a song entry whose selected verses are more than one
- **When** its Preview opens
- **Then** the heading, e.g. `HAL 3 — Sai puji Naibata`, and the verse tabs are both in the header, and
  switching tabs still swaps the verse text in the body.

### Scenario: Scrolling and dismissal

- **Given** any open Preview
- **When** the operator scrolls the content, presses Escape, or clicks the overlay
- **Then** the header stays put while the body scrolls, and dismissal restores the trigger and its
  entry exactly as before.

## Traceability

- Domain/app tests: N/A — no new server rule (the preview payload is unchanged; only where its parts are
  rendered changes).
- E2E: `tests/e2e/test_entry_preview.py` (passage, song tabs, titled and untitled Text, overlay close),
  with regressions checked in `tests/e2e/test_text_screen_breaks.py`,
  `tests/e2e/test_unified_text_screen_mode.py`, `tests/e2e/test_single_screen_text_breaks.py`, and
  `tests/e2e/test_tatib_hover.py`.
- Implementation: `multimedia/web/templates/reading/_preview_modal.html`,
  `multimedia/web/templates/reading/tatib.html`, `static/web/preview.js`,
  `static/styles/design/components.css`.
