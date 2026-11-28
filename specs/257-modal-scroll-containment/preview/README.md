# Preview — spec 257

## Static (hand-drivable)

`index.html` — open it directly (`file://`). It carries the real editor/Preview dialog markup and
the real design CSS: `build_preview.py` inlines `tokens.css`, `fonts.css`, `generate.css` and both
copies of `components.css` (base commit `1cd9f081` and this worktree), so the control cannot silently
become a second "after".

- **Before (base CSS)** — default. Open the editor, scroll its 40 rows to the end, then keep
  wheeling: the page behind moves. Open the picker and wheel its options to the end: the editor
  content behind them moves.
- **After (slice CSS)** — toggle the button, repeat both actions: the page and the editor content
  stay still, while the focused scrollport still reaches its own end.
- **No range** — the "Open editor" button fills 40 rows. To see the zero-range case, open the static
  page's short variant by clearing `editorContent` in DevTools, or use the live A/B probe below,
  which drives the short case deterministically.
- **Preview dialog** — "Open preview" repeats the same check in `.preview__body`.

The readout at the bottom right shows `scrollY`, root `overflow-y`, the focused scrollport's
`overscroll-behavior-y` and both scroll offsets live.

## Live A/B (measured)

- After (slice worktree): `http://127.0.0.1:8765/`
- Before (unmodified `1cd9f081`): `http://127.0.0.1:63404/`

`probe.py` drives both with the same viewport and wheel steps, printing one JSON object per case:

```
<venv>/bin/python specs/257-modal-scroll-containment/preview/probe.py
```

`geometry.py` checks that opening and closing a dialog moves neither the document width, the dialog
box nor the scroll offset:

```
<venv>/bin/python specs/257-modal-scroll-containment/preview/geometry.py
```

Both scripts use synthetic scrollable content so the two servers' own pages (which have no document
scroll at this viewport) are comparable; the CSS under test is the CSS each server actually serves.
