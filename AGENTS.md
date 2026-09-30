# Agent notes

Project conventions for humans and coding agents. Prefer these docs over guessing.

This repository **adopts the vexbook process at `v0.4.0`** (see
[`docs/adr/0001-adopt-vexbook-process.md`](docs/adr/0001-adopt-vexbook-process.md)).
It is an **adopter**, not a greenfield spawn.

## Process (vexbook — binding)

- **Way of working:** [`docs/PROCESS.md`](docs/PROCESS.md)
- **Must-apply gate:** [`docs/rules/SDD-GATE.md`](docs/rules/SDD-GATE.md) — plan stops at
  Draft specs; do **not** implement until the owner Accepts the Draft. This is the
  current must-apply shared doc listed by PROCESS.
- **Existing repo / keep-up:** [`docs/ADOPT.md`](docs/ADOPT.md) — owner-triggered only; agents
  never sync unprompted. The greenfield path is [`docs/KICKOFF.md`](docs/KICKOFF.md) (kept for
  reference).
- **Specs:** `specs/NNN-slug/{plan,spec,tasks}.md` from [`specs/_template/`](specs/_template/);
  consecutive integers; **spec 000** is the whole scaffold and stays one spec; one concern per
  spec. Backfill of as-built behavior is a separate, owner-accepted slice.
- **Board:** [`backlog/board.md`](backlog/board.md) with `ITEM-XXX` files under
  [`backlog/items/`](backlog/items/) from [`_template.md`](backlog/items/_template.md). Only the
  **Backlog** column is sorted by priority (P0 first). Board, tasks, and version (when `bump` is
  not `none`) land in **the same PR** as the work.
- **Versioning:** SemVer is locked. Identity is repo-root [`VERSION`](VERSION) (one line, no `v`),
  [`CHANGELOG.md`](CHANGELOG.md), and annotated tags `vX.Y.Z`. The ITEM/spec carries
  `bump: major | minor | patch | none`. `VERSION` continues from the highest tag shared with the
  parallel `develop` line (currently `0.5.2`); see ADR 0001.
- **Git:** **Git Flow** — `main` is production, `develop` is integration (see
  [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and
  [`docs/adr/0002-git-flow-merge-strategy.md`](docs/adr/0002-git-flow-merge-strategy.md)).
  - Features (`feat/*`, `fix/*`, `chore/*`, `docs/*`) branch from `develop` and **squash-merge into
    `develop`**.
  - Releases (`release/*`) and hotfixes (`hotfix/*`) target `main` and use a **standard merge
    commit**; every merge into `main` is a merge commit, never a squash.
  - After a merge, **delete the remote branch only; keep the local branch intact**.
  - Never create vendor/agent-named branches; never force-push `main` or `develop`.
- **Commits:** Conventional Commits (`type(scope): imperative subject`). Agent commits end with a
  `Co-authored-by` trailer for the vendor product that authored the commit — never another
  vendor's trailer. Open **draft** PRs using the repository PR template.

## Product (this repo)

- **What:** worship multimedia for GKPS Klender — Bible, Songs, Tata Ibadah (service order), and
  Bookmarks, plus live OBS projection sources. See [`docs/PRODUCT.md`](docs/PRODUCT.md) and
  [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).
- **Stack:** Python 3.12 + Django 4.0 + Django REST Framework; PostgreSQL; WhiteNoise; deployed on
  Vercel (`@vercel/python`). Frontend is server-rendered templates with vanilla JS, jQuery, RxJS,
  and Fomantic UI.
- **Tests:** Django test runner; coverage via `coverage`. E2E is Playwright (Python) via Django
  `LiveServerTestCase`. TDD for domain/application rules.
- **Vocabulary:** use the canonical terms and naming rules in
  [`docs/GLOSSARY.md`](docs/GLOSSARY.md) for all new work.
- **Conventions:** Git Flow ([ADR 0002](docs/adr/0002-git-flow-merge-strategy.md)), Keep a
  Changelog, `VERSION` (currently `0.6.0`).

## This agent's rules

OpenCode reads this `AGENTS.md` as its project-rules file; it is the vendor loader for the binding
docs above. When PROCESS adds a must-apply shared doc, update the process section here as well. Do
not add or commit vendor agent directories.
