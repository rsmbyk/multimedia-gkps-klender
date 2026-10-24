# ADR 0001: Project process

## Status

Accepted

## Context

The repository had no written process. Work landed on branches with ad-hoc conventions,
with no spec gate, no board, no version identity, and no ADRs. The project needed one
written way of working for humans and agents.

## Decision

This project uses:

- **Specification-driven development with Spec Kit**.
- **Test-driven development** for domain and application rules; **Playwright (Python) E2E**
  for user-visible acceptance.
- **In-repo Kanban board** at `backlog/board.md`, one card per item.
- **Git Flow** — the repository's deviations and additions are in
  [ADR 0002](0002-git-flow-merge-strategy.md).
- **Conventional Commits**.
- **SemVer** with `VERSION`, `CHANGELOG.md`, and annotated `vX.Y.Z` tags.

The repo convention that goes with them — the docs-only exception — is in
[`docs/PROCESS.md`](../PROCESS.md).

## Consequences

- `docs/PROCESS.md` is the process declaration; this ADR records the choice.
- `VERSION` is the in-tree version, `CHANGELOG.md` is the release record, and tags mark
  what shipped.
- Existing specs under `specs/NNN-slug/` stay as dated records.
- The board is the source of truth for demand; cards move with the work.
