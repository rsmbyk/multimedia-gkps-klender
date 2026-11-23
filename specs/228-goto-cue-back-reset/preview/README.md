# Preview: Back clears the Go To from the cue over an empty stage

`live preview at http://127.0.0.1:8765/projector` — the slice worktree's own server. Hard-reload
after a JS edit. Clear `gkps-display` in localStorage between scenarios.

`probe.py --base http://127.0.0.1:8765` starts a Go To from the dock with no service, then presses
the dock's Back and prints the cue before and after.

## States

1. **No service, before Back** — open `/obs/dock` with no service on air, press `g`, search a song,
   Enter, then open `/projector`. The cue names the song with its baits and `back to service`.
2. **No service, after Back** — press the dock's Back (or the cue's own Back). The cue returns to
   its separator-only state: no label, no baits, no Back control. The empty notice is back.
3. **Service with no entries** — open `/projector?service=<empty>`, start a Go To, press Back. The
   cue clears the same way and the empty notice returns.
4. **Never opened** — a projector that has never had a Go To shows the same empty cue as state 2.
5. **Populated service** — the cue still returns to the entry's label, baits and next control.
6. **Idle HUD** — leave a projector with no service (or a service with no entries) untouched for a
   few seconds. The cue shows no text and no `·`; the edge and centre zones show no arrows or
   hide/show icon and do nothing on click; the pointer stays visible. A click still fullscreens;
   the service list, keys sheet and find band still open. Starting a Go To restores the spec 227
   cue and controls until Back ends it.

## Measured read-back (1280×800)

- Before Back: cue reads `· HAL 1 Jahowa Sihol Pujionku ·12345671/2 back to service`; seven baits;
  `#cue-next.hidden === false`.
- After Back: cue reads `·`, prefix empty, zero baits, zero flips, Back empty and
  `#cue-next.hidden === true`; `visibility: visible` — the cue itself is still the operator's
  controls surface, only the Go To information is gone.
- Idle HUD: cue `innerText === ''`, separator `display: none`, zone `pointerEvents: none`,
  `cursorHidden: false`, body cursor `auto`; `.keys` and `#cue-service` keep `pointerEvents: auto`,
  and a click at (100, 100) enters fullscreen.
- The lone arrow: `#cue-next[hidden]` computed `display: flex` and `#cue-arrow` painted
  12.8 × 12.8 before the rule; now `display: none` and the arrow box is 0 × 0.
