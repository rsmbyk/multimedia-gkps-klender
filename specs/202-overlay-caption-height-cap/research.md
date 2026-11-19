# Research: Height-bound song caption type

**Spec**: `specs/202-overlay-caption-height-cap/spec.md`
**Unknowns remaining**: 0

## D001 — Which dimension governs the rest size

- **Decision**: `font-size: 5cqh` on `.obs-overlay__caption`; the `3.75cqw` width term and the 80px
  ceiling are removed.
- **Rationale**: the owner asked for a bound in percent of the screen *height*. On the normal 16:9
  source the two readings differ (72px vs 54px at 1080p); keeping `min(3.75cqw, 5cqh)` would preserve
  the width term on portrait-ish sources, which is larger than "the rest is 5 %" asks for and needs
  an extra term in the spec.
- **Alternatives**: `min(3.75cqw, 5cqh)` — rejected, keeps a width dependency; `clamp(2cqh, 5cqh,
  80px)` — rejected, the 80px ceiling would stop a 4K source at 3.7 % of its height.

## D002 — Where the 2 % floor lives

- **Decision**: the JS computes `stage.clientHeight * 0.02` on each `fitCaption()` call and passes it
  to `Math.max()` in the existing shrink loop.
- **Rationale**: `fitCaption()` already clears the inline size so the stylesheet governs the rest;
  a CSS-only floor cannot be read back as a resolved pixel value from a custom property. Measuring
  the stage mirrors `2cqh` exactly, since the stage is `position: fixed; inset: 0`.
- **Alternatives**: a fixed 11px floor — rejected, breaks the percent rule; a CSS `clamp(2cqh, ...)`
  read through `getComputedStyle` — rejected, custom properties resolve as token streams, not px.

## Provenance

Owner clarifications in conversation (2026-11-19): font size, not block height; rest starts at the
5 % value; 2 % is a floor the fit cannot pass; at the floor the text is simply too long.
