# display-state

**capability**: `display-state`
**last folded**: 2026-11-03
**slices**: `184-display-session-scope`

The browser-local state that decides what is on air in one browser — which Tata Ibadah, which screen,
whether the words are up, and in which edition. The dock, the projector and a reading page's
project control write it; every surface reads it. Spec 119 built it and made catch-up mandatory;
spec 184 created this capability file when it bounded the state's life to the browser session.

### R1 — The display state lives only for the browser session that wrote it

The state SHALL carry the session that wrote it and SHALL be read only while that session is live: a
state whose stamp does not match the browser's session marker is no state at all, on every surface and
from its first paint. The marker SHALL be a cookie with no expiry whose value carries no service,
screen, translation or operator identity. Within one session the state SHALL keep its present
catch-up and live-update behaviour, and closing every surface SHALL NOT end it. (spec 184)

#### Scenario: a browser starts again
- WHEN the browser session ends and the browser starts again on the same storage
- THEN the overlay paints nothing, the projector paints no screen, and the dock marks no service as on screen

#### Scenario: a state with no stamp
- WHEN a stored state has no session stamp, or one from another session
- THEN every reader returns `{service: null, screen: 0, on: false}` and never paints the stored object

#### Scenario: every surface closes inside one session
- WHEN the dock, the projector and the overlay are all closed and one is opened again in the same session
- THEN the service is still on air (spec 119, kept)

#### Scenario: the browser cannot hold a cookie
- WHEN a page cannot read its marker back after writing it
- THEN the display works for the life of that page, a reload starts idle, and no error reaches the operator
