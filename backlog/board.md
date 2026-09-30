# Backlog board

In-repo Kanban. Each card is an `ITEM-XXX`. Details live in [`items/`](./items/).

**Backlog column only:** sort by Priority (P0 first, then P1, P2, P3; ties by ID). Other columns stay in workflow order.

See [`README.md`](./README.md) for column meanings and owner phrases.

Migrated from legacy `BL-001`–`BL-010` (see `docs/adr/0001-adopt-vexbook-process.md`).
Legacy `BL-*` IDs are preserved inside item files.

## Backlog

| ID | Title | Summary | Type | Priority | Effort | Spec | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [ITEM-006](./items/ITEM-006-vitest-obs-display-end-markers.md) | Vitest for OBS display navigation and end-marker paths | Isolatable display/end-marker tests | test | P2 | M | [007](../specs/007-obs-songs-live/spec.md) | 2026-09-30 |
| [ITEM-009](./items/ITEM-009-revisit-open-api-access.md) | Harden or revisit open product API access | Auth policy decision | idea | P2 | L | [001](../specs/001-api-open-access/spec.md) | 2026-09-30 |
| [ITEM-010](./items/ITEM-010-bible-api-write-path-tests.md) | Expand bible API write-path test coverage | Pytest write paths | test | P2 | S | [003](../specs/003-api-bible-content/spec.md) | 2026-09-30 |
| [ITEM-007](./items/ITEM-007-bible-web-content-admin.md) | Bible web content-admin UI | Web UI or keep admin-only | feat | P3 | L | [008](../specs/008-obs-bible-live/spec.md) | 2026-09-30 |
| [ITEM-008](./items/ITEM-008-bookmarks-web-content-admin.md) | Bookmarks web content-admin UI | Setlist web UI or keep OBS-only | feat | P3 | L | [006](../specs/006-songs-bookmarks/spec.md) | 2026-09-30 |

## Speccing

| ID | Title | Summary | Type | Priority | Effort | Spec | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Ready

| ID | Title | Summary | Type | Priority | Effort | Spec | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [ITEM-003](./items/ITEM-003-web-tatib-month-year-filters.md) | Wire web tatib calendar to month/year API filters | Calendar drives month/year | feat | P1 | S | [012](../specs/012-web-tatib-admin/spec.md) | 2026-09-30 |
| [ITEM-004](./items/ITEM-004-ci-pytest-npm-test.md) | CI for pytest and npm test | PR checks with Postgres | chore | P1 | M | [017](../specs/017-test-coverage/spec.md) | 2026-09-30 |
| [ITEM-005](./items/ITEM-005-vitest-project-hotkeys-mute.md) | Vitest for project hotkeys 1/2/3 and mutual mute | Project control coverage | test | P2 | S | [010](../specs/010-obs-project-projection/spec.md) | 2026-09-30 |

## In progress

| ID | Title | Summary | Type | Priority | Effort | Spec | Branch | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## In review

| ID | Title | Summary | Type | Priority | Effort | Spec | PR | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [ITEM-000](./items/ITEM-000-adopt-vexbook.md) | Adopt vexbook process at v0.4.0 with full migration | Process file set + NNN/ITEM/VERSION | chore | P0 | M | [000](../specs/000-multimedia-baseline/spec.md) | — | 2026-09-30 |

## Done

| ID | Title | Summary | Type | Priority | Effort | Spec | Merged | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [ITEM-001](./items/ITEM-001-shared-obs-semver-footer.md) | Shared OBS SemVer footer and version constant | One version constant + footer | feat | P0 | M | [007](../specs/007-obs-songs-live/spec.md) | release/0.5.0 | 2026-09-30 |
| [ITEM-002](./items/ITEM-002-cut-release-0-5-0.md) | Cut first SemVer release 0.5.0 | Tag v0.5.0 on main | chore | P0 | M | [000](../specs/000-multimedia-baseline/spec.md) | release/0.5.0 | 2026-09-30 |
