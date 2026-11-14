# Data Model: The companion's page manages this computer's origins

**Spec**: `specs/192-companion-origin-page/spec.md`

## Entities

### Recorded origin

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| value | string | exact origin: `http`/`https` scheme, no whitespace/credentials/path/query/fragment, hostname present, optional numeric port ≤ 65535 (FR-002) | FR-002 |

Stored as a JSON array in the `settings` table (`key='origins'`), order preserved; never stored
twice (FR-002).

**Relationships**: none — a flat set checked at request time against the `Origin` header.
**Validation**: `rules` in the page form and `parse_allowed_origins` in the companion must accept
exactly the same shape (FR-002, SC-004).
**State transitions**: added (form / API) → edited (inline) → deleted — each mutation rewrites the
settings row and the in-memory list atomically (FR-002).

### Local seed

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| value | string | compose-interpolated `http://localhost:<WEB_PORT>` and `http://127.0.0.1:<WEB_PORT>` | FR-006 |

Read-only everywhere; never editable from the page (assumption) — displayed by the page (FR-001).

### Font directory view

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| path | string | container path under `/usr/share/fonts/host/*` or the operator directory | FR-005 |
| source | string | optional launcher-provided host label (`GKPS_MEDIA_FONT_LABELS`) | FR-005 |
| families | integer | unique family count from `fc-list` on that directory | FR-005 |

Computed per request, never stored; a missing directory is omitted; no directories at all → the
none-found line (FR-005).

## Invariants

- The recorded set is always unique and order-stable (FR-002; SC-004).
- The companion's own origin never needs an allowlist entry — page and config endpoints are served
  on the Host + own-origin check alone (FR-004).
- Enforcement is per request over `env seeds ∪ recorded set` (FR-003) — a page change takes effect
  without a restart.
- The stored set survives companion restarts, daemon restarts and machine reboots (FR-002; SC-002)
  and is removed with the volume (`docker compose down -v`) — documented.

## Not modelled

- The media session token and its handoff — unchanged by this slice (FR-004 only exempts the page
  from it).
- Per-origin metadata (labels, environments) — the set is a flat ordered list of exact origins; a
  labelling scheme would be new product surface, not requested.
