# Agent notes

Project conventions for humans and coding agents. Prefer these docs over guessing.

This repository follows the process declared in [`docs/PROCESS.md`](docs/PROCESS.md)
and [ADR 0001](docs/adr/0001-project-process.md).

## Process (binding)

- **Specification-driven development with Spec Kit.**
- **Board:** in-repo Kanban at [`backlog/board.md`](backlog/board.md), cards in
  [`backlog/items/`](backlog/items/).
- **Git:** Git Flow; the repository's deviations and additions are in
  [ADR 0002](docs/adr/0002-git-flow-merge-strategy.md).
- **Commits:** Conventional Commits.
- **Versioning:** SemVer. Identity is repo-root [`VERSION`](VERSION),
  [`CHANGELOG.md`](CHANGELOG.md), and annotated tags `vX.Y.Z`.
- **Specs:** `specs/NNN-slug/`; templates in [`specs/_templates/`](specs/_templates/).
- **Tests:** TDD for domain/application rules; Playwright (Python) E2E.

## Repo conventions

- **Docs-only changes** may skip the numbered spec with a short plan and owner approval.

## Product (this repo)

- **What:** worship multimedia for GKPS Klender — Bible, Songs, Tata Ibadah (service order), and
  Bookmarks, plus live OBS projection sources. See [`docs/PRODUCT.md`](docs/PRODUCT.md) and
  [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).
- **Stack:** Python 3.12 + Django 4.0 + Django REST Framework; PostgreSQL; WhiteNoise; deployed on
  Vercel (`@vercel/python`). Frontend is server-rendered templates with vanilla JS, jQuery, RxJS,
  and Fomantic UI.
- **Tests:** Django test runner; coverage via `coverage`. E2E is Playwright (Python) via Django
  `LiveServerTestCase`.
- **Vocabulary:** use the canonical terms and naming rules in
  [`docs/GLOSSARY.md`](docs/GLOSSARY.md) for all new work.

## This agent's rules

OpenCode reads this `AGENTS.md` as its project-rules file; it is the vendor loader for the
process above. [`docs/PROCESS.md`](docs/PROCESS.md) is the declaration.
