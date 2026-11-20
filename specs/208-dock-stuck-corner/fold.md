# Fold: the live entry header's corners follow its pin state

**Spec**: `specs/208-dock-stuck-corner/spec.md`
**Date**: 2026-11-20
**Status**: Converged

## Capabilities touched

| Capability | Operation | Before | After |
| --- | --- | --- | --- |
| `dock` | added | no corner state for the live header; no bottom pin; the Next band was caged by its live block | R17 — the live header's top corners follow its pin state; R18 — a faithful bottom pin above an always-visible Next band |
| `dock` | modified | R15's centre act and Next band click/label | unchanged in R15; referenced by R18 for the pin's click act and the band's unchanged click/label |

## Operations

- **Added** `dock/R17` — the live header wears `.is-stuck` (top radius 0 px) exactly when pinned at the top edge with its block still below; the state is re-evaluated on scroll, sync, glide frames and landings, crossing and block-toggle morphs and their landings, and resize; the band's motion guard does not suppress it; only the live header wears it; reduced motion reconciles in the same paint. Five scenarios.
- **Added** `dock/R18` — a faithful clone of the live header stands at the bottom edge when its bottom reaches the Next band's top, flat bottom / round top, abutting the band; the Next band is always visible while a next entry exists and pins flush even when the list fits; the per-frame/reduced-motion rules mirror R17; clicking re-centres the live row (R15 centre act) without changing the screen. Six scenarios.
- **Modified** `docs/spec/dock.md` header — `last folded` 2026-11-19 → 2026-11-20; `208-dock-stuck-corner` prepended to `slices`.

## Before / after counts

- Capability rule count: 16 → 18 (R17 and R18 added; no rule removed).
- No existing rule's text was changed; R15 is referenced, not edited.
- No other capability file is touched.

## Notes

- R18's trigger is the Next band's **top** (`row.bottom > bandRect.top`), not the scrollport edge and not a row early; an early stage added a second header-height of chrome and read as too tall (owner, 2026-11-20).
- The header node cannot bottom-pin as the entry's first child; the pin is a list-level slot holding a `cloneNode(true)` of the live header (mechanism finding, superseding the earlier caption-strip shape).
- The Next band is list-level so it is never caged; the list fills the scrollport and its body drops its bottom padding so the band pins flush in the no-scroll case too (no duplicate row, no dangling gap).
- Two cards (ITEM-219 fix, ITEM-221 feat) share the one spec pack; the declared bump is `minor` for the new capabilities.
