# Research — spec 246

## Decision

Render the Media Library page with `data-section="media-library"` by adding that one key to the
view's template context.

## Rationale

The shell chooses between *toggle the own section* and *fetch another section* by comparing a rail
tile's `data-panel` with the live document root's `data-section`. The Media Library page inherits
the base template's default `alkitab`, but its template fills only the stage blocks — no
`#panelBody` rows and no child list. The shell therefore believes Alkitab is selected and toggles
an empty sidebar. A library-specific section value makes the comparison honestly report a section
change; the existing `navigate()` path then fetches the section root and paints real rows.

## Alternatives

1. **Guard the toggle branch in `reading.js` when the sidebar is empty.** Rejected: it patches a
   symptom at every rail click and defines emptiness as proxy for section identity; a genuinely
   empty Bible list would then fetch on its own tile click, changing `reading/R44`'s empty-state
   behaviour.
2. **Render the Bible sidebar into the Media Library page.** Rejected: it duplicates a list the
   stage does not use, changes the approved preview's stage and needs another fetch to stay current.
3. **Keep `alkitab` but mark the rail tile as unselected.** Rejected: the shell has no separate
   selected-tile state; the section value *is* that state, and a second flag would drift.

## Provenance

- Gate-1 preview measurements in `preview/probe.py`: base and fixed request counts, section values,
  sidebar row counts and empty-state visibility at 1440×900, dark mode, 1×.
- `multimedia/web/templates/reading/base.html` line 8 — default section is `alkitab`; lines 227–245
  — the sidebar and empty-list nodes the library template leaves empty.
- `static/web/reading.js` — `railBtnClick`'s section comparison and `applyPage`'s section adoption.
- `docs/spec/reading.md` `R62` — the Media Library tile's in-place fetch and pending state, which
  this slice leaves intact.
