# Preview: a long transfer name ellipsizes instead of moving the row

**Spec**: `specs/147-transfer-icon-column/spec.md`
**Shape**: `static` — four panels of the real dialog, opened directly
**Open**: `specs/147-transfer-icon-column/preview/preview.html`

## Run

The page is self-contained — no server. Regenerate it from any running copy of the page whose
Transfers dialog holds both short and long names (here the local compose stack on `:63404`):

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/147-transfer-icon-column/preview/build_preview.py \
  http://127.0.0.1:63404/media-library/
```

## What is real, and what is frozen

- **The markup is the page's own.** The builder opens the running page, clicks the Transfers button,
  and copies `#mediaTransfersList`'s children after the page's own script has drawn them — the nine
  companion jobs, the upload glyph, the `Completed` labels. Nothing is transcribed.
- **The stylesheets are frozen at `05379336`** (develop, immediately before this slice). The
  comparison has to keep drawing the shipped rows in its **Now** panels after the fix lands in the
  working tree; linking the live stylesheet would turn Now into a second Fixed.
- **One declaration is added to the Fixed panels only**: `[data-option="fixed"] .media-transfers__mark
  { flex: none; }`. That is the whole proposed change; the implementation writes the same declaration
  on `.media-transfers__mark` itself.
- **The 382px panels** emulate a 420px window. The app's rule gives `min(580px, 100vw - 32px)` = 388px
  there, and Chrome's own dialog `max-width: calc(100% - 6px - 2em)` caps the rendered box at 382px —
  so 382 is what a person actually sees. The panel sets that width directly rather than shrinking the
  whole page, because the dialog is the only surface this slice touches.
- The dialog's 190ms scale-in is disabled in the preview chrome: measured mid-flight, 32px of column
  reads 31.04px and every number in the readout is 0.97 of its true value.

## The readout

Under each dialog the page measures, across that panel's nine rows: how many names truncate, the set
of mark widths, and the smallest / largest left edge of the glyph, of the name and of the status
label. A non-zero spread turns red — that is the defect, and the Fixed panels must show `0.0px`.

Numbers as generated (2026-10-28):

| Panel | Mark column | Glyph spread | Name / label spread | Truncating |
| --- | --- | --- | --- | --- |
| Now, 580px | 32 / 21 / 22.75px | 5.5px | 11.0px | 2 of 9 |
| Fixed, 580px | 32px | 0.0px | 0.0px | 2 of 9 |
| Now, 382px | 32 / 21px | 5.5px | 11.0px | 3 of 9 |
| Fixed, 382px | 32px | 0.0px | 0.0px | 3 of 9 |

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| Short names only | the Now/Fixed panels' first, third, sixth to ninth rows | the column already holds; both columns agree |
| A name that truncates | rows 2 and 4 (`side-view-…`, `Sujud & Terima Kasih…`) | Now: the glyph sits 5.5px left and the text 11px left. Fixed: on the line, name ending `…` |
| The narrow dialog | the two 382px panels | three names truncate, the column still holds at 0.0px |
| Empty list | not in the preview — the static page has no companion. Reach it live: stop the media companion, open `/media-library/`, press the Transfers button | the paragraph keeps its place; this slice changes nothing about it |
| An active transfer | not in the preview — needs a running job. Reach it live during an upload | label reads `42%`, geometry unchanged |
| The rail's own list | not in the preview — reach it live by clicking the rail button instead of the dialog's | same rows, same geometry |
