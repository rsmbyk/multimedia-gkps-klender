# display-state

**capability**: `display-state`
**last folded**: 2026-11-04
**slices**: `186-display-session-refresh`, `185-dock-goto`, `184-display-session-scope`

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

### R2 — The state carries what is on air instead of the service, as a pointer

The state SHALL carry `goto`, which is `null` while the service is on air or names what is on air
instead: a song with its screen index, or a passage with its book, chapter, verse and shown edition.
While `goto` is not null the state's `screen` and `translation` SHALL be the service's own place and
SHALL NOT change; Back is `goto: null` and every surface then paints them. The goto SHALL carry no
verse text, title or lyric. `show` and a move to a service screen SHALL end it; `hide` SHALL blank it
and keep its place; `release` SHALL end it with the service; `flip` SHALL name the edition of whatever
is on air. Every change SHALL be one write and one `{type: 'goto'}` message, and a goto whose stored
shape cannot be parsed SHALL read as no goto. (spec 185)

#### Scenario: a go to starts from the dock
- WHEN the dock writes `goto` for a chosen song or passage
- THEN the state's `screen` and `translation` are unchanged, and every reader paints the go to

#### Scenario: the operator hides the words during a go to
- WHEN `on` goes false while `goto` is set
- THEN the words leave every surface, the go to keeps its place, and a resume needs no second write

#### Scenario: a service screen goes on air during a go to
- WHEN `show` or a move puts a service screen on air
- THEN `goto` is cleared in the same write

#### Scenario: a corrupt go to
- WHEN the stored `goto` is not a song or a passage
- THEN readers treat it as no go to and paint the service screen the state names

#### Scenario: the browser session ends
- WHEN the stored state's stamp no longer matches the browser
- THEN the go to reads as no go to, with the rest of the state

### R3 — A surface open across the session's end re-reads, and paints idle

A surface that stays open SHALL read the display state again when its document becomes visible, when
its window gains focus, and when it is restored from the back/forward cache, and SHALL paint from that
read in the same turn — no timer, no polling interval. The domain's re-read SHALL be the state
module's own act: it compares the read with what it holds and notifies its subscribers only when they
differ, so a surface that renders on notification needs no listener of its own, and a re-read that
finds the same state repaints nothing. A state whose session stamp no longer matches SHALL leave the
surface painting nothing: no live row, no go to block, no projector screen, no overlay plate, the
dock's eye reading `Display this service`. The re-read SHALL add no storage key, channel message or
verb. (spec 186)

#### Scenario: the session ends while a dock tab is open
- WHEN the browser's session marker is gone and the dock tab takes focus
- THEN it marks no entry and no screen row, draws no block, and its eye reads `Display this service`

#### Scenario: the tab becomes visible again
- WHEN a hidden surface becomes visible
- THEN the same re-read happens, without a reload

#### Scenario: nothing has changed
- WHEN a surface is focused while its state still matches
- THEN no subscriber is notified and nothing repaints

#### Scenario: the projector is the open surface
- WHEN the marker is gone and the projector takes focus
- THEN it paints no screen, no detour, and `data-showing="false"`

#### Scenario: the page comes back from the back/forward cache
- WHEN a restored page fires `pageshow` with `persisted`
- THEN the re-read runs there too
