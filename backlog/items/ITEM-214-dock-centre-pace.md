---
id: ITEM-214
status: done
title: 'The dock''s re-centring keeps pace with fast advancing'
type: fix
priority: P2
effort: S
created: 2026-11-19
updated: 2026-11-19
spec: 205
branch: fix/205-dock-centre-pace
pr: 544
issue: 542
closed_at: 2026-11-19
closed_reason: merged into develop (PR #544)
bump: patch
release_version: —
---

# ITEM-214: The dock's re-centring keeps pace with fast advancing

## Summary

In following mode, advancing faster than the centring glide completes makes the list bob up and
down: each advance restarts the glide from `t = 0`, and spec 200's softened ease-in begins every
restart near zero velocity, so the list lags the live row. Halve the re-centring pace to 200 ms and
drop the smootherstep half of the curve (plain sine in-out), shared by the glide and the crossing
morph so expand, collapse and scroll stay one motion.

## Notes

- Modifies `dock/R15`'s motion sentence (spec 200). The hand block-toggle (`dock/R14`, 230 ms) is a
  separate motion and is untouched.
- Spec 200 tuned the pace *up* to 400 ms for single-move smoothness; this is the fast-advance
  condition, the opposite case.
- The per-crossing collapse-clamp reversal (scroll up then clamp back as the departing block
  shrinks) is a separate mechanism, unchanged here — a possible follow-up if the owner's "up and
  down" is that jerk.
- A concurrent slice holds spec 204 (`fix/204-dock-entry-open-reset`); this slice takes 205 and
  ITEM-214, leaving ITEM-213 for spec 204's natural order.

## Acceptance sketch

- A single centring lands 0 px off, 0 reversals, over ~200 ms (sine in-out).
- Rapid advancing (120/200/300 ms cadence) shows a lower mean live-row offset and smaller max frame
  step than develop.
- The E2E deceleration guard still passes; reduced motion stays instant.

## Links

- Spec: [205](../../specs/205-dock-centre-pace/spec.md)
- Related items: ITEM-210 (spec 200, the centre triggers and the 400 ms pace this modifies)