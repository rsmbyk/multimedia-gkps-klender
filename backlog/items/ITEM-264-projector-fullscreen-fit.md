---
id: ITEM-264
status: done
title: 'Projector words stay at the windowed size after fullscreen'
type: fix
priority: P1
effort: S
created: 2026-11-27
updated: 2026-11-27
spec: '247-projector-fullscreen-fit'
branch: fix/247-projector-fullscreen-fit
pr: 637
issue:
closed_at: 2026-11-27
closed_reason: merged into develop (PR #637)
bump: patch
release_version:
---

# ITEM-264: Projector words stay at the windowed size after fullscreen

## Summary

Switching the projector page between full screen and windowed leaves the fitted words and heading at
the old size, so the larger fullscreen stage has empty space above and below the text. It happens
with the F key, the mouse zones and F11.

## Notes

The fit is recomputed on resize, on the bundled faces arriving and on a header rewrite, but not on a
fullscreen signal. A transition that changes the stage without a window resize therefore leaves the
old inline font size and remembered fit in place. The slice re-fits the screen on the stage on the
next frame after `fullscreenchange` and after a `(display-mode: fullscreen)` change; a Go To detour
on the stage is fitted too.

## Acceptance sketch

- A fullscreen transition that grows the stage re-fits the active words and heading.
- A transition back restores the original size; a repeat signal at the same stage changes nothing.
- F11, which has no `fullscreenElement`, re-fits through the display-mode signal.
- The cue, key sheet, media controls and the existing resize answer are unchanged.

## Links

- Spec: `specs/247-projector-fullscreen-fit/spec.md`
- PR: [#637](https://github.com/rsmbyk/multimedia-gkps-klender/pull/637)
