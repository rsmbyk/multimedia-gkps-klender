# Convergence: the first refresh authenticates its references write

**Spec**: `specs/150-references-token-order/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-10-28

Every row of `plan.md`'s traceability table was checked against the code and the runs.

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| SC-001's live readout cannot be taken on the branch: the compose `web` service serves `develop`, and a worktree server is refused by the companion's origin allow-list (`multimedia/local_media.py:447`). | `partial` | SC-001 | Recorded when spec 148 ran into the same wall; this pack carries it as the one `manual` row, with the post-merge commands in `quickstart.md` and task T013. |

No `missing`, `contradicts` or `unrequested` gap: the diff is one statement in `refresh()` plus the stub's
token check, and every other row resolves to a green run or a recorded inspection.

**Outcome**: 1 finding, dispositioned as the pack's `manual` row and task T013; no code change required.

## Pass 2 — 2026-10-28

**Outcome**: Converged — nothing remains. The one finding is a measurement deferred past the merge, not a
gap between the code and a requirement.

## Accepted gaps

<!-- none: the single finding is a deferred measurement with a scheduled task, not an accepted gap -->

## Cap reached

<!-- not reached: pass 2 converged -->
