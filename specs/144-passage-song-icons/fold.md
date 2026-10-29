# Fold: a passage and a song carry their own kind mark

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-10-28

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R24` | A passage and a song carry a decorative 20px glyph — open book, flagged note — on the media chip's centre line, with the title on the media title's 64px column; no other kind is marked, the mark is hidden from assistive technology and takes no pointer, and a song's title may take one more line where the narrower column wraps it. |

## Drift guard

- **Files changed in this capability**: `multimedia/web/templates/reading/tatib.html` (the row's kind
  class and the heading's mark), `multimedia/web/templates/reading/_entry_kind_icon.html` (new — the two
  glyphs), `static/styles/design/components.css` (the row's 64px column, the mark's seat, the narrow
  screen variant).
- **Header**: `last folded` stays 2026-10-28 (already today); `144-passage-song-icons` prepended to
  `slices`.
- **Declared no behaviour change**: no — one requirement added, none modified or removed.
- **Not touched, on purpose**: the sidebar's service list, the OBS dock's entry list, the projector and
  the preview modal — `R24` scopes the mark to the stage (FR-008).

<!-- A changed file with no delta is CRITICAL; Fold refuses to complete. -->
