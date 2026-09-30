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

`000` is reserved for the project scaffold baseline. As an adopter, this repo has no scaffold
spec yet — the as-built baseline backfill is a separate, owner-accepted slice.
