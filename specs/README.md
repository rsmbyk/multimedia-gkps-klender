# Specs

Living behavior contracts. Layout and gates: [`docs/PROCESS.md`](../docs/PROCESS.md).

## Rules

1. Spec **before** implementation. Plan (manual notes or any AI agent plan mode) **stops at Drafts**.
2. Use [`_template/`](./_template/) — `{plan,spec,tasks}.md` in every Draft.
3. Number specs `000`, `001`, … consecutively. Folder: `NNN-slug/`.
4. **Spec 000** is reserved for scaffolding and is **one spec**.
5. Keep acceptance in Given / When / Then.
6. Link tests under Traceability; tasks name those paths for TDD.
7. Update the spec in the same PR as behavior changes.
8. **One concern per spec.** CSS and copy still get a numbered spec.
9. Every spec comes from one or more `ITEM-XXX` on [`backlog/board.md`](../backlog/board.md).

## Index

| Spec | Title | Status |
| --- | --- | --- |
| [001](001-public-songs-reading/spec.md) | Public song reading + design foundation | Accepted |
| [002](002-local-docker-compose/spec.md) | Local Docker Compose stack | Accepted |
| [003](003-maintenance-page/spec.md) | Maintenance page at the site root | Accepted |
| [004](004-public-site-revamp/spec.md) | Public site revamp | Accepted |
| [005](005-sidebar-editors/spec.md) | Sidebar editors for Kidung and Tata Ibadah | Accepted |
| [006](006-service-entries/spec.md) | Service entries — one Tata Ibadah holds texts, scriptures and songs | Accepted |
| [007](007-service-order-editor/spec.md) | The old rows — editable, and one running order | Accepted |
| [008](008-sidebar-selection-tint/spec.md) | Softer selected-item tint in the reading sidebars | Accepted |

`000` is reserved for the project scaffold baseline. As an adopter, this repo has no scaffold
spec yet — the as-built baseline backfill is a separate, owner-accepted slice.
