---
id: ITEM-119
status: in_progress
title: 'Keep public reading navigation consistent with current and saved data'
type: fix
priority: P1
effort: M
created: 2026-10-20
updated: 2026-10-20
spec: specs/119-consistent-reading-navigation/spec.md
branch: fix/119-online-navigation-freshness
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.19.1
---

# ITEM-119: Keep public reading navigation consistent with current and saved data

## Summary

Online in-page navigation can leave list, book, home, and search views on an older saved generation, while full reloads request current server data. Offline same-day Tata Ibadah order also uses ID where Django uses creation time. Make opened reading views consistent without requiring refresh.

## Acceptance sketch

- Online menu, sidebar, result, and history navigation settle on current server data.
- Offline browsing keeps a truthful saved fallback and matches server ordering/layout rules.
- Normal and hard reloads agree with in-page navigation after loading settles.

## Links

- Spec: [119](../../specs/119-consistent-reading-navigation/spec.md)
