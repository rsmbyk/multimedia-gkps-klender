# Backlog board

In-repo Kanban. Each card is an `ITEM-XXX`. Details live in [`items/`](./items/).

**Backlog column only:** sort by Priority (P0 first, then P1, P2, P3; ties by ID). Other columns stay in workflow order.

See [`README.md`](./README.md) for column meanings and owner phrases.

## Backlog

| ID | Title | Summary | Type | Priority | Effort | Spec | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [ITEM-002](./items/ITEM-002-projection-controls.md) | Projection source as display + controls | Drive the service from the projection window without switching to the dock | feat | P1 | L | — | 2026-09-30 |

## Speccing

| ID | Title | Summary | Type | Priority | Effort | Spec | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [ITEM-006](./items/ITEM-006-sidebar-editors.md) | Sidebar editors for Kidung and Tata Ibadah | Add/edit modals for songbooks, songs and Tata Ibadah from the reading sidebars; hymn books stay read-only; no login by owner decision | feat | P1 | L | [005](../specs/005-sidebar-editors/spec.md) | 2026-10-03 |

## Ready

| ID | Title | Summary | Type | Priority | Effort | Spec | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- |

## In progress

| ID | Title | Summary | Type | Priority | Effort | Spec | Branch | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## In review

| ID | Title | Summary | Type | Priority | Effort | Spec | PR | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [ITEM-005](./items/ITEM-005-public-site-revamp.md) | Public site revamp | Search-first home, icon rail with nested sidebars, full-corpus search (Bible, Kidung, Tata Ibadah), EN chrome + Indonesian terms, AA palette | chore | P1 | L | [004](../specs/004-public-site-revamp/spec.md) | [#261](https://github.com/rsmbyk/multimedia-gkps-klender/pull/261) | 2026-10-03 |

## Done

| ID | Title | Summary | Type | Priority | Effort | Spec | Merged | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [ITEM-004](./items/ITEM-004-maintenance-page.md) | Maintenance page at the site root | `/` shows a maintenance notice; home moves to a temporary URL behind a switch | feat | P1 | M | [003](../specs/003-maintenance-page/spec.md) | develop | 2026-10-01 |
| [ITEM-003](./items/ITEM-003-local-docker-compose.md) | Local Docker Compose stack on low-conflict ports | `web` + `db` via `docker compose`, published on random high ports | chore | P1 | S | [002](../specs/002-local-docker-compose/spec.md) | develop | 2026-10-01 |
| [ITEM-001](./items/ITEM-001-public-songs-reading.md) | Public song reading + design foundation | Design foundation + public song pages; editor to /manage | feat | P0 | M | [001](../specs/001-public-songs-reading/spec.md) | main | 2026-09-30 |
| [ITEM-000](./items/ITEM-000-adopt-vexbook.md) | Adopt vexbook process at v0.4.0 | Process file set + adoption ADR + board/specs stubs | chore | P0 | M | — | main | 2026-09-30 |
