---
id: ITEM-248
status: done
title: 'The referenced-verse notice is missed below the action row'
type: fix
priority: P2
effort: S
created: 2026-11-23
updated: 2026-11-23
spec: 232-verse-reference-notice
branch: feat/232-verse-reference-notice
pr: 608
issue: 607
closed_at: 2026-11-23
closed_reason: merged into develop (PR #608)
bump: patch
release_version:
---

# ITEM-248: The referenced-verse notice is missed below the action row

## Summary

When a song verse is named by a Tata Ibadah, its editor disables `Delete verse` and prints a 12px
sentence *below* the action row. A reader meets a faded red button before the sentence explains why.
The reason should sit in the row beside the button, and the disabled button should read as unavailable
rather than as a faded danger action.

## Notes

- The notice is emitted in `multimedia/web/templates/reading/_editor_form.html`; the dialog body is
  fetched on every open, so a script-side rewrite would be lost on reopen.
- The count is verse-level (`views.py:181-184`), not the song-wide count at `views.py:2452`.
- Owner chose the B · Inline preview on 2026-11-23: one line beside the buttons, no extra row height
  at desktop width, neutral Delete. At 650px and below the note wraps above the buttons.
- Spec 189 had recorded a neutral disabled button ("never a faded danger"); the shipped CSS faded the
  red button at `opacity: .5`.

## Acceptance sketch

- The note leads `.editor__actions` with `Used in <count> Tata Ibadah — delete unavailable`.
- The disabled Delete has opacity 1 and uses `--rail-bg`, `--divider` and `--head-ink`.
- The desktop row stays 38px; at 420px the note takes a full-width line above a right-aligned button row.
- An unreferenced verse, other editors and the delete endpoint are unchanged.

## Links

- Spec: [232](../specs/232-verse-reference-notice/spec.md)
- Related items: ITEM-241 (the verse modal header rule), ITEM-246 (the add-verse control)
