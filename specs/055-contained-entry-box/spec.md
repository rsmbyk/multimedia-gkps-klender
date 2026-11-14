# Spec 055: Give each entry a containing box with centred words and equal add-row gaps

- **ID:** 055
- **Status:** Accepted
- **Item:** ITEM-057
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

The service pane's vertical model has three problems the owner hit while walking the live
`/tatib/142/` after specs 052–054: the start bar is parked above the first entry no matter what
(spec 030), each entry reserves a 44px band for Preview / Edit / Delete that inflates every card
(spec 053), and a revealed add row leaves 4px above its buttons but 84px below them (the row's
10px padding plus the next heading's 30px margin). The owner's four rules, verbatim: the top and
bottom gaps must include the control buttons; they must look equal; the texts/words must be
centred vertically; the buttons stay floating at the top-right — in every condition. One model
satisfies all four: an entry is a **box containing its controls** (min-height 52px = 8 + 36 + 8),
its words centre inside it, every revealed add row keeps 8px to the boxes above and below, and
the start bar collapses and reveals like the other rows.

## Scope

### In scope

- `.tatib__item--acts` becomes the containing box: flex column, `justify-content: center`,
  `min-height: 52px`; the spec-053 `padding-top: 44px` band goes; first/last flow-child margins
  zeroed so the box is its content or 52px.
- Words centred vertically in the box (exact on anything that fits in 52px).
- `.entry__add` rows: rest margins `6px 0` → uniform 12px box-to-box rhythm; revealed
  `padding: 8px 0; margin-block: 0` → exactly 8px above and below the buttons, in every reveal
  state (neighbour hover, own hover, focus, touch).
- The start bar `.entry__start` collapses like the rows: 0px at rest; revealed on hover/focus of
  itself or the first entry (`is-revealed` from `entries.js`; the buttons wrapped in
  `.entry__start-inner` in `tatib.html`); `margin-top: -30px` while revealed so it sits 8px
  under the heading and 8px above the first words.
- `.tatib__eos` takes the same 52px box: margins 0, the rule drawn by `::before` (centred),
  diamond at the box centre, the note pinned under the rule.
- Touch (hover: none / pointer: coarse): bar and rows shown outright in the same geometry.
- E2E rewrites and new assertions (named in tasks).

### Out of scope

- The controls' look, their `top: 8px; right: 8px` spot, and the 033/034 reveal/touch triggers.
- Link colours (spec 056).
- The editors-off pane: `.tatib__item + .tatib__item { margin-top: 2px; }` stays as is.
- The empty-service invitation block and other panes.

## UI details

Approved preview: the live `/tatib/142/` session of 2026-10-11 (injected-CSS previews — rest,
hover first entry, hover card, hover one-liner, divider, bar hover, touch; 1920 and 1280 wide)
that the owner OKed with "proceed".

- **Size / spacing:** box `min-height: 52px` = 8px + controls (measured 35.6px) + 8px. At rest:
  box-to-box gap **12px** uniform (row margins `6px 0`); start bar 0px; heading → first box
  30px. Revealed row: buttons **8px** from the box above and **8px** from the box below —
  measured for the first entry, the card, the one-liner, the divider, keyboard focus, and the
  bar hover. Start bar revealed: 8px under the heading, 8px above the first words.
- **Position / layout:** controls keep `position: absolute; top: 8px; right: 8px`; inside a
  52px box that is the box's vertical centre. On entries taller than 52px the controls float
  over the top-right corner while shown — no reserved band (amends 053; owner-approved).
- **Colors / typography:** unchanged; the hover fill (spec 034) paints the box as one row.
- **States:** rows and bar keep `opacity: 0` at rest and the existing reveal triggers
  (neighbour hover per 036/037, own hover, `:focus-within`, `is-revealed`); the bar joins the
  same scheme; touch shows everything outright.
- **Responsive behavior:** the five buttons may wrap (measured row height 77.2px at 1280); the
  gaps stay 8px/8px and the box stays at least 52px at every width.
- **Motion:** `grid-template-rows`, `opacity` and `padding` transition 140ms ease with a 220ms
  hide delay, 0s on reveal (existing); the bar adds `margin-top` to the same transition.

## Domain rules

- **The box contains its controls.** Every entry that renders `.entry__acts` is at least 52px
  tall and the controls sit wholly inside it (measured: 8px from its top, 8.4px from its bottom
  on a 52px box). The controls never stick out into the gap around the entry.
- **The gaps include the buttons.** The gap between a revealed add row and an entry is measured
  box-edge to box-edge, and since the box wraps the controls it brackets them: 8px above, 8px
  below, in every case.
- **Words are centred.** Content shorter than the box is centred exactly (measured 2.7px / 2.7px
  on the song card, 14.1px / 14.1px on a one-line entry); taller content defines the box's
  height.
- **Controls float at the top-right.** Unchanged spot and reveal; with a 52px box that spot is
  the box's centre. On a taller entry they overlay its first line(s) while shown — the approved
  trade for having no reserved band.
- **At rest, no parked space.** The start bar is collapsed (0px) like every row; the pane reads
  tighter than any prior spec. Opening it moves the first entry down once by the bar's revealed
  height minus the heading's 30px margin — 13.6px on one line, 47.2px when the five buttons
  wrap — and it stays put from then on (the 052 slide-under rule covers the wrapped case, where
  a short first entry can slide out from under a stationary pointer).
- **The divider takes the box.** A legacy END_OF_SECTION row and a `section_break` entry render
  the same 52px box with the rule at its centre and the note under the rule; margins 0.
  (Known edge, recorded for reviewers: a legacy row's operator note pins under the rule as
  before and can render a few pixels above the box's centreline — unchanged behaviour, not a
  regression.)

## Acceptance scenarios

### Scenario: At rest

- **Given** the pane with editors on
- **When** nothing is hovered or focused
- **Then** every add row and the start bar is 0px tall, and consecutive entry boxes sit 12px
  apart uniformly

### Scenario: Hovering the first entry

- **Given** the first entry with the start bar above it
- **When** I hover the entry
- **Then** the bar reveals 8px under the heading and 8px above the entry's words, the entry
  shifts down once — by the bar's revealed height minus the heading's 30px margin (13.6px on
  one line, 47.2px wrapped) — and stays settled, and the row below the entry keeps 8px above
  and below its buttons

### Scenario: Hovering the song card or a one-line entry

- **Given** an entry whose content is shorter than 52px
- **Then** its words sit centred (equal space above and below), the controls are wholly inside
  the box, and the rows on both sides hold 8px to the box

### Scenario: The divider

- **Given** a section break between entries
- **Then** the same 52px box holds the centred rule, rows on both sides hold 8px, and nothing
  flickers or oscillates

### Scenario: Keyboard and touch

- **Given** an entry holds keyboard focus
- **Then** the reveal matches the hover behaviour (bar/rows, 8px gaps); on a touch device the
  bar and every row are shown outright in the same geometry

### Scenario: A narrow window

- **Given** a width where the five add buttons wrap (1280px measured)
- **Then** the row grows to its wrapped height and the gaps stay 8px above and below

## Traceability

- Domain/app tests: N/A (pane layout; no server data).
- E2E: `tests/e2e/test_tatib_entry_controls.py` (rewrites + new), `tests/e2e/test_reorder.py`
  (the start bar reveals before it is clicked), `tests/e2e/test_tatib_section_break.py`,
  `tests/e2e/test_tatib_hover.py`, `tests/e2e/test_entries.py`.
- Implementation: `static/styles/design/components.css`, `static/web/entries.js`,
  `multimedia/web/templates/reading/tatib.html` (`.entry__start-inner`).
- Amends: spec 030 (the bar is no longer always visible), spec 035 (the break's margins),
  specs 036/037 (reveal triggers unchanged; the open row's margins are neutralised),
  spec 052 (10px → 8px; the resting rhythm), spec 053 (the 44px band → the 52px containing box).
- Pairs with: spec 054 (the verse line inside the box), spec 056 (link colours).
