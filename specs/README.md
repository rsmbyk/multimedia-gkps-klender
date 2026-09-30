# Specs

Living behavior contracts. Layout and gates: [`docs/PROCESS.md`](../docs/PROCESS.md).

## Rules

1. Spec **before** implementation. Plan (manual notes or any AI agent plan mode) **stops at Drafts**.
2. Use [`_template/`](./_template/) — `{plan,spec,tasks}.md` in every Draft.
3. Number specs `000`, `001`, … consecutively. Folder: `NNN-slug/`.
4. **Spec 000** is the product baseline (migrated from legacy `APP`).
5. Keep acceptance in Given / When / Then (migrated as-built bodies preserve
   legacy EARS verbatim for traceability).
6. Link tests under Traceability; tasks name those paths for TDD.
7. Update the spec in the same PR as behavior changes.
8. **One concern per spec.** CSS and copy still get a numbered spec.
9. Every spec comes from one or more `ITEM-XXX` on [`backlog/board.md`](../backlog/board.md).

Legacy `CODE` → `NNN` mapping lives in
[`docs/adr/0001-adopt-vexbook-process.md`](../docs/adr/0001-adopt-vexbook-process.md).
Legacy `CODE` refs remain readable inside migrated spec bodies.

## Index

| Spec | Title | Status |
| --- | --- | --- |
| [000](000-multimedia-baseline/spec.md) | Multimedia GKPS Klender baseline | Accepted |
| [001](001-api-open-access/spec.md) | Open product API and web access | Accepted |
| [002](002-api-songs-content/spec.md) | Songs REST content | Accepted |
| [003](003-api-bible-content/spec.md) | Bible REST content | Accepted |
| [004](004-api-tatib-content/spec.md) | Tatib REST content | Accepted |
| [005](005-api-song-search/spec.md) | Song lyric search | Accepted |
| [006](006-songs-bookmarks/spec.md) | Song bookmarks and setlists | Accepted |
| [007](007-obs-songs-live/spec.md) | OBS Songs dock and source | Accepted |
| [008](008-obs-bible-live/spec.md) | OBS Bible dock and source | Accepted |
| [009](009-obs-tatib-live/spec.md) | OBS Tatib dock and source | Accepted |
| [010](010-obs-project-projection/spec.md) | Combined OBS projection | Accepted |
| [011](011-web-songs-admin/spec.md) | Web songs content admin | Accepted |
| [012](012-web-tatib-admin/spec.md) | Web tatib content admin | Accepted |
| [013](013-web-django-admin/spec.md) | Django staff admin | Accepted |
| [014](014-deploy-vercel/spec.md) | Vercel production | Accepted |
| [015](015-deploy-local/spec.md) | Local Compose runtime | Accepted |
| [016](016-docs-sdd-adoption/spec.md) | SDD adoption notes | Accepted |
| [017](017-test-coverage/spec.md) | Current test coverage | Accepted |
