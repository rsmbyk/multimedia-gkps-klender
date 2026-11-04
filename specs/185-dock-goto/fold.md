# Fold: the dock's Go To

**Capability**: `docs/spec/display-state.md` (R2 added) · `docs/spec/projector.md` (R1, R5 modified) ·
`docs/spec/overlay.md` (R1 modified) · `docs/spec/dock.md` (new, R1–R4)
**Folded at**: 2026-11-04

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `display-state/R2` | the state carries `goto` — a pointer to what is on air instead of the service — with the service's place frozen beside it, the verbs' meanings, and the corrupt/session scenarios |
| `added` | `dock/R1` | the runner offers a Go To and the picker does not; a go to with nothing on air adopts the browsed service underneath it |
| `added` | `dock/R2` | the find band answers from the projector's own index, read once at the first open, with no request while typing and one fetch per selection |
| `added` | `dock/R3` | what is on air is the list's live block, the transport acts on it, and Back restores the service's screen and edition |
| `added` | `dock/R4` | the band is a layer with three ways to close it; the switch-service control is disabled, not hidden, while a go to is up |
| `modified` | `projector/R1` | the Go To writes the display state instead of holding a page-local detour; the fetched payload becomes a cache keyed by the state; a projector opened mid-go to paints it |
| `modified` | `projector/R5` | a go to arriving over the channel stops a playing recording, as another screen does |
| `modified` | `overlay/R1` | the state it paints gained `goto`: a song as the caption, a passage as the quotation card, in the shown edition |

## Drift guard

- **Files changed in this capability**:
  - `display-state`: `static/web/display.js` (shape, verbs `goTo`/`stepGoto`/`back`/`resume`, the
    `{type: 'goto'}` message)
  - `projector`: `static/web/projector.js` (the detour read from the state, the payload cache,
    `fromChapter`, media released before a go to paints), `static/web/projector-library.js`
    (`fromChapter` exported)
  - `overlay`: `static/web/obs-overlay.js` (`readState` carries `goto`, `syncGoto` paints it)
  - `dock`: `static/web/obs-dock.js` (the band, the layer, the block, the transport, the disabled
    switch), `static/styles/design/obs-dock.css` (their rules),
    `multimedia/web/templates/reading/obs_dock.html` (the head's control, the block, the band, the
    layer)
- **Declared no behaviour change**: no — every file above carries a delta in this table.
- **Not moved**: the dock's older rules (`reading/R33` and the picker's buckets) stay where they are;
  `dock.md`'s header names the overlap, and moving them would rewrite accepted text this slice does
  not change (research D010).
