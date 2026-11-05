# Contracts: one keyboard grammar for the dock and the projector

**Spec**: `specs/187-keyboard-parity/spec.md`

## Interfaces exposed by this slice

| Interface | Kind | Defined in | Consumed by |
| --- | --- | --- | --- |
| `gkps-display` (localStorage object) | browser-local state | `contracts/display-state.md` | the dock, the projector, the overlay, the reading page's project control |
| `gkps-service-display` (BroadcastChannel) | window-to-window messages | `contracts/display-state.md` | the same four surfaces |
| The keyboard grammar | behavioural contract between two surfaces | `contracts/keyboard.md` | the dock's runner/picker, the projector |

## Not exposed

- **No HTTP endpoint is added.** Chapter and book steps reuse `/projector/goto/chapter/<book>/<chapter>/`,
  songs reuse `/projector/goto/song/<id>/`, and the lookup index reuses `/projector/goto/index/`
  (spec 185). Nothing new is served, nothing new is fetched.
- **No new storage key.** The go to stays a field of `gkps-display`; no migration runs.
- **The sheets' markup and CSS stay page-local.** The dock's sheet is inside `obs_dock.html`; the
  projector's inside `projector_controls.html`. They share a grammar, not a component.
