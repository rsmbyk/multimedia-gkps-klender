# ADR 0005: Anchor board cards on GitHub Issues

## Status

Accepted

## Context

The board lives in the repository and nothing on GitHub points at it. A pull request cites a
spec and a card, but neither the card nor the spec can be followed from the pull request, and a
card cannot be followed to the work that served it without searching. The process grammar's
board part answers this with a **tracker mirror** that is an anchor, not a sync target: one
issue per card, carrying a stable number the pull request references.

## Decision

- **One GitHub issue per card, and no card past `Speccing` without one.** The issue is created when
  the card enters `Ready` — the point at which the work is authorised and a pull request can exist —
  and is backfilled by the agent when it works with a card already in `Ready`, `In progress`,
  `In review` or `Done` that has no `issue:`.
- **The issue holds a number, a title carrying `ITEM-XXX`, and one line pointing at the card.**
  No status, no priority, no assignee, no spec or branch field: each of those would be a second
  place to be wrong.
- **`Refs #NNN` in the pull request, never `Closes`.** Under Git Flow `Closes` fires on a merge
  to the default branch, which would close the anchor at release rather than at `Done`. `Done`
  stays the board's word.
- **The card stores the number** in its `issue:` field, written in the same commit that moves
  the card, so the link survives renames on either side.
- **`board:item` is the only label**, so the issue list can be filtered to anchors.
- **The in-repo board remains the only source of truth.** Nothing is ever read back from the
  issue, and a closed or drifted issue breaks nothing.
- **No deviation from the grammar**: this adopts the board part's mirror as written. The only
  repo-specific choice is the starting point in the consequences below.

## Consequences

- The issue list is not a board; nobody can work from GitHub alone.
- Anchors begin with ITEM-128, created alongside the wiring itself on the owner's word. Cards that
  predate the rule keep an empty `issue:` until an agent works with one: the widening below backfills
  per card, never as a sweep of the board's history.
- Pull request bodies carry a real `Refs #NNN` instead of the template's placeholder.
- An issue that arrives from outside is a report, not an anchor: it becomes a card through the
  board first, and only then gets mirrored.

## Amendment — 2026-10-25

The decision above read, until this date:

> **One GitHub issue per card**, created when the card enters `Ready` — the point at which the
> work is authorised and a pull request can exist.

That wording made the **transition** the trigger, and a card can reach `Ready` or beyond without it:
`ITEM-132` was written at Fold, entered the board as `In progress`, and so never had an issue — the
first card to expose the gap. The grammar's rule (BRD-10) was widened on the owner's instruction:
every card past `Speccing` carries one anchor, the agent creates it whenever it works with a card
that lacks one, and the rule itself — not the owner's `Ready` act — is the authorisation. Nothing
else moved: still one issue per card, still `board:item` only, still `Refs` never `Closes`, still
nothing read back from the issue.
