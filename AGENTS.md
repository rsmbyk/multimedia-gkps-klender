# Agent notes

Project conventions for humans and coding agents. Prefer these docs over guessing. OpenCode reads
this file as its project-rules file; it is the vendor loader for the process below.

The process in [`docs/PROCESS.md`](docs/PROCESS.md) is binding. Every agent follows it for every
change, without being asked.

## What this repo uses

| Part | Choice |
| --- | --- |
| Specification | `sdd` — Spec Kit's loop: eleven stages, two owner gates |
| Tests | `tdd` — classicist; Playwright (Python) E2E for user-visible acceptance |
| Git | `git-flow`; the repository's deviations are in [ADR 0002](docs/adr/0002-git-flow-merge-strategy.md) |
| Versioning | `semver` — `VERSION`, `CHANGELOG.md`, annotated `vX.Y.Z` tags |
| Board | `kanban`, in-repo at [`backlog/board.md`](backlog/board.md) |
| Tracker mirror | GitHub Issues as an anchor — `Refs`, never `Closes` |

**Precedence:** repo conventions → Vex version → original.

## Where the rest lives

- Rules: [`docs/PROCESS.md`](docs/PROCESS.md)
- Decisions: [`docs/adr/`](docs/adr/) — [ADR 0001](docs/adr/0001-project-process.md) records the
  process choice, [ADR 0006](docs/adr/0006-process-grammar.md) the grammar it follows
- Slices: `specs/NNN-slug/`; templates in [`specs/_templates/`](specs/_templates/)
- Board: [`backlog/board.md`](backlog/board.md), cards in [`backlog/items/`](backlog/items/)
- Current behaviour: `docs/spec/`
- Release record: [`CHANGELOG.md`](CHANGELOG.md) + [`VERSION`](VERSION)
- Vocabulary: [`docs/GLOSSARY.md`](docs/GLOSSARY.md) — the canonical terms and naming rules for all
  new work

## Product (this repo)

Worship multimedia for GKPS Klender — Bible, Songs, Tata Ibadah (service order), Bookmarks, and
live OBS projection sources. Python 3.12 + Django 4.0 + Django REST Framework; PostgreSQL;
WhiteNoise; deployed on Vercel (`@vercel/python`). The frontend is server-rendered templates with
vanilla JS, jQuery, RxJS, and Fomantic UI. See [`docs/PRODUCT.md`](docs/PRODUCT.md) and
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).
