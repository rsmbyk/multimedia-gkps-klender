---
id: ITEM-219
status: in review
title: 'The live entry header''s corners follow its pin state'
type: fix
priority: P1
effort: S
created: 2026-11-20
updated: 2026-11-20
spec: specs/208-dock-stuck-corner/spec.md
branch: fix/208-dock-stuck-corner
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/551
issue:
closed_at:
closed_reason:
bump: minor
release_version:
---

# ITEM-219: The live entry header's corners follow its pin state

## Summary

The owner reports two inconsistent states of the runner's live entry header: pinned at the list's
top edge but with rounded top corners, and sitting in normal flow but with square ones. The flat
top is the `.is-stuck` class, toggled only inside `updateBand()` behind the NEXT band's motion
guard — so every scroll a glide or crossing generates is swallowed, nothing re-runs after the
300 ms hold, a crossing measures the new live header against the old scroll position, and
height-only block toggles never re-measure at all. The corner state must track the header's actual
geometry on every path that moves the list.

## Notes

- Reproduced on `develop` at `c385a194` (63404, 420 × 860, HAL 1 with 21 screens): pinned at
  delta 0 px with no class and 9 px radius; after Ctrl+Home, in flow at delta 4 px with the class
  and 0 px radius. One hand scroll reconciles both — the toggle works, its invocation is the bug.
- The band's guard stays for the band (reparenting mid-glide shifts layout); the corner class is
  paint-only and leaves the guard.
- "Pinned" gains the block-still-below clause: a header scrolled out above the list is not stuck.
- Only the live header may wear the class; a header losing liveness loses it in the same paint.
- Scope: the service entry list only — the go to's `.offstrip` and the reading page's pinned
  header carry no corner state.
- The branch and worktree existed empty (cut 2026-11-19 from `85319b73`, no commits, no PR); this
  slice fast-forwarded the branch to `c385a194` and took the claim over.

## Acceptance sketch

- A pinned header at rest wears `.is-stuck` and 0 px top radius, with no hand scroll after the
  advance that pinned it; an in-flow header at rest has no class and 9 px radius.
- A hand-opened block above the pinned header rounds its corners without a scroll event.
- During a glide or morph the class flips on the frame the geometry crosses the pin line; the old
  live row loses the class on the crossing paint; reduced motion reconciles instantly.
- The NEXT band's guard, yield and hold are unchanged; the existing dock E2E modules stay green.

## Links

- Spec: `specs/208-dock-stuck-corner/spec.md`
- Related items: ITEM-208 (spec 198 — headers toggle, items jump), ITEM-210 (spec 200 — following
  and the named centring acts), ITEM-214 (spec 205 — the shared 200 ms pace), ITEM-216 (spec 204 —
  an open starts every block shut)
