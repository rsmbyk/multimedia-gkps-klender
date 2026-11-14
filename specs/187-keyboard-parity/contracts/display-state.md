# Contract — the display state, with a go to that names no service

**Spec**: `specs/187-keyboard-parity/spec.md` · **Module**: `static/web/display.js`

This is the delta to the contract spec 185 wrote (`specs/185-dock-goto/contracts/display-state.md`) and
to `docs/spec/display-state.md` R2. One allowance changes; no field and no message is added.

## Stored shape

```
gkps-display = {
  service: <id|null>, screen: <n>, on: <bool>, translation: <'TB'|'SIM'|null>,
  at: <ms>, session: <string|null>,
  goto: null | { kind: 'song',    song_id: <id>, index: <n> }
             | { kind: 'passage', book_id: <id>, chapter: <n>, verse: <n>, translation: 'TB'|'SIM' }
}
```

- **`goto` may now stand beside `service: null`** (FR-003). Before this slice `gotoOf()` refused a go
  to without a service; the picker's `G` needs it, and the owner's ruling is that such a go to stands
  alone rather than adopting a service.
- `screen` and `translation` remain the **service's** place. A service-less go to writes
  `screen: 0`, `translation: null`, and nothing reads them until a service is on air again.
- A stored value whose `goto` cannot be parsed still reads as `goto: null`.

## Verbs

| Verb | No go to | Go to over a service | Go to with no service |
| --- | --- | --- | --- |
| `show(service, screen)` | the service's screen goes on air | the go to ends, the service's screen goes on air | the go to ends, the service's screen goes on air |
| `moveTo(screen)` | the service's screen moves | the go to ends first | the go to ends, the service moves |
| `hide()` | words off, place kept | words off, the go to's place kept | words off, the go to's place kept |
| `release()` | nothing on air | the go to ends with the service | nothing on air |
| `flip(translation)` | the service's edition | the go to's edition | the go to's edition |
| `goTo(goto)` | the go to starts | replaces it | replaces it |
| `stepGoto(position)` | no-op | moves `index` / `verse` | moves `index` / `verse` |
| `back()` | no-op | `goto: null`; the service is on air as it stood | `goto: null`, `service: null`, `on: false` — idle |

Every verb still writes once (`at` renewed, `session` stamped) and posts one message.

## Messages on `gkps-service-display`

Unchanged from spec 185: `{type: 'goto', goto}`, `show`, `hide`, `release`, `flip`, `update`, `state`.
A service-less go to uses the same `goto` message; readers must not assume `service` is non-null when
they paint it (FR-011).

## Reader obligations

| Reader | Obligation |
| --- | --- |
| Projector | Paints the detour when `goto` is non-null, whether or not `service` is (FR-011); `back` leaves every surface idle. |
| Overlay | Paints the plate for a `goto` with `service: null`; paints nothing once it ends (FR-011). |
| Dock | Shows the go to block alone when `service` is null; `Back` ends it and returns to the picker (FR-004). |
| Reading page's project control | Ends a service-less go to the way it ends any projection: `release()`. |
