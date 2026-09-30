# ADR 0001: Adopt vexbook process at v0.4.0

## Status

Accepted

## Context

`multimedia-gkps-klender` had a docs-native Git Flow + SDD + TDD + single-SemVer
workflow (`docs/GIT_FLOW.md`, `docs/SDD.md`, `docs/TDD.md`, `docs/VERSIONING.md`,
`docs/BACKLOG.md`, `docs/DEPLOY.md`) with legacy identifiers:

- Specs: `CODE` IDs (`APP`, `API-SONGS`, `OBS-SONGS`, …) in
  `specs/<area>/<feature>/` + `specs/_templates/` (plural), registry in
  `specs/README.md`.
- Backlog: `BL-*` in `backlog/items/BL-NNN-slug.md`, board in `backlog/README.md`,
  template in `backlog/_templates/item.md`.
- Version: no root `VERSION`; SemVer finalized on `release/*` in `CHANGELOG.md`
  (`## Version x.y.z`) + `APP_VERSION` in
  `multimedia/obs/static/obs/common/version.js`.

Owner asked to adopt vexbook (local `~/Projects/vexbook`, source `v0.4.0`) with
full migration of specs, backlog, and version identity.

## Decision

Adopt vexbook process at `v0.4.0`.

- Binding: [`../PROCESS.md`](../PROCESS.md), [`../KICKOFF.md`](../KICKOFF.md)
  (reference only; this repo is an adopter), [`../ADOPT.md`](../ADOPT.md), and
  [`../rules/SDD-GATE.md`](../rules/SDD-GATE.md).
- Git model: Git Flow (already in use; recorded here per PROCESS).
- Specs: vexbook `NNN` layout going forward (`specs/_template/`, consecutive
  integers, `000` = product baseline). Legacy `CODE` specs migrated to
  `000`–`017` with legacy IDs preserved in-body for traceability.
- Backlog: vexbook `ITEM-*` + `backlog/board.md` going forward. Legacy `BL-001`
  –`BL-010` migrated to `ITEM-001`–`ITEM-010` (numbers preserved); `ITEM-000`
  records this adoption. Legacy `BL-*` IDs preserved in-body.
- Version: create root `VERSION` = `0.5.1` (current shipped version). `VERSION`
  is canonical; `version.js` `APP_VERSION` is a mirror. New changelog sections
  use Keep a Changelog shape (`## [X.Y.Z] - YYYY-MM-DD`); old `## Version …`
  sections stay as history.
- Do not renumber existing ADRs (none existed; this is `0001`). Do not force
  spawn-style `0001` (process) / `0002` (product). Do not copy vexbook
  `templates/`, backlog/specs history, `VERSION`, or `CHANGELOG` history.

### Spec mapping (legacy CODE → NNN)

| NNN | Slug | Legacy |
|-----|------|--------|
| 000 | multimedia-baseline | `APP` (`specs/app/`) |
| 001 | api-open-access | `API-ACCESS` (`specs/api/open-access-policy/`) |
| 002 | api-songs-content | `API-SONGS` (`specs/api/songs-content/`) |
| 003 | api-bible-content | `API-BIBLE` (`specs/api/bible-content/`) |
| 004 | api-tatib-content | `API-TATIB` (`specs/api/tatib-content/`) |
| 005 | api-song-search | `API-SEARCH` (`specs/api/song-search/`) |
| 006 | songs-bookmarks | `SONGS-BM` (`specs/songs/song-bookmarks/`) |
| 007 | obs-songs-live | `OBS-SONGS` (`specs/songs/obs-songs-live/`) |
| 008 | obs-bible-live | `OBS-BIBLE` (`specs/bible/obs-bible-live/`) |
| 009 | obs-tatib-live | `OBS-TATIB` (`specs/tatib/obs-tatib-live/`) |
| 010 | obs-project-projection | `OBS-PROJECT` (`specs/project/obs-project-projection/`) |
| 011 | web-songs-admin | `WEB-SONGS` (`specs/web/songs-content-admin/`) |
| 012 | web-tatib-admin | `WEB-TATIB` (`specs/web/tatib-content-admin/`) |
| 013 | web-django-admin | `WEB-ADMIN` (`specs/web/django-staff-admin/`) |
| 014 | deploy-vercel | `DEPLOY-VERCEL` (`specs/deploy/vercel-production/`) |
| 015 | deploy-local | `DEPLOY-LOCAL` (`specs/deploy/local-compose-runtime/`) |
| 016 | docs-sdd-adoption | `DOCS-SDD` (`specs/docs/sdd-adoption/`) |
| 017 | test-coverage | `TEST-COV` (`specs/test/current-coverage/`) |

### Backlog mapping (legacy BL → ITEM)

| ITEM | Legacy | Status mapping |
|------|--------|----------------|
| ITEM-000 | — (this adoption) | in-review → done on merge |
| ITEM-001 | BL-001 | done → done |
| ITEM-002 | BL-002 | done → done |
| ITEM-003 | BL-003 | ready → ready |
| ITEM-004 | BL-004 | ready → ready |
| ITEM-005 | BL-005 | ready → ready |
| ITEM-006 | BL-006 | idea → backlog |
| ITEM-007 | BL-007 | idea → backlog |
| ITEM-008 | BL-008 | idea → backlog |
| ITEM-009 | BL-009 | idea → backlog |
| ITEM-010 | BL-010 | idea → backlog |

Target status vocabulary maps: `idea`→`backlog`, `specified`→`speccing`,
others map 1:1 (`ready`, `in-progress`, `in-review`, `done`).

## Consequences

- `docs/PROCESS.md`, `docs/KICKOFF.md`, `docs/ADOPT.md`,
  `docs/rules/SDD-GATE.md` are binding; SDD loop is Draft → Accept → implement;
  plan work stops at Drafts.
- New behavior/CSS/copy changes use `ITEM-XXX` → `specs/NNN-slug/` with `bump`;
  board, tasks, and version (when applicable) land in the same PR.
- Old paths removed after migration: `specs/<area>/`, `specs/_templates/`,
  `specs/constitution.md` (superseded; product constraints live in ADRs +
  `docs/`), `backlog/items/BL-*.md`, `backlog/_templates/`.
  `specs/README.md`, `backlog/README.md`, `backlog/board.md` follow vexbook
  shapes. `docs/BACKLOG.md`, `docs/SDD.md` remain as product notes but PROCESS
  wins on conflict; follow-up cleanup may retire them.
- Vendor rules (`.cursor/rules/`) reference every must-apply shared doc from
  PROCESS.
- First behavior change after adopt still goes through SDD.
