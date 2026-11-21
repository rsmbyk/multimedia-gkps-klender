# Fold: a dead companion says why

**Slice**: `specs/218-restart-log` · **Run**: 2026-11-21

## Capabilities touched

| Capability | File | Operations |
| --- | --- | --- |
| `local-stack` | `docs/spec/local-stack.md` | 1 `modified` (`R5`) |

## Operations

### `local-stack/R5` — modified (complete replacement block)

- The not-running report now carries three parts: the line naming the companion, the companion's own
  last log line when it has one, and the line naming `docker compose logs media` and
  `docker compose build`.
- "No log SHALL be requested unless the companion could not be reached" states what was implicit.
- Two scenarios were added — a companion with no log, and a healthy companion that is not asked —
  because both are shapes the previous text left to inference.
- Provenance line reads `(spec 216, revised by spec 218)`.
- Covers FR-001..FR-006.

## Counts

| | Before | After |
| --- | --- | --- |
| Requirements in `local-stack` | 5 | 5 |
| Scenarios in `local-stack` | 18 | 20 |

Header: `slices` gained `218-restart-log` in front; `last folded` stays `2026-11-21`.

## Not folded

Nothing — converged in one pass, one accepted MEDIUM (analysis A-01).

## Idempotence

Re-running replaces `R5` with the same block and touches nothing else.
