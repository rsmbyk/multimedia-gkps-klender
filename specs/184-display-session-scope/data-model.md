# Data Model: the active Tata Ibadah lasts only the browser session

**Spec**: `specs/184-display-session-scope/spec.md`

Two objects, both in the operator's browser. Nothing reaches the server, and nothing is migrated.

## Entities

### Display state

`localStorage['gkps-display']` — one object per browser, written by the dock, the projector and the
reading page's Project/Stop control, read by every surface.

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `service` | number \| null | a Tata Ibadah id; `null` means nothing selected | FR-001, FR-007 |
| `screen` | number | ≥ 0; kept while hidden, reset by release | FR-007 |
| `on` | boolean | `true` = words on air; `false` = hidden | FR-007 |
| `translation` | `'TB'` \| `'SIM'` \| null | the shown edition; null = the entry's own | FR-007 |
| `at` | number | the writer's `Date.now()` | FR-008 (kept as today) |
| `session` | string | **equals the session marker** or the object is not a state | FR-001, FR-003 |

**Validation**: read through `GKPSDisplaySession.owns(stored)`; a parse error, a missing `session`, or
a `session` that differs from the marker all resolve to the empty state
`{service: null, screen: 0, on: false, translation: null}` (FR-001, FR-009). The object is not
deleted on failure — the next write replaces it (spec Assumptions).

**State transitions**: `empty → on air` (show) · `on air → hidden` (hide) · `hidden → on air` (show
again, in place) · `any → empty` (release) · `any → empty` across a browser session boundary (a new
session's read rejects the old stamp). The first three are today's verbs, unchanged (FR-007).

### Session marker

`gkps-session` — a cookie, one per browser session.

| Attribute | Value | Why |
| --- | --- | --- |
| value | `crypto.randomUUID()` (fallback: time + random, base 36), URI-encoded | opaque; no service, screen, translation or operator (FR-005) |
| domain | the host serving the app | one marker for all four routes |
| path | `/` | `/reading/…`, `/obs/dock`, `/obs/source/overlay`, `/projector` all read it |
| expiry | none | the browser's own session definition — gone when the process ends (FR-001) |
| `SameSite` | `Lax` | a same-site page needs nothing looser |
| `HttpOnly` | absent | the page reads and writes it |
| `Secure` | absent | the local stack is plain `http`; the value is not a secret |

**Validation**: `stamp()` returns `current()` when the cookie holds a value; otherwise it writes a
candidate and returns **what the jar holds afterwards**, so two surfaces minting at once agree on the
last value written (FR-010). If nothing can be read back, the page keeps an in-memory id for its own
lifetime (FR-006).

## Invariants

- A state returned by any reader always has `session === current marker`; the empty state has none.
  (FR-001, FR-002)
- Every write stamps the marker as read *after* a mint, never a candidate the jar did not keep.
  (FR-003, FR-010)
- The marker contains no display data and the display state is never sent to the server. (FR-005)
- Within one session, a write by any surface is visible to every other surface, as today. (FR-004)
- A state without a `session` is never a state, so the deploy starts idle. (FR-009)

## Not modelled

- **Expiry or refresh.** The marker is not rotated; it ends with the browser session. A longer-lived
  browser keeps one id, which is what spec 119's in-session rule wants.
- **Identity.** There is no operator, account or machine identity in the marker or the state.
- **Server storage.** The state is not mirrored anywhere; the public site stays no-login.
- **A second store.** No new `localStorage` key and no second cookie: the stamp rides in the object
  that already exists.
