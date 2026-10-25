# Fold: The Break kind retires, and the breaks already written stay

**Capability**: `reading` ([`docs/spec/reading.md`](../../docs/spec/reading.md))
**Folded at**: 2026-10-25

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| modified | `R6` — an empty Tata Ibadah quarter-centres its add tiles | five add actions → four: the Break tile leaves the row, the label list loses `Add Break`, the grid drops to four tracks, and the narrow fallback reads three and one instead of three and two. The requirement's title follows the count. |
| added | `R8` — a retired entry kind stops being offered, and what it wrote keeps working | no creation control on any of the three surfaces; the writing endpoints answer `404`; an existing break still draws its divider and sidebar row, contributes its projector screen, reorders and deletes; the stored kind value and display name stay; the legacy `END_OF_SECTION` row is untouched |

`R6` is **modified**, not duplicated: the capability doc states current behaviour, and the current behaviour of the
empty service is four tiles. The five-tile text stays in `specs/130-empty-service-tiles/` as that slice's record.
`R1`–`R5` are untouched.

`R8` is the next free number: `develop` carries `R1`–`R6` (130's tiles are `R6`), and the unmerged 129 slice took
`R7` on its own branch when it rebased onto `3a360d06`. A number is claimed on a branch and never reused; if 129
has not merged when this slice does, `R7` simply arrives later, out of order but never renumbered.

## Repair made during the fold

`R6`'s paragraph and its four scenarios appeared **twice** in the file, the two copies differing by one word
("the same row of tiles" / "the same centred row of tiles"). This fold writes `R6` once. That is a documentation
defect repaired, not a behaviour change: both copies said the same thing, and the surviving copy is the one
whose wording matches the shipped block.

## Drift guard

- **Files changed in this capability**: `multimedia/web/templates/reading/tatib.html`,
  `multimedia/web/templates/reading/_entry_form.html`, `multimedia/web/reading/entries.py`,
  `static/styles/design/components.css`, `static/web/entries.js`, `static/web/offline-render.js`
- **Declared no behaviour change**: no — the retirement is `R8`, and the tiles' count is `R6`'s own sentence
- **Guard result**: every changed source file is named by `R8` (the control, the map, the scripts) or by `R6`
  (the tile row's tracks). `views.py`, `_toc.html`, the model and the search module were read and are unchanged,
  which is what `R8`'s second paragraph promises. The test files and the slice's docs are the record, not
  behaviour. No other reading surface was touched, so nothing outside the tree can have drifted.
