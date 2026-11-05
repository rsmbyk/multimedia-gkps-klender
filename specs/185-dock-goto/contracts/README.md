# Contracts: the dock's Go To

**Spec**: `specs/185-dock-goto/spec.md`

## Interfaces exposed by this slice

| Interface | Kind | Defined in | Consumed by |
| --- | --- | --- | --- |
| `gkps-display` (stored shape, `goto` field) | browser storage | `contracts/display-state.md` | `static/web/display.js` readers: the dock, the projector, the overlay, the reading page |
| `gkps-service-display` message `{type: 'goto', goto}` | `BroadcastChannel` | `contracts/display-state.md` | the same three surfaces |
| `GKPSDisplay` verbs `goTo`, `back`, `flip` | in-page JS API | `contracts/display-state.md` | `obs-dock.js`, `projector.js`, `display.js`'s own callers |
| `/projector/goto/{index, chapter/<b>/<c>, song/<id>}/` | HTTP GET, existing | `multimedia/web/reading/goto.py` (spec 136) | the dock, the projector, the overlay |

## Not exposed

No new endpoint, no server-rendered goto, no storage key of its own (FR-013). The find band's
query and the block's rows are page memory and never leave the dock. The projector's recording lock
stays the projector's own runtime state — it gates its own `G`, not the state.
