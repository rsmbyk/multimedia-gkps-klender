# Fold: entry-kind icons in the OBS dock

**Capability**: `docs/spec/dock.md`
**Folded at**: 2026-11-28

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R20` | New requirement: every non-break entry header carries one 16px kind mark immediately left of its chevron — book for passage, note for song, play-frame for media, rules for text — using the product's own contents-row glyphs. The mark is decorative, keeps the chevron trailing and centred on a wrapped row, and stays at the trailing edge in the live ink when the chevron hides. Three scenarios: the mixed-kind service, a multi-line header, the live header and its clones. (spec 250) |

## Operations

- Header moved `last folded` from 2026-11-25 to 2026-11-28 and prepended
  `250-dock-entry-kind-icons` to the `slices` line, keeping every incoming slice ID in place.
- One `added` block, `R20`; no `modified`, `removed` or `renamed` operation. `R3` (expand state),
  `R14` (header names its block) and the two pin requirements keep their own wording — the mark
  changes what the header shows, not what a click does.
- The pinned clones copy the whole `.entryrow`, so the mark rides them without a second writer;
  no pin rule needed editing.

## Evidence

- The new E2E module `tests.e2e.test_dock_entry_kind_icons` was red before the writer and green
  after (2 tests), covering the kind matrix, placement, break rows and the live row.
- Targeted regressions: spec 198's chevron matrix, spec 203's header wrap and spec 208's stuck
  header each green (3 cases). The full browser matrix is deferred to the push step.
- Live probe at 420×800, dark, 1×: mark 361–377px, chevron 387–402px, 10px gap, 0px off the
  row centre; 3-line media row 76.7px, 2-line song + Bait row 77px, 4-line media row 96.3px.
- Before / after counts: `### R` blocks 19 → 20; `#### Scenario` entries 75 → 78; `slices` entries
  11 → 12.
- Capability diff (`git diff --numstat`): 30 insertions, 2 deletions — only the header and R20.

## Drift guard

- **Files changed in this capability**: `docs/spec/dock.md` only.
- **Declared no behaviour change**: no — the header now paints a kind mark it did not paint
  before; the capability file carries the new requirement.
