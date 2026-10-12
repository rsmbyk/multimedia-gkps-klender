---
id: ITEM-069
status: in_progress
title: 'Always show a song entry''s verses on the Tata Ibadah stage'
type: fix
priority: P2
effort: S
created: 2026-10-12
updated: 2026-10-12
spec: 066
branch: fix/066-stage-song-verse-line
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.6.4
---

# ITEM-069: Always show a song entry's verses on the Tata Ibadah stage

## Summary

The stage's `Bait …` line under a song entry only appears when the entry keeps some, not all,
of its song's verses (spec 054). Most entries keep every verse, so the line looks like it went
missing, while the sidebar always shows it (spec 057). Show it on the stage for every song
entry with verses, in the same format as the sidebar.

## Notes

- Owner reported the line "gone" on 2026-10-12; it was never removed — spec 054's
  partial-only rule hides it on full selections.
- Owner OKed always showing it on 2026-10-12. Deleted targets keep showing no line.
- Spec 066 accepted on 2026-10-12.

## Acceptance sketch

- A full selection shows `Bait 1-3` on the stage; a partial one still shows `Bait 1, 3`.
- The stage line equals the sidebar's second line for the same entry.
- A deleted target shows the warning and no verse line.

## Links

- Spec: [066](../../specs/066-stage-song-verse-line/spec.md)
- Related items: ITEM-056 (spec 054), ITEM-059 (spec 057), ITEM-062 (spec 060)
