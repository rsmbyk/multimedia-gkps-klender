# Data Model: the first refresh authenticates its references write

**Spec**: `specs/150-references-token-order/spec.md`

Nothing stored changes. What this slice re-orders is one value's lifetime.

## Entities

### Write token

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `write_token` | string | present in every connected `/status` payload (`local_media.py:587`); compared against the request header at `:514` | FR-001 |
| `token` (page) | string | the module's copy; must hold the current refresh's value **before** that refresh writes | FR-001 |
| `X-GKPS-Media-Token` | request header | exactly `token`; an empty or wrong value is refused `403 {'error': 'Not authorized.'}` | FR-001, FR-003 |

**Relationships**: one `/status` response → one `write_token` → one refresh's writes.
**Validation**: a write belongs to the refresh whose `/status` supplied its token; a refresh that writes
before applying its status writes with the previous token — empty on the first one.
**State transitions**: `absent → known` (first `/status`) · `known → known` (every later refresh, same or
new value) · `known → absent` only if a refresh's `/status` fails, which also degrades the page.

### Refresh

Unchanged from spec 148's model: one `/status` + `/files` read, one references read and write, one draw.
This slice adds one ordering rule to it.

## Invariants

- **A refresh writes with its own token.** The token from the refresh's `/status` is assigned before its
  references write is sent (FR-001).
- **One draw still.** The single `render()` stays at the end of every path; assigning the token adds no
  paint (FR-002, R24).
- **The stub refuses what the companion refuses** — no token, no write (FR-003).

## Not modelled

- **The companion's own token lifetime** (one per process, `local_media.py:601`). Untouched.
- **`share()`'s token path** (`media-handoff.js` polls `/status` itself before sharing). Untouched — it
  already reads the token from its own poll, which is why only the library page's first refresh failed.
