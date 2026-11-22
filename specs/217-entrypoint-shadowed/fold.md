# Fold: the runtime entrypoint survives the bind mount

**Slice**: `specs/217-entrypoint-shadowed` · **Run**: 2026-11-21

## Capabilities touched

| Capability | File | Operations |
| --- | --- | --- |
| `local-stack` | `docs/spec/local-stack.md` | 1 `modified` (`R4`) |

## Operations

### `local-stack/R4` — modified (complete replacement block)

- The requirement now says the entrypoint the image runs lives **outside** the directory the local
  stack bind-mounts, so a mounted checkout cannot replace it. The LF pin and the build-time strip keep
  their sentences; "whatever the stack mounts over the working directory" is added to the opening.
- A second scenario was added — the `web` service runs the image's own entrypoint, not the mounted
  file, and an LF and a CRLF checkout behave identically — because that is the case the previous text
  did not cover and the one that failed.
- Provenance line reads `(spec 216, revised by spec 217)`.
- Covers FR-001, FR-002, FR-003, FR-004.

## Counts

| | Before | After |
| --- | --- | --- |
| Requirements in `local-stack` | 5 | 5 |
| Scenarios in `local-stack` | 17 | 18 |

Header moved: `slices` gained `217-entrypoint-shadowed` in front; `last folded` stays `2026-11-21`.

## Not folded

Nothing — the slice converged; SC-003's end-to-end row is an evidence gap on this machine (analysis
A-01), not a behaviour gap, and the behaviour it names is what `R4` already states.

## Idempotence

Re-running the fold replaces `R4` with the same block and leaves the rest of the file untouched.
