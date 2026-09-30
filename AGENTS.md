# Agent guide

Project conventions for humans and coding agents. Prefer these docs over
guessing.

This repo adopts the **vexbook** process at **`v0.4.0`** (see
`docs/adr/0001-adopt-vexbook-process.md`). `docs/PROCESS.md`,
`docs/KICKOFF.md`, `docs/ADOPT.md`, and `docs/rules/SDD-GATE.md` are binding.
Product docs below remain authoritative for stack and domain detail.

## Process (vexbook, binding)

- **Way of working:** [`docs/PROCESS.md`](docs/PROCESS.md)
- **Must-apply gate:** [`docs/rules/SDD-GATE.md`](docs/rules/SDD-GATE.md) — plan
  stops at Draft specs; do not implement until the owner Accepts the Draft.
- **Existing repo / sync:** [`docs/ADOPT.md`](docs/ADOPT.md) (owner-triggered;
  no auto-sync). Greenfield spawn path is [`docs/KICKOFF.md`](docs/KICKOFF.md)
  (kept for reference; this repo is an adopter, not a spawn).
- **Specs:** `specs/NNN-slug/{plan,spec,tasks}.md` from `specs/_template/`;
  consecutive integers, spec `000` is the product baseline. One concern per spec.
- **Board:** [`backlog/board.md`](backlog/board.md) (`ITEM-*` under
  `backlog/items/`). Backlog column sorted P0–P3. Board, tasks, and version
  (when `bump` is not `none`) land in the same PR.
- **Versioning:** SemVer locked. `VERSION` (root, no `v`) + `CHANGELOG.md` +
  tag `vX.Y.Z` on `main`. `ITEM`/`spec` carry `bump: major|minor|patch|none`.
  `multimedia/obs/static/obs/common/version.js` (`APP_VERSION`) mirrors
  `VERSION`; record in release checklist.
- **Git:** Git Flow — `main` (production/Vercel), `develop` (integration).
  Features from `develop` (`feat/*`, `fix/*`, `chore/*`, `docs/*`); default PR
  target `develop`; release/hotfix via merge commits per
  [`docs/GIT_FLOW.md`](docs/GIT_FLOW.md).
- **Commits:** Conventional Commits; agent commits end with a `Co-authored-by`
  trailer for the vendor product that authored the commit.

## Product (this repo)

- **What:** worship content + live OBS projection for GKPS Klender
  (`specs/000-multimedia-baseline/` + index in [`specs/README.md`](specs/README.md)).
- **Branching and releases:** Git Flow — [`docs/GIT_FLOW.md`](docs/GIT_FLOW.md);
  single SemVer + changelog area labels — [`docs/VERSIONING.md`](docs/VERSIONING.md);
  history — [`CHANGELOG.md`](CHANGELOG.md); production — [`docs/DEPLOY.md`](docs/DEPLOY.md).
- **Testing (TDD):** [`docs/TDD.md`](docs/TDD.md); Python `pytest` /
  `requirements-dev.txt` / `pytest.ini`; JavaScript Vitest / `package.json` /
  `vitest.config.js`. Behavior changes: failing test first.
- **Specs (SDD):** vexbook `NNN` layout going forward (migrated from legacy
  `CODE` IDs; mapping in ADR 0001). Legacy `CODE` refs (`OBS-SONGS-AC3`, …)
  remain readable in migrated spec bodies for traceability.
- **Backlog:** [`backlog/board.md`](backlog/board.md) (`ITEM-*`); migrated from
  legacy `BL-*` (mapping in ADR 0001). Field guide in [`backlog/README.md`](backlog/README.md).

## Cursor rules

Agent-oriented summaries live under [`.cursor/rules/`](.cursor/rules/). They
point at the docs above; the markdown in `docs/` is the source of truth.
Vendor rules must reference every must-apply shared doc from `docs/PROCESS.md`.
