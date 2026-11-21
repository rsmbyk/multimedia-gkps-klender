# Fold: a checkout made on Windows starts the stack

**Slice**: `specs/216-windows-checkout-start` · **Run**: 2026-11-21

## Capabilities touched

| Capability | File | Operations |
| --- | --- | --- |
| `local-stack` | `docs/spec/local-stack.md` | 2 `added` |

## Operations

### `local-stack/R4` — added

- Full block written with three scenarios: a CRLF checkout starts, a `core.autocrlf=true` checkout
  holds LF scripts, a checkout older than the pin starts without being re-cloned.
- Covers FR-001, FR-002, FR-003.

### `local-stack/R5` — added

- Full block written with three scenarios: a restarting companion is named and the start's status is
  kept, an empty mount keeps its existing message, a failed start runs no check.
- Covers FR-004, FR-005, FR-006, FR-007.

## Counts

| | Before | After |
| --- | --- | --- |
| Requirements in `local-stack` | 3 | 5 |
| Scenarios in `local-stack` | 11 | 17 |

Header moved: `last folded` `2026-11-14` → `2026-11-21`; `slices` gained `216-windows-checkout-start`
at the front.

## Not folded

Nothing — the slice converged with no accepted gaps (see `converge.md`).

## Idempotence

Re-running this fold adds nothing: both blocks are keyed by their `R<n>` heading, and `R4`/`R5` now
exist. The header line is written, not appended, so a second run leaves the same text.
