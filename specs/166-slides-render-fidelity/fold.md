# Fold — spec 166

**Capability**: `media-library` · **Operations**: added R2, R3, R4 · **Before**: 1 requirement ·
**After**: 4 requirements.

| Requirement | Operation | Why |
| --- | --- | --- |
| `media-library/R2` — a converted deck keeps the deck's own layout | added | The conversion had no requirement: the tree began with the transfer dialog's drawing rules, so "a deck is converted" carried no statement about what the result looks like. |
| `media-library/R3` — a derivative is named after the renderer that made it | added | New behaviour: the key covers the version, the converter revision and the font inventory. Previously the version alone. |
| `media-library/R4` — the operator can add the faces only Office has | added | New interface: a mounted directory, re-scanned at start. |

**Not folded — accepted gaps** (from `converge.md`):

- F1, the Office display faces' substitute differing between the image and the reference machine. R2
  carries the substitute clause; the closing of it is R4's subject, not a behaviour this slice owes.
- F2, sub-pixel antialiasing differences on four pages.

**No behaviour change** in `projector/R7`: the projector paints whatever PDF the companion serves, and
that is what it did before.

Counts: 1 → 4 requirements; `last folded` moved to 2026-10-30; the slice ID prepended to `slices`.
