# Convergence: live reading freshness

**Spec**: `specs/258-live-reading-freshness/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-11-28

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| Page poll sent `kind=tatib` to an endpoint that accepts `service` | `missing` | FR-001 | mapped `tatib` to `service` in `freshness.js` |
| The poll cached the loaded version, so a test could not simulate a stale page | `partial` | FR-003 | the baseline is now read from `data-page-version` on each poll |
| Reload did not clear the badge because the shell refresh keeps the badge node | `missing` | FR-006 | `freshness.js` listens for `shell:page` and resets the stale state |
| The sidebar animation assertion ran before `animationstart` fired | `partial` | FR-010 | the E2E now records animation names from an init script and waits 80 ms |
| Page-rendering tests had no static manifest in the worktree | `partial` | FR-012 | `collectstatic` run; the six `ServiceReorderPaneTests` errors disappeared |

**Outcome**: 5 gaps fixed; no requirement changed.

## Pass 2 — 2026-11-28

**Outcome**: Converged — nothing remains.

## Verification evidence

- 5 endpoint tests and 4 Playwright tests: OK.
- 443 app tests: 7 failures, all reproduced on unmodified develop — scripture fragment placeholder (ITEM-261), shortcuts sheet, legacy tatib list, image projection and three slot endpoints (ITEM-217).
- Preview probe remains aligned: badge 289×48, disabled controls at 0.45 opacity, 180 ms row animation.

## Accepted gaps

| Gap | Type | Severity | Accepted on |
| --- | --- | --- | --- |
| Seven unit-lane failures identical on develop | `contradicts` | known red | 2026-11-28 — recorded as ITEM-217 and ITEM-261 |

## Cap reached

<!-- not reached -->
