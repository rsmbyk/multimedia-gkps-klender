---
id: ITEM-130
status: done
title: Follow the Vex process grammar from memory
type: chore
priority: P2
effort: S
created: 2026-10-24
updated: 2026-10-24
spec:
branch: docs/vex-process
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/379
issue:
closed_at:
closed_reason:
bump: none
release_version:
---

# ITEM-130: Follow the Vex process grammar from memory

## Summary

The process this repository declares is prose, written into the repository itself, so it is a copy
that drifts: the grammar has moved on and nothing here would learn about the next change. Point the
repository at the grammar in shared memory, and generate `docs/PROCESS.md` from its rule index —
every rule of the selected parts, verbatim and in ID order, with this repository's own conventions
preserved in `repo:` blocks.

## Notes

- Docs and repository tooling only: `bump: none`, no numbered spec (the docs-only convention).
- Generated with the `vex-process` skill, which reads the rule index for wording and never invents a
  rule.
- The `repo:` blocks carry the docs-only exception, the tests' scope and location, the branch-cleanup
  and force-push rules, the changelog archive, and the anchor label — each once.
- `AGENTS.md` shrinks to what this repository uses, that the process is binding, and where the rest
  lives: no rule text, no rule IDs.
- [ADR 0006](../../docs/adr/0006-process-grammar.md) records the choice.
- This card rides the owner's word rather than a `Ready` promotion, and takes no issue anchor until
  the owner creates one.
- `specs/_templates/preview/README.md` is the one template behind the grammar — it lacks the mockup
  tier added on 2026-10-22 — and is brought up to the normative block here.

## Acceptance sketch

- `docs/PROCESS.md` carries every ID of the five selected parts and of the nine contracts, and no ID
  from an unselected part.
- The `repo:` blocks hold exactly the conventions above, once.
- `AGENTS.md` carries no rule text and no rule IDs.
- `docs/adr/0006-process-grammar.md` records the choice, the vintage and the precedence.
- Every template matches the grammar's normative block.
- `backlog/board.md` carries this card; `CHANGELOG.md` is untouched (`bump: none`).

## Links

- Spec: —
- Related items: ITEM-123 (the declaration this replaces), ITEM-128 (the tracker mirror it carries),
  ITEM-000 (the original adoption)
