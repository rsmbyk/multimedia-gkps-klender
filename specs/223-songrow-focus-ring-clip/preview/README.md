# Preview: Song-row focus ring at the list top

**Spec**: `specs/223-songrow-focus-ring-clip/spec.md`
**Shape**: static
**Open**: `specs/223-songrow-focus-ring-clip/preview/index.html` opened directly
**Live**: `http://127.0.0.1:8767/songs/1820/` — this slice's worktree, dark mode, 900×700.

## Run

none: open the file directly. It is built from the live page by `build_preview.py`, which copies
the project's real `tokens.css`, `components.css`, `generate.css`, fonts and assets into
`preview/assets/` and strips the product's scripts.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| current | choose **Current** — the builder pins `#chBody` back to the base's `padding-top: 0` — then click **Focus top row** and press any key | the ring's top edge is cut at y=130 where the row meets the scrollport |
| A · 3px space | choose **A · 3px space**, focus the row, press a key | first row moves to y=133; the same browser outline is drawn in full |
| B · inset ring | choose **B · inset ring**, focus the row, press a key | row stays where A left it (133px in the re-based preview); a 2px `--focus` ring is drawn inside it |
| unfocused | open the page, or click elsewhere after focusing | no ring on any row |
| pointer only | click a row without pressing a key | no ring; focus alone is not `:focus-visible` |
| selected / hovered | focus or hover the `aria-current="true"` row | the existing fills are unchanged |
| scrolled to last row | scroll `#chBody` to its bottom and focus the last row | bottom ring fits inside the existing 8px padding |
| responsive | resize to 1440×900, 900×700, 390×844 | the ring is complete at each width |
| theme | toggle the page theme control where available | the ring follows the theme's focus token in B, the UA outline in A |

## Live or static

**Static** — the markup, tokens, type and geometry are the product's own, captured from the live
page; only the candidate switcher and the focus button are additions. It shows CSS state; it cannot
show a fetch or a server-rendered change, neither of which this slice makes.

## What is not a preview

A screenshot, a static image and a recording are not previews.
