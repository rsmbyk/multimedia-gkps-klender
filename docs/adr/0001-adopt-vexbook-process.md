# ADR 0001: Adopt vexbook process at v0.4.0

## Status

Accepted

Owner-triggered first-time adopt of the **vexbook** process into this existing product, per [`docs/ADOPT.md`](../ADOPT.md). This is an adopter ADR, so the spawn-style ADR 0001 (process) / 0002 (product) layout does **not** apply and existing ADR numbers are not renumbered.

## Context

This product had no written process: no spec gate, no ITEM board, no version identity, and no ADRs. Work landed directly on branches with ad-hoc conventions. The owner asked to adopt the vexbook process from the latest release so humans and agents share one way of working.

Source: vexbook tag **`v0.4.0`** (`https://github.com/rsmbyk/vexbook`). No automatic sync — the owner triggers adopt or keep-up.

## Decision

- Adopt the vexbook process at **`v0.4.0`**.
- The **process file set** was copied verbatim from that tag:
  - [`docs/PROCESS.md`](../PROCESS.md)
  - [`docs/KICKOFF.md`](../KICKOFF.md)
  - [`docs/ADOPT.md`](../ADOPT.md)
  - [`docs/rules/SDD-GATE.md`](../rules/SDD-GATE.md)
  - `backlog/README.md`, `backlog/items/_template.md`
  - `specs/_template/{plan,spec,tasks}.md`
  - [`docs/adr/_template.md`](./_template.md)
  - [`.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md)
- Per ADOPT, vexbook's `templates/`, backlog/specs history, `VERSION`, and `CHANGELOG.md` history are **not** copied; product history stays local.
- This one thin adoption ADR is recorded at the next free number (**0001**). Further product ADRs continue at 0002+.
- Vendor project rules: the authoring agent (OpenCode) reads [`AGENTS.md`](../../AGENTS.md) as its project-rules file; it references every must-apply shared doc from PROCESS. No vendor directory is committed.
- An empty ITEM board and a fresh `specs/` index were created so the board and reusable stubs exist after the copy.

## Consequences

- [`PROCESS.md`](../PROCESS.md), [`KICKOFF.md`](../KICKOFF.md), and [`rules/SDD-GATE.md`](../rules/SDD-GATE.md) are **binding** for this repository.
- Every behavior, CSS, or copy change now follows SDD: Plan → Draft → owner Accept → implement ([`docs/rules/SDD-GATE.md`](../rules/SDD-GATE.md)).
- `VERSION` is **`0.5.2`** — the highest existing tag in the repository. Tags `v0.4.8`–`v0.5.2`
  belong to the parallel `develop` line and are already published, so continuing from `0.5.2` keeps
  the shared tag namespace collision-free. This is an identity bootstrap, not a release; the
  adoption itself has `bump: none`. The next feature bump is therefore `0.6.0`.
- Gaps observed and resolved with the owner (see [`docs/ARCHITECTURE.md`](../ARCHITECTURE.md) and [`docs/PRODUCT.md`](../PRODUCT.md)):
  - Git model: **Git Flow** — confirmed and detailed in
    [ADR 0002](0002-git-flow-merge-strategy.md).
  - Product `CHANGELOG.md` converted to the Keep a Changelog structure; pre-adoption history
    preserved in [`docs/CHANGELOG-archive.md`](../CHANGELOG-archive.md).
  - E2E tool: **Playwright (Python)** driven from Django `LiveServerTestCase` and run under
    `python manage.py test` ([`docs/ARCHITECTURE.md`](../ARCHITECTURE.md)).
