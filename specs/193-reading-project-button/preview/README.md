# Preview — Project button on the song and Bible pages (spec 193)

Static preview at `specs/193-reading-project-button/preview/index.html` — open it directly in a
browser (or `::preview{file=specs/193-reading-project-button/preview/index.html}` in the desktop
chat). Assembled from the product's real header markup, stylesheet rules and tokens
(`components.css`, `tokens.css`); dark mode by default with a light/dark toggle over the real token
values.

## States shown

1. **Song page, hymn song** — eyebrow `PKJ 4`, the Project control at the right end of
   `read__head-top` (US1).
2. **Song page, ordinary songbook song** — eyebrow is the songbook's name (US1).
3. **Bible chapter page** — eyebrow hidden (Bible pages render none); the control sits in the
   title row at its right end, immediately right of the TB/SIM switch (US2). The
   `data-goto-edition` attribute shows how the page's shown edition reaches the pointer.
4. **Tata Ibadah today** — the unchanged comparison: the date eyebrow, the reopen icon control and
   the Project/Stop toggle this slice ports from (anatomy reference).
5. **States strip** — rest, hover, focus-visible of the new control, plus the ≤720px note: resize
   the browser window below 720px and every sample's control disappears (the rule FR-007 joins,
   components.css:3202).
6. **Markup block** — the exact `read_actions` markup the two templates would carry.

## Bound

A static page shows markup, CSS and states but not what fetches: the click act — writing the Go To
pointer via `display.js`'s `goTo`, the `{type: 'goto'}` broadcast, and opening or focusing the named
`gkps-projector` window — is demonstrated live on the worktree dev server during the
implementation review, not here.
