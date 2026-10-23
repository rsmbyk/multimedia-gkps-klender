---
id: ITEM-123
status: in-review
title: Declare the project process and conventions
type: chore
priority: P1
effort: M
created: 2026-10-23
updated: 2026-10-23
spec:
branch: docs/project-process
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/371
issue:
closed_at:
closed_reason:
bump: none
release_version:
---

# ITEM-123: Declare the project process and conventions

## Summary

Write down what this project uses and the convention that goes with it, retire the old process
copies, put the templates in the repo, and remove the GitHub Actions pipeline. Docs and
repository tooling; `bump: none`.

## Notes

- [`docs/PROCESS.md`](../../docs/PROCESS.md) lists the process and the only repo convention;
  [ADR 0001](../../docs/adr/0001-project-process.md) records the choice.
- Templates live in [`specs/_templates/`](../../specs/_templates/),
  [`backlog/items/_template.md`](./_template.md),
  [`.github/pull_request_template.md`](../../.github/pull_request_template.md) and
  [`docs/adr/_template.md`](../../docs/adr/_template.md).
- The GitHub Actions workflow, its change-scope helper and the helper's test are removed; the
  E2E-tag test stays.
- The board gains the `## Archive` table for cards that ended without shipping.

## Acceptance sketch

- `docs/PROCESS.md` names what the repo uses and its convention.
- ADR 0001 exists.
- The templates are in the repo.
- `AGENTS.md` points at PROCESS.
- The board carries the `## Archive` table.
- The CI pipeline is removed; the E2E-tag test stays.

## Links

- Spec: —
- Related items: ITEM-000 (initial process adoption)
