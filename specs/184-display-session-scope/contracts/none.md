# Contracts: none

This slice exposes no external interface: no endpoint, no payload field and no new message on the
`gkps-service-display` channel. The only object that changes is the browser-local display state,
which never leaves the browser.

Stated rather than left absent, as the repository's plan stage requires.

## The internal seam, recorded

The seam is between the four surfaces, in the operator's own browser:

| Contract | Held by | Consumed by | Shape |
| --- | --- | --- | --- |
| `localStorage['gkps-display']` | the dock, the projector, the reading page | every surface | `{service, screen, on, translation, at, session}` |
| `gkps-session` cookie | the first surface to write | every surface | one opaque id |
| `BroadcastChannel('gkps-service-display')` | unchanged | unchanged | `show` · `hide` · `release` · `flip` · `update` · `state` |

No message carries the session id: a message is only ever sent by a surface that has already stamped
its write, and every receiver writes through the same `write()` that stamps the current marker.
