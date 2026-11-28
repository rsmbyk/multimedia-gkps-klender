---
id: ITEM-269
status: done
title: 'Empty date groups survive the last delete'
type: fix
priority: P1
effort: S
created: 2026-11-28
updated: 2026-11-28
spec: specs/252-empty-date-group/spec.md
branch: fix/252-empty-date-group
pr: 649
issue: 648
closed_at: 2026-11-28
closed_reason: merged into develop (PR #649)
bump: patch
release_version:
---

# ITEM-269: Empty date groups survive the last delete

## Summary

Deleting the last service in a date bucket removes the row in place but leaves the bucket's heading and
`<section>` on screen, so the sidebar shows a group with no children. The same client path serves the
`Templates` group and the unheaded songbook groups; template mode also emits an empty group on a fresh
render. Fix the shared client path and the one renderer that does not already skip empty groups.

## Notes

- Reported first in the services sidebar; all ten grouped surfaces were surveyed with file/line evidence
  in `specs/252-empty-date-group/research.md`.
- Client: `static/web/editors.js` `applyDelete()` retires the section when no rows remain, and hides it
  when a filter has hidden all survivors.
- Server: `multimedia/web/reading/views.py` `_tatib_groups()` emits `Templates` only when templates exist.
- Four E2E pins go red on unmodified develop and green on the fix. One neighbouring sort error is
  byte-identical on unmodified develop and is not part of this card.
- Gate 1 accepted 2026-11-28; card promoted to `Ready`. The tracker anchor issue #648 was created once
  the finding was authorized to be fixed; the PR will say `Refs #648`, never `Closes`.

## Acceptance sketch

- Deleting the last service in a bucket removes its heading on screen and after reload.
- Deleting the last songbook leaves no orphan separator; deleting the last template leaves no group.
- A filtered group hides on the last visible delete and returns when the filter is cleared.
- Other grouped surfaces keep their existing behaviour.

## Links

- Spec: [252](../../specs/252-empty-date-group/spec.md)
- Related items: [ITEM-209](ITEM-209-sidebar-activity.md) (sidebar refresh). The in-place delete path came from spec 190.
