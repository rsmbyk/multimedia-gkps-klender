# ADR 0006: Follow the Vex process grammar

## Status

Accepted

## Context

The process was adopted on 2026-09-30 from vexbook v0.4.0 and re-declared on 2026-10-24 as a short
statement of what the repository uses ([ADR 0001](0001-project-process.md)). In both shapes the
rules lived as prose inside this repository, so a change to the process meant editing every copy —
and a copy that stopped moving looked exactly like a deliberate convention.

The grammar has moved since: SDD's eleven stages and two owner gates, the board's tracker anchor — widened
on 2026-10-25 so every card past `Speccing` carries one, backfilled by the agent rather than hung on the
`Ready` transition — the capability tree under `docs/spec/`, one commit per slice at Fold.

## Decision

- This repository follows the **Vex process grammar at vintage 2026-10-25**, kept once in shared
  memory. The repository holds no second copy of the rules.
- [`docs/PROCESS.md`](../PROCESS.md) is **generated** from the grammar's rule notes: every rule of a
  selected part, verbatim in ID order with its operative detail, plus the contracts between the
  selected parts and the original model's rules each of them adapts.
- This repository's own conventions and deviations live in `repo:` blocks inside that file. They are
  never regenerated, and they win over the grammar wherever they speak.
- The parts in use are unchanged: SDD, TDD, Git Flow, SemVer, an in-repo Kanban, and the GitHub
  Issues anchor declared in [ADR 0005](0005-github-issues-anchor.md).
- Precedence is **repo conventions → Vex version → original**. Silence falls back to the grammar.

## Consequences

- Changing a rule is a change to the grammar followed by a regeneration of `docs/PROCESS.md`, never
  a local edit inside a generated table.
- [`AGENTS.md`](../../AGENTS.md) says what the repository uses and points at the process file. It
  carries no rules and no rule IDs, so there is no second truth to drift.
- A repo convention is added by editing its `repo:` block, not by appending prose.
- When the grammar's vintage advances, `docs/PROCESS.md` is regenerated and the diff shows which
  rules moved.
