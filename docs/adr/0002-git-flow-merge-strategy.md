# ADR 0002: Git Flow merge and branch strategy

## Status

Accepted

Confirms the git model left "to confirm" by [ADR 0001](0001-adopt-vexbook-process.md).

## Context

Vexbook's [`docs/PROCESS.md`](../PROCESS.md) requires each project to pick a git model and record it
in [`docs/ARCHITECTURE.md`](../ARCHITECTURE.md) or an ADR. The owner confirmed Git Flow and the
concrete merge and branch-cleanup rules this repository should follow.

## Decision

- **Git Flow:** `main` is production (deployed to Vercel); `develop` is integration.
- **Features** (`feat/*`, `fix/*`, `chore/*`, `docs/*`) branch from `develop` and are
  **squash-merged into `develop`** — one commit per PR. Default PR target is `develop`.
- **Releases** (`release/*`) branch from `develop`; **hotfixes** (`hotfix/*`) branch from `main`.
  Both target `main`.
- **Every merge into `main` uses a standard merge commit** (never a squash) so release and hotfix
  history is preserved.
- After a release or hotfix lands on `main`, merge `main` back into `develop` so `VERSION` stays
  aligned, then tag `vX.Y.Z` on the `main` commit.
- **Branch cleanup:** after a merge, delete the **remote** branch only. Keep the **local** branch
  intact.
- Never force-push `main` or `develop`; never create vendor/agent-named branches.

## Consequences

- History on `develop` stays compact (one commit per feature PR); history on `main` preserves
  release and hotfix merges.
- Local branches accumulate by design — cleanup is remote-only.
- Recorded in [`docs/ARCHITECTURE.md`](../ARCHITECTURE.md), [`AGENTS.md`](../../AGENTS.md), and
  [`docs/PRODUCT.md`](../PRODUCT.md).
