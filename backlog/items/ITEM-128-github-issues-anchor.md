---
id: ITEM-128
status: in-review
title: Anchor board cards on GitHub Issues
type: chore
priority: P2
effort: S
created: 2026-10-24
updated: 2026-10-24
spec:
branch: docs/tracker-mirror
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/377
issue: 376
closed_at:
closed_reason:
bump: none
release_version:
---

# ITEM-128: Anchor board cards on GitHub Issues

## Summary

The board lives in the repo and nothing on GitHub points at it: a pull request cites a spec and
a card, and neither can be followed back from it. Declare the grammar's tracker mirror in this
repo — one GitHub issue per card, referenced by `Refs` and never `Closes` — and put the single
label it needs in place, so a card that enters `Ready` gains an anchor without further setup.

## Notes

- Docs and repository tooling only: `bump: none`, no numbered spec (the docs-only convention).
- The mirror is an anchor, not a sync: nothing is read back from the issue, and the in-repo
  board stays the only source of truth.
- [ADR 0005](../../docs/adr/0005-github-issues-anchor.md) records the choice;
  [`docs/PROCESS.md`](../../docs/PROCESS.md) carries the state.
- Cards that predate the mirror keep an empty `issue:`; history is not backfilled.
- This card is anchored on the owner's word rather than at `Ready` — it takes the docs-only
  shortcut, and its issue is the wiring's first live use.
- The pull request template's `Refs` line stops being a placeholder once an anchored card's PR
  fills it.

## Acceptance sketch

- `docs/PROCESS.md` names the tracker mirror.
- ADR 0005 records the choice, the timing, and that it carries no deviation from the grammar.
- The repository has one anchor label, `board:item`.
- A card that enters `Ready` gains an issue whose number is written into `issue:` in the same
  commit that moves the card.

## Links

- Spec: —
- Related items: ITEM-123 (the process declaration this extends)
