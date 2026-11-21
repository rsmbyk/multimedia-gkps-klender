# Song entry modal — picker previews

Open `song-verse-picker-preview.html` (self-contained) or `index.html` (needs the sibling
CSS/JS). Markup and classes come from the product's `#editorModal`; preview-only CSS unpins
the fixed dialog/menu and adds the reveal. Tabs 1–4 compare verse-picker models; tab 5 is
the combined direction being carried into the Draft.

## Tab 5 — combined song search + verse tiles

- The Song field is a live search from the first frame of the modal; the input has focus on
  open, so typing works without a second click.
- Results narrow as you type (title, number, book name, `kj 12`-style reference), grouped by
  book with a short reference and title on each row. Backend ranking, book-first order and
  the 200-result cap are unchanged.
- The list is a fixed overlay anchored to the field and capped to the viewport (spec 040):
  the modal height stays constant as results grow, shrink or disappear. The list may run
  past the modal's bottom edge; it is capped only by the window edge. The side readout
  shows the measured modal height.
- Arrow keys move through results, Enter picks, Escape closes the list; tapping a row picks
  it on touch.
- Picking a song turns the field into its chosen label and reveals the verse field in the
  same 200ms motion; `Slow` / `S` stretches it to 900ms for watching. A song with no verses
  leaves the field hidden; a one-verse song leaves it muted.
- Fresh pick starts with verse 1 ticked. Editing an existing entry preserves its saved
  verses (owner decision).

## Tab 1 — verse tiles + checkbox behavior

- Tile layout and styling: five tiles per row; a plain click ticks or unticks one verse.
- Press and drag across tiles to extend a range: the range is previewed while the button is
  held and committed on release; no mark stays on the tiles afterwards.
- The Verses field is inline in the modal — no dropdown trigger or floating menu — with the
  tile grid, with the summary line (`Verses 1`, `All verses`, ...) inside the same section and
  a hairline between that line and the controls below it.
  It is hidden while no song is picked; a one-verse song mutes it.
- `All` disables at all-ticked, `Clear` at none-ticked.
- No-verses song hides the whole Verses field; one-verse song leaves one muted tile.

Tab 6 is the same behavior with a soft-trigger look: a flat summary row, no chevron or box,
and the tiles under a thin rule. Compare it with tab 1's visible panel.

Tabs 2 (`From / To` chips), 3 (typed range) and 4 (enlarged checkboxes) stay as comparison
points from the earlier four-option review; they are not part of the carried design.

## Reachable states

- Song: none (field collapsed) · picked · no verses (field collapsed) · one verse (muted).
- Selection: verse 1 only · `1–3, 5, 8–10` · none (invalid, inline error) · 24 verses.
- Controls: All/Clear enabled and disabled; press-and-drag range; song search empty query,
  title query, number/book query and no-match.
- Theme: dark by default, light via `T`. Navigation: `1`–`6`, `←`/`→`, `S`; hash
  deep-links each tab.

`build_standalone.py` regenerates `song-verse-picker-preview.html` after any edit.
