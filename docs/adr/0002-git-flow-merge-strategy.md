# ADR 0002: Git Flow deviations

## Status

Accepted

## Context

This project uses Git Flow. This ADR records only the places where the repository's practice
differs from the model, plus the branch-cleanup and protection rules that are repo-specific.

## Decision

- Features (`feat/*`, `fix/*`, `chore/*`, `docs/*`) are **squash-merged into `develop`**.
- A slice's `VERSION` bump lands on `develop`; the `release/*` branch confirms it rather than
  setting it.
- After a merge, delete the **remote** branch only; keep the **local** branch and worktree.
- Never force-push `main` or `develop`; never create vendor/agent-named branches.

## Consequences

- `develop` carries one commit per slice.
- Local branches accumulate by design.
- Recorded in [`docs/ARCHITECTURE.md`](../ARCHITECTURE.md), [`AGENTS.md`](../../AGENTS.md), and
  [`docs/PRODUCT.md`](../PRODUCT.md).
