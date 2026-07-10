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
