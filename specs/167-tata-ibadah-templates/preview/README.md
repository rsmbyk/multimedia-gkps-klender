# Preview: a Tata Ibadah is a service or a template

**Spec**: `specs/167-tata-ibadah-templates/spec.md`
**Shape**: `static` — one page, the reading page's own markup, class names, tokens and stylesheets
**Open**: `specs/167-tata-ibadah-templates/preview/index.html` directly

The page is the template's own service page with three surfaces layered on it, reached from the
strip at the top. Nothing here fetches: the entries, the songs and the passage are the product's
own painted shapes, typed into the markup. The stylesheets are the working tree's
(`static/styles/design/{tokens,components}.css`), linked rather than copied, because this slice has
no "before" column to keep drawing — every state on the page is the state the slice proposes.

## States

| Surface | What to look for |
| --- | --- |
| Template page | `Template` in the eyebrow, no date, `Media files` + **Use template** where Project sits, no projector control; the two dashed fill-ins; the choice with its two indented options and `+ Add option`; six buttons in every add bar (`+ Fill-in` and `+ Choice` past a hairline). The two slot marks are one pair — a dashed rounded square with a plus (fill-in) and with a radio (choice); dashed means still to be filled or added, solid means content |
| Entry kinds | Every kind in every role on one sheet: Passage, Song, Text and Media as a fixed entry, as a fill-in, and as a choice with two options each — the specimen for the row anatomy below |
| Template page · Show add bars | Every seam's bar revealed at once — the state a touch device has, and the one that shows the six-button bar's geometry at any width |
| New Tata Ibadah | The Normal/Template switcher at the top of the modal, in the New text modal's own screen-mode component; Normal preselected, date present |
| New Tata Ibadah · Template | The date field is **absent**, not disabled — the switcher carries no help line |
| Edit Tata Ibadah | No switcher; `Copy as template` in the header, right of the title, with no helper note |
| Copy as template? | The confirmation that names the consequence; `Cancel` / `Copy as template` |
| Use template · step 1 | The order view-only, carrying every kind: text, song, passage and media as fixed rows and as fill-ins, and a text, a song and a passage choice. A fixed row uses the page's entry styles at the row's scale — 640 sans/14px heading, 14px serif body, 11.5px meta, 16px kind mark / 18px chip in a 24px gutter — at 52% opacity and inert; a slot row uses the template page's slot styles (600 sans/11.5px kind, 620 serif/17px title, sans/12.5px value). Two slots are title-less (the fill-in song and the passage choice): the kind line is the name and the value sits 7px under it. Every row's words start on the same 24px column. `Renungan` settled (`Change`), the other six slots live; **Next** disabled with `1 of 7 settled — 6 left to fill in`; the list scrolls |
| Choose · text / song / passage | Each choice opens its own chooser of the same component — a modal card with the editor's canvas fill, 12px radius, dialog shadow and the 1px `--divider` ring drawn in the shadow, so the card keeps its 560px width: its heading is the slot's title, or the kind when the slot is title-less; its options, `Preview` expanding the lyric, the prayer or the verses in place, and an explicit **Choose** per row. A passage option is its reference alone — no edition line and no repeated verse number; a text option is its title, the prayer behind `Preview`, and a title-less text is its opening line, muted and cut with an ellipsis |
| Chooser dismissal | With a chooser open, `Cancel`, Escape and a click on its backdrop each close the chooser **alone** — the generate modal stays open with every settled slot as it was, and focus returns to the row's `Choose`. Escape closes the modal only when no chooser is open |
| Use template · settled | All seven slots settled, `All 7 entries settled`, **Next** enabled; the chosen songs read `KJ 152 — Ada Kuasa · Bait 1, 2, 3` and `NKB 12 — Nyanyikanlah Nyanyian Baru · Bait 1, 4`, the verses after the dot muted; the text choice reads the body-only prayer's opening line (`Tuhan, sertailah kami…`), and the chooser also lists `Doa Damai` and `Doa Berkat` |
| Name and date | Step 1 marked done — a filled badge with a drawn check — then the normal Tata Ibadah form with the name prefilled and the nearest Sunday; `Ready to create.`; Back / Create. Badge marks are optically centred: the list's tracking is cancelled on the badge, the check is drawn rather than typed, and the digit nudge is scoped to ≥1.5dppx, where the glyph rasterises sub-pixel (measured 0.00/0.00 at 1dppx, −0.25/±0.5 at 2dppx) |
| Create this Tata Ibadah? | The confirmation naming the service, the date and that the template stays as it is |
| Add fill-in | The 480px modal: optional title/note, the four-chip kind picker with Text selected, the help line, `Add fill-in` / `Cancel` |
| Add choice | The same modal for a choice: optional title, the same kind picker, the help line noting options are added on the row afterwards, `Add choice` / `Cancel` |
| Empty choice | Use template with a choice that has no options: the row reads `No options yet`, its control is disabled (55% opacity) and labelled `No options`, and **Next** stays disabled with `one choice has no options` in the status |
| 900 / 420 wide | The generate frame at both widths, and the six-button bar at a 388px pane, where it wraps to two rows and becomes a plate |
| Use template · media & titles | The five media families as fill-ins, titled (`Family · Title`) and untitled (`Family · filename`); a titled and an untitled media choice; an untitled text choice beside the titled one. The media choosers list all five families (the titled one mixes a filename-only option); untitled rows show kind + value only, and a filename or a title-less text's opening line is drawn in the quiet ink |

`Dark` re-renders every state on the tokens (`--canvas #14130F` in dark); the new components hold
no colour of their own.

## Run

```sh
# none: open the file directly.
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/167-tata-ibadah-templates/preview/probe.py    # re-measure, refresh shots/
```

`probe.py` writes one screenshot per state into `shots/` (not committed) and prints every measured
box as JSON — the numbers the spec's `## UI/UX` section carries.

## What the page does not show

- **The Set modal.** `Set` in the product opens that kind's existing New modal (passage, song, text,
  media). Those forms are shipped components and this preview does not re-draw them; clicking `Set`
  here toggles the row between its unsettled and settled states so both are reachable.
- **The server.** Nothing is created, copied, stored or refused: the two confirmations close their
  dialog and print a line in the harness strip. The atomic create, the template's immutability and
  the slot-kind enforcement are behaviour, verified by tests, not by this page.
- **The panels.** The left sidebar's dated/Templates lists and the copy's landing on the new
  template are navigation, drawn by the app's own lists; the preview carries the stage alone.
- **The projector guard.** The page has no projector control; `/projector?service=<template>` and
  the OBS dock's list are server behaviour, outside a static page.
