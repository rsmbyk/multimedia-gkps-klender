# Research: the active Tata Ibadah lasts only the browser session

**Spec**: `specs/184-display-session-scope/spec.md`
**Unknowns remaining**: 0

## D001 — The session primitive is a session cookie

- **Decision**: the display state carries a `session` stamp; the stamp's value is kept in
  `gkps-session`, a cookie with no expiry (`Path=/`, `SameSite=Lax`, not `HttpOnly`), minted by the
  first write and read by every surface.
- **Rationale**: a cookie without an expiry is the browser's own definition of "this session" — it
  is shared by every tab, survives a reload, and is dropped when the browser process ends. It keeps
  spec 119's in-session rule ("closing every surface changes nothing") while adding exactly the
  boundary the owner asked for.
- **Alternatives considered**:
  - *`sessionStorage` per surface plus the channel handshake*: survives a reload of one surface, but
    a new surface can only recover the state while another surface is alive — closing the dock, the
    projector and the overlay would end the display with the browser still open, which the owner's
    answer rejects.
  - *Memory only*: same objection, and worse — a reload of the only surface loses the display.
  - *A heartbeat in `localStorage`*: cannot tell "the browser restarted one second ago" from "no
    surface has written for a while", and would end the display mid-service.
  - *Server-side state*: forbidden by spec 119 — the state must never reach the server, and the app
    has no accounts.
- **Provenance**: owner decision (Clarify, 2026-11-03); the store's behaviour measured in D009.

## D002 — The marker's attributes, and why it carries nothing else

- **Decision**: name `gkps-session`; value a `crypto.randomUUID()` (fallback
  `Date.now().toString(36) + Math.random().toString(36).slice(2)`), URI-encoded; attributes
  `Path=/; SameSite=Lax`; no `Expires`/`Max-Age`; no `Secure` attribute (so the same code works on
  the local `http://127.0.0.1` stack and on the https deployment); not `HttpOnly` (the page must read
  and write it).
- **Rationale**: `Path=/` is needed because the four surfaces live on four routes (`/reading/…`,
  `/obs/dock`, `/obs/source/overlay`, `/projector`). A single opaque value carries no service,
  screen, translation or operator identity, so a cookie that travels with requests reveals nothing
  about what is on air.
- **Alternatives considered**: four path-scoped cookies (one per surface) would not be one marker;
  localStorage for the marker (outlives the session — the defect); a signed value (adds a secret and
  a server dependency for no gain).
- **Provenance**: research; settings read — the project sets no `CSRF_COOKIE_SECURE`/CSP that would
  interfere (`multimedia/settings.py`).

## D003 — One shared session module, not three copies

- **Decision**: add `static/web/display-session.js`, loaded before the surface script by
  `reading/base.html`, `reading/obs_dock.html`, `reading/projector.html` and
  `reading/obs_overlay.html`. It exposes `window.GKPSDisplaySession` with `current()` (the marker or
  empty), `stamp()` (the marker, minting it if absent) and `owns(stored)` (does this stored object
  belong to the live session?).
- **Rationale**: the rule must be identical in the three readers/writers. `display.js` (the dock and
  every reading page), `projector.js` (its own store) and `obs-overlay.js` (its own read) each keep
  their present structure; each replaces its parse/validate with one call.
- **Alternatives considered**: load `display.js` on the projector and the overlay and use
  `gkpsDisplay.read()` — the overlay would then also run a channel handler that *writes* on every
  message (it is a listen-only surface), and the projector would double-write; duplicating the
  cookie code in three files — drift between readers is the exact failure this slice must avoid.
- **Provenance**: research.

## D004 — The stored shape gains one field; no migration

- **Decision**: `localStorage['gkps-display']` becomes
  `{service, screen, on, translation, at, session}`. A stored object without a `session`, or with a
  different one, reads as `{service: null, screen: 0, on: false, translation: null}`. The stale object
  is not removed on read; the next write replaces it.
- **Rationale**: the owner's answer keeps a state that a browser restart invalidates; the simplest
  invalidation is a stamp the state itself carries. Not deleting on read avoids a race in which one
  surface's read prunes a state another surface is writing (FR-009, spec Assumptions). No migration:
  the first load after the deploy is a browser session without a marker, so it starts idle — which is
  the requested behaviour rather than a loss.
- **Alternatives considered**: a separate `gkps-display-session` key (two objects to keep in step);
  bumping the storage key (`gkps-display-2`) — it would leave the old key orphaned and still need a
  stamp for future sessions.
- **Provenance**: research.

## D005 — Minting is a compare-and-take, so two surfaces agree

- **Decision**: `stamp()` reads the marker; if absent it writes a candidate, then **re-reads** the
  cookie and returns whatever value the jar now holds. Every writer stamps with that returned value.
- **Rationale**: the Project act opens the projector window and writes the state from the reading
  page at nearly the same moment (`display.js`), while the projector's own `?service=` adoption
  writes too (`projector.js`). Two independent mints would leave one state stamped with an id the
  cookie no longer holds, and the display would read as dead until the next act. Re-reading after the
  write makes the last cookie write the agreed id.
