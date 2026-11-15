---
id: ITEM-204
status: done
title: 'A song lyric never paints more than two lines on the overlay'
type: fix
priority: P1
effort: S
created: 2026-11-15
updated: 2026-11-15
spec: 195
branch: fix/195-hotfix-batch
pr: 523
issue: 521
closed_at: 2026-11-15
closed_reason: merged into develop (PR #523)
bump: patch
release_version: 1.32.1
---

# ITEM-204: A song lyric never paints more than two lines on the overlay

## Summary

A song screen whose lyric lines are long wraps past the two-line caption the overlay was designed around — three, four, five rows of text stack up. The type should shrink so every screen paints at most two visual lines, never more.

## Notes

- The overlay's own spec records the two-line caption as the accepted shape (a two-line lyric at 1080p paints 1728×202); spec 183 added wrapping but let the block grow by every wrapped row.
- The plate kinds (passage, liturgy) are out of scope — the request names the song lyric only.

## Acceptance sketch

- A two-line lyric that fits paints exactly as before (same numbers).
- A lyric whose lines wrap shrinks its type so the whole block stays within two visual lines.
- No screen ever paints a third visual line.

## Links

- Spec:
- Related items:
