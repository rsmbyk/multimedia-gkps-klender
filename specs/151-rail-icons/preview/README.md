# Rail icons — preview

`preview.html` is the **static preview** for `specs/151-rail-icons/spec.md`: the live app's own rail
and Tata Ibadah stage, at 1:1, in two columns.

| Column | What it is |
| --- | --- |
| **Now — develop** | the rail and stage exactly as `24a6d6d2` renders them |
| **Proposed** | the same DOM with the slice's four marks swapped in |

The top bar switches each mark between the proposal and its alternative, so every candidate in the
spec is reachable by hand; the **Dark** button flips the whole page to the dark theme.

Both columns are 502px wide: an 80px rail beside a 420px stage. The rail scrolls with its stage.

## How it is built

    ~/Projects/multimedia-gkps-klender/.venv/bin/python \
      specs/151-rail-icons/preview/build_preview.py [--url URL]

- The markup is fetched from the running app (`http://127.0.0.1:63404/tatib/144/`, the compose `web`
  container on `develop`) — it is the page's own rail and its own `<article class="read">`, not a
  reconstruction.
- The stylesheets are frozen at `24a6d6d2` (`assets/tokens.css`, `assets/components.css`), the commit
  this slice branched from, so the **Now** column cannot drift with the working tree.
- The other media families are read out of `static/web/media-stage.js` at build time, so the preview
  cannot invent a mark the product does not draw.
- The proposed marks live in this file's `GLYPHS` table; they move into the templates when the slice
  is implemented.

`assets/` and `preview.html` are generated — edit `build_preview.py`, not them.
