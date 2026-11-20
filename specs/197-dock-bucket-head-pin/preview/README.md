# Preview — the bucket head, pinned

`index.html` is a static preview: two copies of the dock picker at 449×520, drawn by the product's own
`static/styles/design/tokens.css` and `obs-dock.css`, with the real picker markup
(`.dock__head`, `.dock__body`, `section[data-bucket]`, `h3.group__head`, `button.servicerow`) and rows read
off the running dock.

The two panes differ in two numbers:

| Pane | Declaration | Result |
| --- | --- | --- |
| Before | `.group__head { padding-top: 10px }` over `.dock__body { padding-top: 4px }` | the head's box starts 4px below the scroller's top; the row above paints in that strip |
| After | `.group__head { padding-top: 14px }` over a picker body with no top padding | the head's box starts at the scroller's top and its own padding is the sky above the label; the strip is covered |

The label's distance under the divider is 14px in both panes and in both states — only the strip's owner
changes.

## States the page reaches by hand

- **Pinned** (opens here) — *Pinned (98px)*: the readout under each pane prints the head's offset, the element
  painted in the strip and the air above the next label. Before reads `4.0px`, `span.servicerow__n` and
  `10.0px`; after reads `0.0px`, `h3.group__head` and `26.0px`.
- **Group boundary** — *Group boundary*: the same three numbers with the boundary in view, so the air above
  the second label can be judged on its own.
- **Rest** — *Rest (0px)*: the first head sits at the scroller's top in the after pane and 4px below it in the
  before pane; the label is 14px under the divider in both, and no row paints in the strip.
- **Long name** — the 64-character row wraps inside its column in both panes; this slice moves nothing
  horizontally.

## Live preview

The real page, at the reported size: `python manage.py runserver 127.0.0.1:8767 --noreload` in this
worktree, then `/obs/dock` at 449×604, dark theme, scrolled past the first bucket. `develop` answers the
same route on `:63404` for comparison.