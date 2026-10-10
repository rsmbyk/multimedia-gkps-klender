---
id: ITEM-055
status: done
title: 'Give each entry the height of its floating controls'
type: chore
priority: P2
effort: S
created: 2026-10-10
updated: 2026-10-10
spec: specs/053-entry-controls-height/spec.md
branch: fix/053-entry-controls-height
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/306
archived_at:
archive_reason:
bump: patch
release_version: 1.3.19
---

# ITEM-055: Give each entry the height of its floating controls

## Summary

Preview / Edit / Delete float over an entry's top-right corner (`position: absolute; top: 8px`), so on
untitled entries they sit on the first text line and on titled entries they crowd the title. Each entry
that renders the controls reserves a top band for them (~44px: 8px offset + 36px measured control
height); its title or first line always starts below the band.

## Notes

- Amends spec 033 ("over the words"): the overlap goes away; position, reveal, and touch behavior stay.
- The hover fill (spec 034) already paints the item's whole box, so the band needs no extra highlight rule.
- A modifier class on `.tatib__item` (set where `.entry__acts` is emitted in `tatib.html`) keeps
  items without controls tight.
- `tatib__eos` items are out of scope: a break is a rule, not a text block.
- Owner asked for this on 2026-10-10 while reviewing the pane with spec 052 (hidden add rows).

## Acceptance sketch

- On every entry with controls — titled or not — the controls never overlap a word, at any width.
- Reveal on hover/focus and always-on-touch behavior are unchanged.
- An item that renders no controls reserves no band; the hovered row (band + text) highlights as one.

## Links

- Spec: [053 — Give each entry the height of its floating controls](../../specs/053-entry-controls-height/spec.md)
- Related items: ITEM-035 / spec 033 (float entry controls), ITEM-036 / spec 034 (hover highlight), ITEM-054 / spec 052 (pane resting space)
