---
id: ITEM-175
status: backlog
title: The section-break divider measures 8px where its test expects 0px
type: fix
priority: P2
effort: S
created: 2026-10-29
updated: 2026-10-29
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-175: The section-break divider measures 8px where its test expects 0px

## Summary

`tests.e2e.test_tatib_section_break.SectionBreakE2ETests.test_the_divider_takes_the_same_box_as_the_entries`
reads the divider's box as `['8px', '8px']` and the assertion wants `['0px', '0px']`. The divider carries
8px the entries do not, or the assertions were written before the entries' own padding moved.

## Notes

- Reproduced on `3e005688^` (develop without spec 155), 2.5 s, same two values — pre-existing.
- Spec 143's add-bar work and spec 144's spacing changed the rows around this divider; read that
  history before deciding which side is wrong.

## Acceptance sketch

- The divider's box matches the entries' — either the 8px goes or the assertion is corrected with the
  measured reason.

## Links

- Spec: none yet
- Related items: ITEM-143 (add bar), ITEM-144
