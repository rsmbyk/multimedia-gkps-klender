---
id: ITEM-215
status: backlog
title: 'Two dock-follow "must not centre" E2E tests are red on develop'
type: fix
priority: P1
effort: S
created: 2026-11-19
updated: 2026-11-19
spec: —
branch: —
pr: —
issue: —
closed_at: —
closed_reason: —
bump: —
release_version: —
---

# ITEM-215: Two dock-follow "must not centre" E2E tests are red on develop

## Summary

`test_other_state_notices_never_centre` and `test_scrolling_and_expanding_another_entry_end_following`
(`tests/e2e/test_obs_dock_follow.py`) fail with `1832 != 1873` — identical on the unmodified base
commit `85319b73`, so the failure is not a regression of any open slice. Both assert an exact
`scrollTop == start` after an act that must not centre; a background re-read or the Next band hiding
shrinks the scroll range and the browser clamps `scrollTop` down by about one row (41 px), so the
equality fails while the behaviour is correct (no upward centring: `1832 <= 1873`).

## Notes

- Found while running the push-step dock lane for spec 205; verified red on the base 400 ms code by
  checking out `85319b73:static/web/obs-dock.js` and re-running both tests.
- The motion-verification reference already records the fix: assert `after <= start` for a "must not
  centre" rule, and use the live row's centre offset for positive landing assertions, because the
  scroll maximum itself changes under a reflow.

## Acceptance sketch

- Both tests assert the absence of an upward glide (`after <= start`) rather than exact equality, and
  pass on develop without changing the behaviour they guard.

## Links

- Spec: —
- Related items: ITEM-210 (spec 200, the module these tests guard), ITEM-184 (other known-red E2E)