# Data model: the drawer shell's state

**Slice**: `specs/138-sidebar-overlay-stack`

**No entity changes.** No model, migration, payload or stored value moves. What follows is the
shell's own state — the attributes the stylesheet and the script agree on — because that is the
whole data model of this slice.

## The four attributes, all on `<html>`

| Attribute | Values | Written by | Means |
| --- | --- | --- | --- |
| `data-nav` | `closed` · `mini` · `open` | server (first paint), `reading.js` | the first-level list: hidden, rail-width (desktop only), or open |
| `data-ch` | `closed` · `open` | server (first paint), `reading.js` | the second-level list: hidden or open |
| `data-rail` | `closed` · `open` | `reading.js` | **new** — the phone's menu drawer |
| `data-drawer-open` | present · absent | `reading.js` | **new** — set while any of the three is open; the stylesheet locks the page's scroll |

`data-section` (`alkitab | kidung | tatib`), `data-ch-mode` (`chapter | song`) and
`data-read` (`on | off`) are unchanged and keep their present meanings.

## The states a user can be in

| Width | State | `nav` | `ch` | `rail` | On screen |
| --- | --- | --- | --- | --- | --- |
| > 1272px | today's columns | `closed` / `mini` / `open` | `closed` / `open` | `closed` | unchanged: the stage is pushed by each column |
| ≤ 1272px | closed | `closed` | `closed` | `closed` | the stage; the rail |
| | first level | `open` | `closed` | `closed` | one drawer at the rail's edge |
| | first + second | `open` | `open` | `closed` | the second covers the first |
| ≤ 720px | closed | `closed` | `closed` | `closed` | the toolbar and the stage |
| | menu | `closed` | `closed` | `open` | the rail as a full-width drawer |
| | list over menu | `open` | `closed` | `open` | the list covers the menu, which stays underneath |
| | list alone | `open` | `closed` | `closed` | the list over the stage (opened from the rail on a tablet, or restored) |
| | contents over list | `open` | `open` | `closed` | the second level covers the first — never for Tata Ibadah on a phone |

## Rules over the states

- **One section.** `nav`/`ch`/`rail` never describe two sections at once: switching sections closes
  the previous stack first.
- **Depth is a prefix.** `ch = open` implies `nav = open`; `rail = open` implies `ch = closed` unless
  a list has been opened over it.
- **The control reads `anyOpen()`.** `menu` glyph when all three are `closed`, `close` otherwise.
- **Escape** sets all three to `closed`, in one write.
- **A resize above the breakpoint** clears `rail` and leaves `nav`/`ch` to the desktop's own rules.

## What the implementation must not change

`data-nav`'s `mini` value, `data-ch-mode`, `data-section` and `data-read` keep their present
vocabulary: the desktop's CSS and the rest of `reading.js` read them, and spec 137's inherited wrap
rule keys off `data-read`.
