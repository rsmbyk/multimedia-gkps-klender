---
id: ITEM-000
status: done
title: Adopt the project process
type: chore
priority: P0
effort: M
created: 2026-09-30
updated: 2026-10-23
spec:
branch:
pr: 256
issue:
closed_at:
closed_reason:
bump: none
release_version:
---

# ITEM-000: Adopt the project process

## Summary

Adopt the project process: specification-driven development with Spec Kit, an in-repo
Kanban board, Git Flow, Conventional Commits, SemVer, and TDD. Docs-only; `bump: none`.

## Notes

- The process is declared in [`docs/PROCESS.md`](../../docs/PROCESS.md);
  [ADR 0001](../../docs/adr/0001-project-process.md) records the choice.
- `VERSION` is the in-tree version, `CHANGELOG.md` is the release record, and annotated
  tags mark what shipped.
- `CHANGELOG.md` uses the Keep a Changelog structure; pre-adoption history is archived in
  `docs/CHANGELOG-archive.md`.

## Acceptance sketch

- Process declaration present.
- ADR 0001 exists.
- Board and `specs/` scaffolding exist.
- `AGENTS.md` points at the process declaration.

## Links

- Spec: — (docs-only)
- Related items: ITEM-123 (current process conventions)
