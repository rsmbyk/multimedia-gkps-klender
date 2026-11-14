# Research: a Tata Ibadah sidebar row is three lines, ellipsized

**Slice**: `specs/135-tatib-sidebar-row-clamp` · **Date**: 2026-10-26
**Exit**: zero unknowns.

## D1 — The cap lives on one box per label, not on each line

**Decision.** The row's label becomes a single clamped block: `display: -webkit-box;
-webkit-box-orient: vertical; -webkit-line-clamp: 3; overflow: hidden; overflow-wrap: anywhere;
min-width: 0;` on `.songrow__t`.

**Rationale.** The request is a height cap over text that word-wraps, so the unit is the line box,
not the source line. Every kind already renders its text into `.songrow__t`, so one rule reaches
text, media, passage, song, section break and the legacy rows — the "same as all kinds" the owner
asked for. `overflow-wrap: anywhere` is what turns an unbroken run (the Drive link in service 143)
from an overflow into a wrap; measured on the unchanged page, that label's `scrollWidth` was 422px in
a 311px box with `overflow-wrap: normal`.

**Alternatives.** `max-height` + `overflow: hidden` — cuts a line box in half and draws no ellipsis.
`text-overflow: ellipsis` — single line only. Server-side character budgets — do not know the pane's
width, and the owner explicitly removed the character cap.

**Provenance.** Browser measurements on the preview; `static/styles/design/components.css:1605-1613`;
`multimedia/web/reading/views.py:1082-1106`.

## D2 — A song's heading and its `Bait …` line are two blocks inside the clamped box, with no `<br>`

**Decision.** `.songrow__t--song` holds `.songrow__heading` and `.songrow__verses` as sibling blocks;
no line break element between them. The heading is clamped at two lines when a `Bait …` line exists:
`.songrow__t--song:has(.songrow__verses) .songrow__heading { display: -webkit-box;
-webkit-line-clamp: 2; }`.

**Rationale.** The owner's decision at Clarify: the `Bait …` line counts as one of the three, so the
heading spends at most two — it must never push the line out. Measurements on the real markup: a
`<br>` between heading and `Bait …` is itself a box item and adds a fourth line (label box 80px where
the same content without it is 60px); a heading capped at two lines with the `<br>` kept still hid
the `Bait …` line behind the container clamp.

**Alternatives.** Clamp only the container (heading takes three lines, `Bait …` disappears) — that
was the first draft, and the owner rejected it. Clamp the heading with its reference/title spans as
children of the clamped box — WebKit blockifies them, so `PJ 606` lands on its own line above the
title.

**Provenance.** Owner answer at Clarify (2026-10-26); four browser probes recorded in the preview
directory's history; `components.css:1608-1613`.

## D3 — Two ellipsis paths, one visible result

**Decision.** The browser draws `…` where the clamp truncates; the server appends a literal `…` to
the last line it keeps when it drops body lines, reusing `_clamped_paragraphs`'s `clipped` flag.

**Rationale.** A five-line body cut to three at the server ends exactly at a line boundary, so the
browser has nothing to clamp and would show no ellipsis, while text is in fact hidden. Conversely a
three-line body whose third line wraps is clipped only by the browser. Both paths must end in `…`, so
both exist.

**Alternatives.** Send the whole body and let the browser clamp — the DOM would carry every line of
every text entry, which the stage already refuses to do. Append the `…` always — it would decorate
rows that show everything, which the spec forbids.

**Provenance.** `views.py:929-943` (`PANE_TEXT_LINES`, `_clamped_paragraphs`); preview cases 12 and
18 (literal) against 21-23 (browser).

## D4 — The payload carries lines, not a capped string

**Decision.** A `toc_items` entry carries `label_lines` (a list, one string per line) for every row,
and keeps `label` as the plain, space-joined text used by the grip's accessible name. `two_line_label`
is removed.

**Rationale.** Presence of line breaks is now a property of every row, so a boolean that says "this
row has two lines" no longer describes anything. A list also lets the template and the saved renderer
emit `<br>` between lines without re-splitting a string, and keeps the grip's label readable (a
newline inside `aria-label` is not).

**Alternatives.** Keep `label` with `\n` and split in the template — Django's autoescape would need
`linebreaksbr`, which adds `<p>` markup; the saved renderer would re-implement the split.

**Provenance.** `multimedia/web/templates/reading/_toc.html:20-26`;
`static/web/offline-render.js:596-612`; `views.py:1095-1106`.

## D5 — The legacy row follows the Text entry

**Decision.** Without a title, a legacy `TataIbadahItem` row carries the first three body lines;
with a title, the title alone; its 60-character cut and its appended `…` are gone.

**Rationale.** The owner's decision at Clarify. The old rule (`title or first line`, cut at 60 plus
`…`) is what put the 81-character Drive link in service 143 into a clipped single line.

**Alternatives.** Keep the first line only — leaves the row one line tall while every other kind now
uses three.

**Provenance.** Owner answer at Clarify; `views.py:1016-1018`; service 143 row 1 in the database.

## D6 — Where each piece lands

**Decision.** Server: `multimedia/web/reading/views.py` (`_tatib_stage`). Template:
`multimedia/web/templates/reading/_toc.html`. Styles: `static/styles/design/components.css`, beside
the row's existing rules. Saved copy: `static/web/offline-render.js`. No model, token, font or icon
change.

**Rationale.** Each file already owns that part of the row; the stylesheet holds `.songrow`'s rules
together, and the saved renderer is the fourth place that draws a row (after the template, the
in-place rebuild in `reading.js`, and the drag ghost, which clones the row).

**Provenance.** `reading.js` clones `#chList` rows for the drag ghost (`.reorder__ghost`), so it
inherits the change without an edit.

## D7 — No new unknowns

The pattern (line-clamp + `:has()`) is already used in this stylesheet (`.editor:has([data-editor-size="large"])`),
so browser support is the project's existing baseline. Nothing in the slice needs a decision the
owner has not already taken.
