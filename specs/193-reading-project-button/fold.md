# Fold — Project button on the song and Bible pages

**Run**: 2026-11-14, at Converged (pass 1, no accepted gaps).
**Idempotence**: re-running rewrites the same blocks and the same headers.

## Capabilities touched

| Capability | Operation | Requirement |
| --- | --- | --- |
| `docs/spec/reading.md` | added | `reading/R42` — A reading page's Project control puts its song or chapter on air |
| `docs/spec/dock.md` | added | `dock/R12` — A reading page starts a Go To |
| `docs/spec/projector.md` | modified | `projector/R1` — The Go To searches a page-memory index and fetches the content it paints (an identical pointer is inert; a stored Go To rides a boot adoption) |

## Counts (before → after)

- `reading.md`: R1–R41 → R1–R42 (added 1)
- `dock.md`: R1–R11 → R1–R12 (added 1)
- `projector.md`: R1–R13 → R1–R13 (modified 1 — full replacement block, scenarios extended by two)

## Header moves

All three files: `last folded` → **2026-11-14**, and `193-reading-project-button` prepended to
their `slices` list.

## Not folded — nothing

No accepted gaps: Converge reported Converged with every traceability row holding by its declared
method. The two `partial` findings were made whole in-pass (T017's boot ride); the stale parity path
was corrected; the evidence note about the pre-existing suite reds is a converge fact, not a
behaviour change.

## Drift guard

Files changed inside these three capabilities in this slice: `static/web/projector.js` (R1's
behaviour — declared), `static/web/display.js` + the two stage templates + `components.css`
(reading/R42, dock/R12 — declared). No undeclared behaviour change.
