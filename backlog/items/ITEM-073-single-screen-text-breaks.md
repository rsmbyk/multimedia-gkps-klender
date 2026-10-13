---
id: ITEM-073
status: done
title: Manual breaks for Single-screen Text entries
type: feat
priority: P2
effort: M
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/070-single-screen-text-breaks/spec.md
branch: feat/069-manual-text-screen-breaks
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/323
archived_at:
archive_reason:
bump: minor
release_version: 1.7.0
---

# ITEM-073: Manual breaks for Single-screen Text entries

## Summary

Reuse the preview-modal screen-break interaction for Single-screen Text entries. Their complete body remains on one fitted projector screen by default; an editor can save custom breaks when several screens are needed.

## Notes

- Depends on Spec 069, which supplies the modal interaction and saved-break metadata for ordinary Text entries.
- Blank lines remain paragraph spacing in this entry kind. Reset breaks restores its one-screen default.

## Acceptance sketch

- Preview shows `Default · 1 screen` with no active break until an editor changes a gap.
- The first added break divides the content into two fitted screens; subsequent clicks toggle one boundary.
- Custom screens preserve the entry title and speaker cues, update an open projector, and keep the trailing built-in blank screen.
- Reset and later text edits follow the accepted spec's default and stale-break rules.

## Links

- Spec: [Spec 070](../../specs/070-single-screen-text-breaks/spec.md)
- Related item: [ITEM-072 in PR #323](https://github.com/rsmbyk/multimedia-gkps-klender/pull/323)
