# Preview: an empty song names itself in the Verses section

Open `index.html` directly (self-contained). It is the product's own `#editorModal`
markup for the Add song form, its own `tokens.css` and the real editor/verse rules out of
`components.css`; only the toolbar, the state switcher and the proposed empty-state rules
are preview-only. `python3 build.py` regenerates `index.html` after any template edit.

## States (switch in place; measurements are live at the bottom)

| Button | What it shows | What to read |
| --- | --- | --- |
| **No song** | today's collapsed field | panel 0 px, label `none`, summary `Pick a song first` |
| **Empty song · before** | spec 210's shipped state | panel 0 px — the sentence exists only in the markup, not on screen |
| **Empty song · proposed** | this slice | label visible, panel holding only `This song has no verses`, body `hidden`, bottom rule `0px` |
| **Song with verses** | unchanged full picker | ten tiles, helper and All/Clear visible, summary `Bait 1` |
| **One verse** | unchanged muted state | one tile, `data-muted=true` |

`T` toggles dark/light. The readout reports the rendered panel box, the label's computed
`display`, the summary text, whether the body rows are visible, and the summary's bottom
border width — the four numbers this change is about.

## What changes, exactly

- Server: the panel is no longer `hidden` for a verse-less song; it carries `data-empty=true`
  so the script and first paint agree. The label is no longer hidden with it.
- CSS: with `data-empty=true` the helper/All–Clear row, the tiles and the readout are not
  drawn, and the summary drops its 8px bottom spacing and 1px separator — nothing follows it.
- Script: `verseSummary()` hides the panel only when no song is picked, and sets
  `data-empty` from whether the checklist has boxes. All other lines, controls and save
  refusals stay as they are.
