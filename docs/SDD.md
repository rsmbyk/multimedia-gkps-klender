# Spec-Driven Development (SDD)

This project uses **lightweight, docs-native Spec-Driven Development**. Structured
specs in the repo are the source of truth for *intent*; code and tests are
derived from them. Specs are **spec-anchored** (kept alive and updated when
behavior changes) — not a “regenerate the whole codebase from specs” toolchain.

SDD sits **above** TDD. The spec says *what* and *why*; TDD still proves each
slice of work (red → green → refactor). See [`TDD.md`](TDD.md).

No Spec Kit / OpenSpec CLI is required. Agents and humans read Markdown under
`specs/` and follow the phases below (Cursor Plan Mode is a good fit for Plan).

## When to use SDD

| Situation | Expectation |
|-----------|-------------|
| New product behavior | Full loop: Specify → Plan → Tasks → Implement |
| Non-trivial bug fix or cross-cutting change | Full loop (or a short spec if the bug is well-bounded) |
| Docs-only / pure tooling with no behavior change | Skip specs |
| Tiny one-file fix with obvious intent | Optional mini-spec in the PR; full `specs/` tree not required |

When in doubt, write a short `spec.md`. Ambiguity is more expensive than a page
of Markdown.

## Phases

Human review at each phase boundary before moving on (same spirit as “discuss
approach first”).

### 1. Specify

Capture intent in `specs/<area>/<feature>/spec.md` (or update an existing spec).

Include:

- **Problem / goal** — why this exists
- **User stories** — As a … I want … so that …
- **Acceptance criteria** — prefer [EARS](#ears-notation) statements
- **Out of scope** — what we will *not* do
- **Constraints** — links to constitution and existing docs (TDD, deploy, etc.)

Do not start implementation until the spec is agreed.

### 2. Plan

Translate the spec into `plan.md` beside it:

- Approach and main touch points in the codebase
- Data / API / UI contracts if relevant
- Risks, migrations, and rollout notes
- Explicit “non-goals” carried from the spec

Stay inside project constraints ([`constitution.md`](../specs/constitution.md),
Git Flow, deploy runbook). Prefer stdlib and existing patterns; ask before large
or uncommon dependencies.

### 3. Tasks

Break the plan into `tasks.md`: a checklist of atomic, shippable units. Each
task should have:

- One clear objective
- Likely files / areas to touch
- A **verification** step (tests to add/run, manual check, or both)

Tasks should be small enough that an agent (or junior engineer) can finish one
without inventing new product scope.

### 4. Implement

Work tasks in order. For each task that changes product behavior:

1. Follow **TDD** ([`TDD.md`](TDD.md)): failing test → implementation → refactor
2. Confirm the task’s verification step
3. Check the result against the spec’s acceptance criteria

If reality diverges from the spec, **update the spec first** (or clarify with a
human), then change the code. Do not silently let the code become the only truth.

## Repository layout

```text
specs/
  README.md                 # index, ID conventions, feature registry
  constitution.md           # project-wide guardrails (points at docs/)
  app/                      # APP — full product overview
  _templates/               # copy these for new work
    spec.md
    plan.md
    tasks.md
  <area>/<feature>/         # one folder per change or capability
    spec.md
    plan.md
    tasks.md
```

`<area>` should match changelog-style labels when possible (`songs`, `bible`,
`api`, `web`, `deploy`, `docs`, …). See [`VERSIONING.md`](VERSIONING.md).

Branch naming still follows [`GIT_FLOW.md`](GIT_FLOW.md)
(`feature/*`, `fix/*`, `chore/*`). Specs for a topic live on that branch and
merge with the PR.

## Spec IDs

Every spec folder has a stable **Spec ID** (short code). Use it in titles,
cross-references, PR notes, and chat (“see `OBS-SONGS-AC3`”).

| Kind | Pattern | Example |
|------|---------|---------|
| Spec | `<CODE>` | `OBS-SONGS`, `API-SONGS`, `APP` |
| User story | `<CODE>-US<n>` | `OBS-SONGS-US1` |
| Acceptance criterion | `<CODE>-AC<n>` | `OBS-SONGS-AC3` |
| Task | `<CODE>-T<n>` | `OBS-SONGS-T2` |

Rules:

- Codes are **stable** once published. Renaming a folder does not change the
  code unless the registry is updated deliberately.
- Numbers are **local to that spec** (restart at 1 in each file).
- OBS live surfaces use **`OBS-` first**, then the domain (`OBS-SONGS`,
  `OBS-BIBLE`, `OBS-TATIB`, `OBS-PROJECT`).
- Cross-ref in Markdown as plain codes (`API-SONGS-AC2`) and/or links to the
  feature `spec.md`.
- The living registry of codes lives in [`specs/README.md`](../specs/README.md)
  and [`specs/app/spec.md`](../specs/app/spec.md).

When writing acceptance criteria, prefix each bullet with its ID:

```markdown
- **API-SONGS-AC1:** WHEN an unauthenticated client lists books THE system
  SHALL return HTTP 200.
```

## EARS notation

Prefer short, testable acceptance criteria. [EARS](https://en.wikipedia.org/wiki/EARS_(software_requirements))
patterns that work well here:

| Pattern | Form |
|---------|------|
| Ubiquitous | THE system SHALL … |
| Event-driven | WHEN … THE system SHALL … |
| State-driven | WHILE … THE system SHALL … |
| Unwanted | IF … THEN THE system SHALL … |
| Optional | WHERE … THE system SHALL … |

Example: `WHEN a user selects a songbook THE songs dock SHALL load that book's
song list without remaining on a permanent loading state.`

## Relationship to other conventions

| Doc | Role vs SDD |
|-----|-------------|
| [`TDD.md`](TDD.md) | How each implementation task is proven |
| [`GIT_FLOW.md`](GIT_FLOW.md) | Where work branches and merges |
| [`VERSIONING.md`](VERSIONING.md) | Changelog labels; no SemVer bump on develop PRs |
| [`DEPLOY.md`](DEPLOY.md) | Production constraints for deploy-related specs |
| [`BACKLOG.md`](BACKLOG.md) | What we might do next (`BL-*`); specs take over once in scope |

## Agent expectations

See [`.cursor/rules/sdd.mdc`](../.cursor/rules/sdd.mdc). For in-scope product
work, agents should produce or update specs before coding, wait for human OK at
phase boundaries when the session expects it, and keep specs in sync when
behavior changes.
