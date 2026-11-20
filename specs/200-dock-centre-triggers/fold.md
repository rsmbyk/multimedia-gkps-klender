# Fold: the dock follows the live entry only when following

**Spec**: `specs/200-dock-centre-triggers/spec.md`
**Converged**: 2026-11-18 (`converge.md`, one pass, one accepted gap)

## Capabilities touched

- `docs/spec/dock.md` — **added**: `dock/R15` with seven scenarios; header's `last folded` moved to
  2026-11-18 and `200-dock-centre-triggers` prepended to `slices`.

## Operations

| Capability | Operation | Requirement | Before | After |
| --- | --- | --- | --- | --- |
| `dock` | added | R15 | 14 requirements (R1–R14) | 15 requirements (R1–R15) |
| `dock` | added | R15 scenarios | 44 scenarios | 51 scenarios |

No requirement was modified, removed or renamed. R14 (headers toggle, items jump) keeps its number
and wording — this slice adds the mode around it.

## Not folded — accepted gap

- Browsing-mode crossings still animate block heights, so the browser may clamp `scrollTop` down
  when the list shrinks. Accepted at Gate 2 (finding A4) and re-recorded in `converge.md` C6; no
  centring glide runs, which is what FR-006 forbids. No capability text was changed for it.

## Idempotence

Re-running this fold with `dock/R15` already present writes no second block; the header date and
slice list are set values, not appends.
