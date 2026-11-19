# Research: A whisper of a tint on an open entry header

**Spec**: `specs/206-dock-expanded-tint/spec.md`
**Unknowns remaining**: 0

## D001 — How the wash is expressed

- **Decision**: `background: color-mix(in srgb, var(--rail-bg) 96%, var(--ink))`.
- **Rationale**: `.nextband:hover` in the same sheet already writes a subtle fill this way at
  92/8 (`obs-dock.css:651`), so "4 % ink on the rail" is legible as *half the hover tone* in the
  source, not just in a comment. The dock is uniformly `--rail-bg`, so an opaque mix is exact, and
  the resolved colour is a plain RGB triple in both themes — measurable in the E2E without a
  compositing step.
- **Alternatives**: `color-mix(in srgb, var(--ink) 4%, transparent)` — rejected: it re-introduces
  alpha compositing where the sheet's own precedent is an opaque rail mix, and the row would then
  depend on whatever sits behind it. `rgba(31, 31, 29, .04)` / `rgba(255, 255, 255, .05)` — rejected:
  two literal colours to keep in step with the ink token by hand, which is the drift the tokens
  exist to prevent.

## D002 — Token or literal

- **Decision**: no new token; the percentage lives in the rule.
- **Rationale**: one consumer. `.nextband:hover` sets the same precedent for a one-consumer tone.
  A token would also force the light and dark halves to be written twice, since a token cannot mix
  two other tokens per theme without duplicating the expression.
- **Alternatives**: `--entry-open-bg` in `tokens.css` — rejected as ceremony for a single rule; it
  would name a number nothing else shares.

## D003 — Where the rule sits

- **Decision**: between the base `.entryrow` block and `.entryrow:hover`.
- **Rationale**: `.entryrow[aria-expanded="true"]`, `.entryrow:hover` and
  `.entryrow[aria-current="true"]` all weigh (0,2,0). Only source order separates them, and the
  order the dock needs is base → wash → pointer → live. This was confirmed the hard way while
  building the preview: appended after the sheet, the rule beat both `.entryrow:hover` and the live
  row, so an open header under the pointer showed the wash instead of the pointer face, and the live
  row lost its green fill. Spliced in at its shipping position, all three states compute correctly.
- **Alternatives**: `:where(.entryrow[aria-expanded="true"])` to drop the weight — rejected: it
  would fall to (0,1,0) and tie with the row's own base rule, making the page depend on which of two
  equal rules is later; and the mechanism would be invisible to the next reader. Raising the live
  rule's weight instead — rejected: it edits CSS that spec 198 accepted, for no gain.

## D004 — What the pointer does to the wash

- **Decision**: the hover face replaces the wash; it is never composited with it.
- **Rationale**: a blend needs a third tone for "open and hovered", which no other pair of states in
  the dock has — the one precedent, `.entryrow[aria-current="true"]:hover`, exists because the live
  fill is opaque and would otherwise be replaced, not because states are blended. The chevron still
  says *open* while the pointer is on the header.
- **Alternatives**: `color-mix(in srgb, var(--rail-bg) 92%, var(--ink))` on open+hover — rejected:
  a fourth tone to name and test, for a state the pointer already answers.

## D005 — Motion

- **Decision**: add no transition; the row's `transition: background var(--ease)` carries the wash.
- **Rationale**: `paintEntry` sets `aria-expanded` when the block starts growing
  (`static/web/obs-dock.js:578`), so the 200 ms background ease and the block's growth start
  together. Reduced motion already governs the row's background the way it governs every other row
  state; a slice about a fill has no business adding a reduce story.
- **Alternatives**: a 120 ms fade of its own — rejected: two durations on one property in one row.

## D006 — How the E2E proves the colour

- **Decision**: compare `getComputedStyle(...).backgroundColor` against an in-page probe whose
  background is the same expression, exactly as the spec 198 live-tone assertion already does
  (`test_obs_dock.py:918`).
- **Rationale**: Chromium serialises `color-mix()` as `color(srgb r g b / a)`, so a literal string
  assertion would encode a serialisation detail. The probe states the intent — "the row wears the
  mix it names" — and survives a browser changing its serialisation.
- **Alternatives**: assert `#E5E2DB` — rejected: brittle, and false the moment a token changes by one
  level. Assert channel deltas only — rejected: it would pass on the wrong colour with the right
  contrast.

## Provenance

- The percentage: owner's gate-1 decision, 2026-11-19, choosing 4 % from the three previewed
  strengths — owner decision; the preview is the evidence.
- The expression, placement and token question: the sheet's own precedent — `obs-dock.css:641`
  (`[aria-current]:hover`), `:651` (`.nextband:hover`), `:369-395` (the three equal-weight rules).
- The hover interaction: research settled it from the cascade, no question asked; recorded as an
  assumption in the spec.
