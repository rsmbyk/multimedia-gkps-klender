# Plan 016: SDD adoption notes

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `DOCS-SDD` from `specs/docs/sdd-adoption/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/docs/sdd-adoption/{spec,plan,tasks}.md` into `specs/016-docs-sdd-adoption/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/docs/sdd-adoption/plan.md`)</summary>

# Plan: DOCS-SDD — Spec-Driven Development adoption

Spec: [`spec.md`](spec.md) (`DOCS-SDD`)

## Approach

Add process docs and scaffolding only. Mirror the existing pattern used for TDD
and Git Flow: detailed markdown in `docs/`, thin always-applied Cursor rule,
pointer in `AGENTS.md`, Unreleased changelog bullet. Spec IDs were added in the
later backfill pass.

## Touch points

| Area | Files / modules (expected) |
|------|----------------------------|
| Docs | `docs/SDD.md`, `AGENTS.md`, `CHANGELOG.md` |
| Agent rules | `.cursor/rules/sdd.mdc` |
| Specs tree | `specs/README.md`, `specs/constitution.md`, `specs/_templates/*`, this example |

## Contracts

- No API / UI / OBS message changes.
- Spec format: Markdown files named `spec.md`, `plan.md`, `tasks.md` with Spec IDs.

## Risks and rollout

- Risks: Agents might over-apply SDD to tiny chores — mitigated by “when to use”
  table in `docs/SDD.md`.
- Migrations / backfill: product feature specs landed separately under `APP`
  registry.
- Rollout: merge via chore PR into `develop`; use on the next product feature.

## Non-goals

- No Spec Kit / OpenSpec install.


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `DOCS-SDD` — intended; follow-up may update them.
