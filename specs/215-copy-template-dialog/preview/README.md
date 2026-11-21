# Preview — spec 215

`static preview at specs/215-copy-template-dialog/preview/index.html`. Open it over `file://`.

Built from the real materials, as SDD-06 asks:

- `fragments.json` — `#editorContent`'s innerHTML, read off the running dev server for a service
  (304) and a template (151). `build.py` puts them into the page verbatim, with the CSRF token
  replaced, the form's `action`/`method` removed (a static page has no server) and the confirmation
  the server still renders inside the body cut out — this slice replaces it.
- `tokens.css`, `components.css` — copies of the product's own stylesheets.
- `preview.css` / `preview.js` — the page's harness, and the one new component: the confirmation's
  layer and card. The layer is `position: fixed; inset: 0`, which is the change; the card's numbers
  are the accepted preview's.

Rebuild after re-reading the fragments:

    .venv/bin/python specs/215-copy-template-dialog/preview/build.py
    .venv/bin/python specs/215-copy-template-dialog/preview/probe.py     # prints every cited number

## States

| Key | |
| --- | --- |
| `1` | the Edit modal alone |
| `2` | the copy confirmation over it |
| `s` | service dialog (480 × 312.5, Name + Date) ⇄ template dialog (480 × 241.3, Name only) |
| `t` | dark ⇄ light |
| `Esc` | closes the confirmation only |

Clicking the scrim closes the confirmation; clicking the card does not. Clicking the Name field
selects the whole value; a second click places a caret. Emptying it disables **Copy as template**.

## Measured (960 × 780 window, both themes, both dialog sizes)

| | |
| --- | --- |
| layer | 960 × 780 at (0, 0) — `position: fixed` |
| card | 448 × 349.7 at (256, 215.1) — centred on the window |
| Edit dialog behind | 480 × 312.5 at (240, 208.6) service · 480 × 241.3 at (240, 244.3) template |
| card padding / radius | 22px 22px 20px / 14px |
| heading | 404 × 22.5, 650 18px/22.5 |
| lead | 404 × 41.8, 13.5px/20.925 |
| Name field | 404 × 38, 500 14px/18.9 on `--rail-bg` |
| facts | 404 × 84.1, three 19.4px rows at 12.5px/19.375 |
| answers | 404 × 38 — Cancel 81.6, Copy as template 150, 8px apart, 22px inside the card's right edge |
| dialog height | unchanged on open and on close (312.5 / 241.2) |

`shots/` is gitignored.
