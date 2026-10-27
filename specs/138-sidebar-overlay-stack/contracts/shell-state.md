# Contract: the shell's state attributes

**Slice**: `specs/138-sidebar-overlay-stack` · Producer/consumer: `static/web/reading.js` →
`static/styles/design/components.css`

The script writes the attributes; the stylesheet reads them. Neither may assume a value the other
does not write. This is the one interface the slice adds.

## The attributes

| Attribute | Allowed values | Who may write | What the stylesheet promises for each |
| --- | --- | --- | --- |
| `data-nav` | `closed`, `mini`, `open` | server on first paint, then the script | `closed`: no first-level drawer. `mini`: the desktop's rail-width panel (ignored at the overlay width). `open`: the first-level drawer at the rail's edge |
| `data-ch` | `closed`, `open` | server on first paint, then the script | `closed`: no second-level drawer. `open`: the second-level drawer, covering the first |
| `data-rail` | `closed`, `open` | the script only | `closed`: no menu drawer. `open`: the rail as the phone's full-width menu; at `>720px` the value is ignored and the rail is the strip |
| `data-drawer-open` | present, absent | the script only | present: the page behind the drawers does not scroll; absent: it scrolls |

## Rules

1. **`data-rail` is the only value with no server-side meaning.** The menu is a phone state; a
   page rendered on the server never carries it, and at `>720px` the stylesheet ignores it.
2. **Depth is a prefix.** The script never writes `data-ch="open"` with `data-nav="closed"`.
3. **`data-drawer-open` is written once per transition** from the three-level test, never per level.
4. **The stylesheet never requires a value it does not document here.** A new state is a new row in
   this table, added with its CSS in the same commit.
5. **`data-nav="mini"` is desktop-only.** At `≤1272px` the script never writes it; the stylesheet's
   mini rules stay for the desktop.

## Compatibility

Everything the desktop reads today — `data-nav`, `data-ch`, `data-section`, `data-ch-mode`,
`data-read` — keeps its vocabulary. The slice adds two attributes and removes none, so a stale page
rendered before the deploy still lays out correctly.
