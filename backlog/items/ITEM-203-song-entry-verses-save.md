---
id: ITEM-203
status: done
title: 'A new song entry saves with the verses that were picked'
type: fix
priority: P1
effort: S
created: 2026-11-15
updated: 2026-11-15
spec: 195
branch: fix/195-hotfix-batch
pr: 523
issue: 520
closed_at: 2026-11-15
closed_reason: merged into develop (PR #523)
bump: patch
release_version: 1.32.1
---

# ITEM-203: A new song entry saves with the verses that were picked

## Summary

Saving a new song entry refuses every pick: the checklist submits verse numbers while the server (since spec 189) validates verse IDs, so every save fails with "Select a valid choice" plus "Keep at least one verse in the service". After the refused save the re-rendered checklist carries ID values and its summary reads "Verses 3971, 3973" — IDs, not numbers — and the server-rendered checkboxes are unstyled.

## Notes

- `entry_song_verses` (the picker's fetch) returns verse numbers; `renderVerses` makes them the checkbox values; `SongEntryForm` offers verse IDs (choices `(id, number)`).
- The summary helper reads `input.value`, so a server-rendered checklist reads as IDs.
- The server-rendered checklist (`{{ form.verses }}`, a `<ul>`) has no styling, unlike the client-rendered one.

## Acceptance sketch

- A fresh song entry saves with the picked verses and paints "Bait 1, 3"-style numbers.
- The verses summary names verse numbers in both the fresh and the re-rendered checklist.
- The server-rendered checklist looks like the client-rendered one.

## Links

- Spec:
- Related items:
