---
id: ITEM-267
status: done
title: 'Each OBS dock entry header shows its kind'
type: feat
priority: P2
effort: S
created: 2026-11-28
updated: 2026-11-28
spec: '250-dock-entry-kind-icons'
branch: feat/250-dock-entry-kind-icons
pr: 641
issue: 642
closed_at: 2026-11-28
closed_reason: merged into develop (PR #641)
bump: patch
release_version: 1.37.9
---

# ITEM-267: Each OBS dock entry header shows its kind

## Summary

In the OBS dock's runner, entry headers say what they are in words but give no quick visual cue. Each
non-break header now carries a small icon of its kind immediately left of the chevron, using the
glyphs the reading page already draws for its contents rows.

## Notes

- The four marks are drawn from `reading/_toc_mark.html`: book for passage, note for song,
  play-frame for media, three rules for text. A section break stays a bare hairline.
- The mark carries the trailing margin so the chevron keeps its old position and stays centred on
  a wrapped row. The live row keeps its mark after the chevron hides.
- Verified with two new E2E behaviours and targeted chevron, wrap and pin regressions; the full
  browser matrix waits for the push step.

## Acceptance sketch

- Every text, passage, song and media header renders one mark of its own beside its chevron.
- A break row renders neither mark nor chevron.
- On a multi-line header the mark and chevron are centred on the whole row with a 10px gap.
- The live header keeps the mark in live ink while its chevron is hidden.

## Links

- Spec: `specs/250-dock-entry-kind-icons/spec.md`
- Related items: ITEM-208 (entry toggle), ITEM-203 (long-word wrap)
