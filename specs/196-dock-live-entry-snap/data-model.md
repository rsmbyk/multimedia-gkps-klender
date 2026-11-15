# Data model — dock live entry snap

**Spec**: `specs/196-dock-live-entry-snap/spec.md` · **Date**: 2026-11-15

## No stored data

This slice changes where the runner parks the live entry; it stores nothing, sends nothing, and creates no state. No model, no migration, no endpoint, no template variable, no context key, no event, no hook, no stored value. The only state it reads is already in `dock` (`obs-dock.js:70-76`) — `dock.entries`, `dock.screens`, `dock.screen`, `dock.lastEntry` — and already-present DOM nodes: `.entryli[data-live="true"]`, its `.entryrow`, its `.nextband`, and `#runBody`.

## Measured at run time, never stored

| Quantity | Where | Computed from |
| --- | --- | --- |
| Live entry's layout top | `liveLi.offsetTop` in `sync()` (`obs-dock.js:1161`) | the non-sticky `.entryli` element, never the pinned row's own `offsetTop` |
| Live entry's box height | `.entryli.offsetHeight` | the `.entryli` element |
| Scroller's view height | `runBody.clientHeight` | `#runBody` |
| Scroller's scroll range | `runBody.scrollHeight - runBody.clientHeight` | `#runBody` |
| NEXT band's protrude | `Math.abs(parseFloat(getComputedStyle(nextBand).bottom))` | the live entry's `.nextband` (`10`, `0` when hidden) |

## Edge-case guard

- A live entry taller than the scroller can never be entirely out of view (`clientHeight < offsetHeight` makes both conditions impossible), so the snap never fires for it — it keeps today's pinned-row behaviour.
- A section-break (divider) entry has no live row and never gets a `data-live="true"` marker (`sync()` skips dividers: `:1085`), so there is nothing to park.
- A go-to block on air follows spec 185's own path (no centring, no snap) — `sync()` returns before the parking code runs (`obs-dock.js:1084-1095`).

## Invariants the tests hold

1. **One live entry at most.** `data-live="true"` is set only on `index === activeEntry` (`obs-dock.js:1118-1120`).
2. **The snap never moves a partly-visible entry.** Any overlap of the `.entryli` box with `[0, clientHeight)` falls back to today's centring target.
3. **The snap never collides with `updateBand`.** The bottom target parks the li's foot 10px below the scroller's bottom edge (the band's `bottom: -10px` protrude), outside the hide rule (`liveEntry.bottom <= box.bottom + 6`) that would otherwise hide the band; with no band (last entry) the protrude is `0` and the foot lands flush at the bottom edge — and the band is hidden by FR-003's rule.
4. **Hand wins.** `wheel` / `pointerdown` call `cancelPendingCenter`, which cancels any pending snap glide before it starts.

## Not modelled

- The service's entries, screens and stops are unchanged; the slice only reads `dock.entries`, `dock.screens`, `dock.screen`.
- Persistent state (last browsed service, last screen, theme) is untouched; the snap is a re-settle, not a stored preference.
