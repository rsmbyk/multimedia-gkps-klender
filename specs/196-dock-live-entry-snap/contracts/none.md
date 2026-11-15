# Contracts — none

**Spec**: `specs/196-dock-live-entry-snap/spec.md` · **Date**: 2026-11-15

This slice exposes no interface. It adds no endpoint, no payload field, no header, no template variable, no context key, no event, no hook and no stored value.

The only names it touches are already internal to the dock:

- `#runBody` (`obs-dock.js:41`) — the scroller whose `scrollTop` the snap drives; this element is already the target of every centring and glide call in the dock.
- `dock` (`obs-dock.js:70-76`) — its fields (`entries`, `screens`, `screen`, `lastEntry`, `on`) are read inside `sync()` and updated without change to their shape or the service they key off.
- `.entryli[data-live="true"]` — the live entry's container, already marked and inspected during `sync()` rendering (`obs-dock.js:1103-1119`).
- `.nextband` — the sticky NEXT band, already controlled by `updateBand()` (`obs-dock.js:623-646`); the snap's bottom target uses the band's top edge as its floor, without changing how the band is shown/hidden.
- `glideScroll()` — the existing snap glide reuses this function (`glideTarget`, `glideFrame`, `reduceMotion`); it does not create a new path or timer.
- `scheduleCenter()` — unchanged; the snap replaces `scheduleCenter` when the entry is off-screen, not adds to it.

The REST API (`/projector?service=…`, `/projector/goto/…`, `/projector/goto/song/…`, `/projector/goto/chapter/…`) is untouched. The pickle (`web/display.js`) is untouched. No new message, no stored value, no template variable, no template change, no CSS change, no DOM addition other than the scroll change already handled.