- **Alternatives considered**: mint on first read (a reader could mint while another tab mints);
  derive the id from a timestamp (two tabs can share a millisecond); a `BroadcastChannel` election
  (more moving parts, and the channel is per page lifetime).
- **Provenance**: research; the race is real in the existing Open-projector path
  (`static/web/display.js` §the project button).

## D006 — No cookie storage: an in-page id, and the honest cost

- **Decision**: if the cookie cannot be read back after writing, `stamp()` keeps a per-page id in
  memory. The page works for its lifetime; a reload starts idle; no error is shown.
- **Rationale**: the alternative (falling back to a `localStorage` marker) would silently restore
  the persistence defect for exactly the user who cannot hold a session cookie. The cost is recorded
  in the spec (FR-006) and the assumption list.
- **Alternatives considered**: refuse to project without cookies (turns a display into an error
  page mid-service); use `sessionStorage` (survives a reload, so a reload would keep the state while
  two tabs disagree — a third answer).
- **Provenance**: research; `document.cookie` can be made unavailable in a test context (probe,
  D009).

## D007 — Tests: a new session is a new context; a browser restart is a persistent profile

- **Decision**: `tests/e2e/test_display_session.py` carries the behaviour:
  - a prior session's state is injected with `context.add_init_script` into a fresh context (no
    cookie), and the overlay's stage is observed from document start (a `MutationObserver` installed
    by the same init script) so "nothing at first paint" is measurable;
  - "same session, every surface closed" is one context, pages closed and reopened;
  - "the browser restarted" is a real `launch_persistent_context` with a temporary profile: project,
    close the browser, launch again on the same profile, open the overlay — the session cookie is
    gone and the state is dead while `localStorage` still holds it.
- **Rationale**: Playwright's `new_context()` has its own storage, so it cannot by itself represent
  "the same browser after a restart". The persistent profile is the only simulation that exercises
  the cookie's lifetime at a process boundary. The scratch probe already ran this shape: the session
  cookie was gone after the relaunch, `localStorage` was intact (D009).
- **Alternatives considered**: deleting cookies with `context.clear_cookies()` (simulates it, but
  proves nothing about the browser's own behaviour); asserting only on `gkpsDisplay.read()` (does not
  reach the overlay's first paint).
- **Provenance**: probe, `~/.hermes/cache/scratch/pw-session-probe/probe.py` (scratch, dated
  2026-11-03); the committed test replaces it.

## D008 — OBS's CEF shares one cookie jar and does not persist session cookies

- **Decision**: an OBS restart is a browser restart for the dock and the overlay.
- **Rationale**: OBS's browser plugin initialises CEF once with
  `CefString(&settings.cache_path)`/`root_cache_path` set to its own config directory and does not set
  `persist_session_cookies` (`obs-browser-plugin.cpp`, CefSettings at l. 304, cache paths at l.
  361–363, `CefInitialize` at l. 397). CEF's default is documented as *"Session cookies are generally
  intended to be transient and most Web browsers do not persist them"* and the field defaults to 0.
  Both a browser source and a dock create their browser with a null request context
  (`obs-browser-source.cpp` l. 241; `panel/browser-panel.cpp` l. 352), which means the global context
  — one cookie jar and one `localStorage` shared by every source and dock in the OBS process.
- **Alternatives considered**: a per-surface marker (they would disagree); storing the marker inside
  `localStorage` (the defect).
- **Provenance**: obs-browser source, `master` read on 2026-11-03; CEF `cef_settings_t`
  documentation for `persist_session_cookies`.

## D009 — Measured: a session cookie dies at restart, `localStorage` does not

- **Decision**: rely on the cookie's lifetime; do not add an unload handler.
- **Rationale**: a scratch Chromium profile was launched twice with
  `launch_persistent_context`. First launch wrote a session cookie, a one-day cookie and a
  `localStorage` value; the profile was closed; the second launch read only the one-day cookie and
  the `localStorage` value — `document.cookie` and the jar both lacked the session cookie. A
  killed browser is the stronger case: a cookie that is never written to disk cannot come back.
- **Alternatives considered**: a `pagehide`/`unload` cleanup (never runs on a crash, and a crash must
  still start idle — spec edge case).
  Note: a browser configured to restore its previous session may restore session cookies with it;
  the spec records that as the session continuing, not as a defect.
- **Provenance**: probe run 2026-11-03 (scratch); its assertions move into the committed E2E in D007.

## D010 — The reading page needs no separate rule

- **Decision**: every reading page already loads `display.js`; its `read()` gains the same check,
  and its Project/Stop verbs go through the same `write()`. Nothing else changes there.
- **Rationale**: spec 141's reopen control and the Project button read the same state; one rule in
  one module keeps them consistent with the projection surfaces (spec §Edge cases — "no third
  answer").
- **Alternatives considered**: a page-local check (a second implementation).
- **Provenance**: research, `static/web/display.js` §the project button.

## Open

<!-- empty: Phase 0 is finished -->
