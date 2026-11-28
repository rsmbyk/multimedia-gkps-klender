---
id: ITEM-266
status: done
title: 'Go To detour words stay at the old size after fullscreen'
type: fix
priority: P1
effort: S
created: 2026-11-27
updated: 2026-11-27
spec: '249-goto-fullscreen-fit'
branch: fix/249-goto-fullscreen-fit
pr: 638
issue:
closed_at: 2026-11-27
closed_reason: merged into develop (PR #638)
bump: patch
release_version:
---

# ITEM-266: Go To detour words stay at the old size after fullscreen

## Summary

After spec 247, switching to full screen still leaves a passage Go To's words at the windowed size
when the geometry change arrives as a resize — the operator's F11, or a page gesture whose
`fullscreenchange` lands before the viewport grows.

## Notes

`render()` fits service screens only and `fitNeighbours()` deliberately skips a Go To detour, so
the detour was never fitted by the resize path. The resize listener now calls spec 247's
stage-screen fit as well, so whichever screen is actually on the stage follows the new geometry.

## Acceptance sketch

- A Go To detour grows and shrinks with the stage on a resize.
- A `fullscreenchange` before the resize cannot freeze the detour at the old size.
- With no detour, service screens and their neighbour fits behave exactly as before.

## Links

- Spec: `specs/249-goto-fullscreen-fit/spec.md`
- PR: [#638](https://github.com/rsmbyk/multimedia-gkps-klender/pull/638)
