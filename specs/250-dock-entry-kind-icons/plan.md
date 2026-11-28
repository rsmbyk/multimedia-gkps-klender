# Plan: entry-kind icons in the OBS dock

## Technical approach

1. `static/web/obs-dock.js` — add `ENTRY_KIND_MARKS` (the four glyph bodies copied from `reading/_toc_mark.html`) and `entryKindIcon(entry)`; append the mark to the row in `renderList()` before the chevron is appended. A break returns no mark. The pinned clones copy the whole row, so they inherit the mark unchanged.
2. `static/styles/design/obs-dock.css` — seat `.entryicon` at 16×16 with the row's own centring and `--head-ink`; move the trailing auto margin from `.entrychev` to the mark so the mark+chevron stay a single pair at the row edge. The live row switches the mark to `--ink` when its chevron hides.
3. `tests/e2e/test_dock_entry_kind_icons.py` — two browser behaviours: the kind/placement matrix across all five entry kinds; the live row's retained mark with no chevron.

No template, backend, migration or dependency changes.

## Verification split

`2 test · 1 inspection · 0 manual`

- **test** (2): the new E2E module; targeted regression cases from spec 198's chevron matrix, spec 203's header wrap and spec 208's stuck header.
- **inspection**: a live probe at 420×800, dark, 1× reads the mark/chevron/title boxes and the painted token colours; screenshots of a text-only and a mixed-kind service.
- The full browser matrix is deferred to the push step.

## Versioning

`bump: patch` (declared at Plan per SDD × Versioning). `VERSION` and the changelog line are written in the delivery commit, not here.

## Delivery

One PR carries the code, this spec pack, the card close and the patch bump. Nothing is pushed without the owner's word.
