# Product

Filled for this repository the way a spawned project fills it at kickoff, adapted for an existing
product. Product facts below are **as-built** from the codebase; anything unconfirmed is marked.

## Problem

GKPS Klender needs to present worship content — Bible passages, songs/hymns, and the order of
service (Tata Ibadah) — on screen and in a live streaming/projection (OBS) setup, and to curate that
content without touching the database by hand.

## Who

- Volunteers/operators running live worship projection.
- Admins curating Bible versions, songs, service orders, and bookmark setlists.
- The congregation viewing projected content.

## What it is

A Django web application with three surfaces:

- **REST API** (`/api/`): Bible, Songs, Tatib, Bookmarks, and search.
- **Web management UI** (`/`): server-rendered admin/management screens.
- **OBS projection sources** (`/obs/`): browser source pages for Bible, Songs, Tatib, and Project.

## Locked decisions

- **Process:** vexbook at `v0.4.0` — SDD, TDD, ITEM board, SemVer (ADR 0001).
- **Stack:** Python / Django / Django REST Framework / PostgreSQL, deployed on Vercel.
- **Versioning:** SemVer; `VERSION` + `CHANGELOG.md` + annotated tag `vX.Y.Z`.
- **Git:** Git Flow — `main` (production) / `develop` (integration); features **squash-merge** into
  `develop`, releases/hotfixes **merge-commit** into `main`, remote branch deleted after merge
  (local kept) ([ADR 0002](adr/0002-git-flow-merge-strategy.md)).

## Non-goals

- Not a public multi-tenant SaaS; it serves one congregation's content.
- Not a runtime dependency on vexbook.

## Parked

- Backfilling as-built behavior into numbered specs (owner-accepted slice).
- Converting `CHANGELOG.md` to the Keep a Changelog shape PROCESS expects.
- Choosing the E2E tool for this stack.
- CI for tests.
