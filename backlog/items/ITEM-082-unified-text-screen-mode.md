---
id: ITEM-082
status: in_progress
title: Use one Text entry with a selectable screen mode
type: feat
priority: P2
effort: L
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/079-unified-text-screen-mode/spec.md
branch: feat/079-unified-text-screen-mode
pr:
archived_at:
archive_reason:
bump: minor
release_version: 1.10.0
---

# ITEM-082: Use one Text entry with a selectable screen mode

## Summary

Unify Multi-line and Single-screen Tata Ibadah Text entries. Keep their current default projector behavior and manual breaks, but choose the default on Create and manage it in a three-state Preview footer switch.

## Notes

- PR #323 delivered manual breaks for two separate entry kinds. This item covers the proposed consolidation and switch that remained separate from Specs 069–071.
- The owner reviewed the Create/Edit and Preview footer mockups in light and dark themes. The revised form has the switch only on Create; Preview handles changes after creation.
- Custom is an icon-only status entered by editing break lines, never by clicking the middle segment.
- Switching from Custom to a default asks before clearing saved breaks; switching between defaults does not.

## Acceptance sketch

- Existing entries migrate to one Text kind with unchanged words, order, break positions, and projector output.
- Create offers Multi-line and Single-screen with icons; Edit has no mode switch.
- Preview shows the three-state switch instead of Reset breaks and the mode badge.
- A custom break selects the middle status; leaving it requires confirmation and refreshes an open projector.

## Links

- Spec: [Spec 079](../../specs/079-unified-text-screen-mode/spec.md)
- Related: [Spec 069](../../specs/069-manual-text-screen-breaks/spec.md), [Spec 070](../../specs/070-single-screen-text-breaks/spec.md), and [Spec 071](../../specs/071-preview-keyboard-scroll/spec.md)
