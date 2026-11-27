---
id: ITEM-241
status: done
title: 'The verse modal header paints two rules'
type: fix
priority: P2
effort: S
created: 2026-11-23
updated: 2026-11-23
spec: 226-verse-modal-header-rule
branch: fix/226-verse-modal-header-rule
pr: 594
issue: 593
closed_at: 2026-11-23
closed_reason: merged into develop (PR #594)
bump: patch
release_version: 1.37.3
---

# ITEM-241: The verse modal header paints two rules

## Summary

Opening `New verse` or `Edit verse n` shows a short rule under the title and a second, full-width
rule under the header. The large-editor CSS also gives the title a bottom border, which outranks the
header's `border: 0` reset. The header should carry only its own divider.

## Notes

- Measured on `develop` at `4ad9e6ff`: the title border is 157.0px wide at y=142.5; the head rule
  is 840px wide at y=157.5, with a 37.5px gap under the title text.
- The non-verse `New song` editor measures a 16px title-to-divider gap; that is the target for the
  verse header (16.5px with the 21px title's line box).
- The large-editor rule is `static/styles/design/components.css:541`; the reset it outranks is at
  line 689.
- The report came from a deployed build that labels the field `Lyrics`; the current build labels it
  `Lyric`, but both paint the same two rules.

## Acceptance sketch

- A verse dialog, new or edit, paints one header rule — the full-width `.editor__head` divider.
- The title's computed bottom border is `0px`; its 21px font, 21px top gap and x=289 text inset
  stay, and the title-to-divider gap is 16.5px (16px in the other editors).
- Non-verse editors, loading state, form fields and actions are unchanged.

## Links

- Spec: [226](../specs/226-verse-modal-header-rule/spec.md)
- Related items: ITEM-201 (the header row this rule was ported with), ITEM-226 (modal layers)
