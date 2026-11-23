---
id: ITEM-245
status: done
title: 'Add verse is dead on a song opened from the sidebar'
type: fix
priority: P1
effort: S
created: 2026-11-23
updated: 2026-11-23
spec: 230-song-verse-script-boot
branch: fix/230-song-verse-script-boot
pr: 602
issue: 601
closed_at: 2026-11-23
closed_reason: merged into develop (PR #602)
bump: patch
release_version:
---

# ITEM-245: Add verse is dead on a song opened from the sidebar

## Summary

Reaching a song through the reading shell's sidebar swaps its markup into the page without a
reload. The song fragment carries the only `songs_verse.js` include, and a script inserted by
`importNode` never executes, so every verse control on that page is unbound. Refreshing the
page runs the script and the controls work. Measured at 1440×900 on `/songs/1387/`: after the
three sidebar clicks the dialog stays closed, while a direct load opens it.

## Notes

- The fix is to boot `songs_verse.js` from `reading/base.html`, where all other reading
  scripts live, and remove the fragment's include so a direct load does not bind twice.
- The script's handlers are delegated on `document`, so one boot covers every later swap.
- Out of scope: verse write endpoints, permissions, button styling and the standalone
  projector/OBS pages, which are not fragments of the reading shell.

## Acceptance sketch

- From `/`, three sidebar clicks to a song and then `Add verse` opens `New verse` without a
  refresh.
- `Edit verse` on the same path opens the numbered editor.
- A direct song load still opens both dialogs and has exactly one script include.
- The button's box and all verse markup, endpoints and guards are unchanged.

## Links

- Spec: [230-song-verse-script-boot](../../specs/230-song-verse-script-boot/spec.md)
- Related items: ITEM-193 (song verse editing), ITEM-239 (empty song Add verse)
