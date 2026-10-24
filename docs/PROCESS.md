# Process

This repository follows the Vex process grammar at vintage **2026-10-24**.

**Precedence:** repo conventions → Vex version → original.

The rule tables below are generated from the grammar's rule index — every rule of a selected part,
verbatim and in ID order. A `repo:` block holds this repository's own conventions and deviations
for that part, and is never regenerated.

## Parts in use

| Part | Choice |
| --- | --- |
| Specification | `sdd` — Spec Kit's loop: eleven stages, two owner gates |
| Tests | `tdd` — classicist |
| Git | `git-flow` |
| Versioning | `semver` — `VERSION` is the authority |
| Board | `kanban` — in-repo, six columns |
| Tracker mirror | GitHub Issues as an anchor — `Refs`, never `Closes` |

## Specification — sdd

| ID | Rule |
| --- | --- |
| SDD-01 | The constitution is optional, lives at `CONSTITUTION.md`, and is never auto-created. |
| SDD-02 | One slice is one folder, `specs/NNN-slug/`, with `NNN` the next free number. |
| SDD-03 | Specify reads `docs/spec/<capability>.md` before writing; an existing requirement is *modified*, never duplicated. |
| SDD-04 | Specify never asks: it leaves `[NEEDS CLARIFICATION: <question>]` markers for Clarify. |
| SDD-05 | `spec.md` carries prioritised user stories, each with *why this priority*, an *independent test* and Given/When/Then scenarios, then `FR-###`, `SC-###` and Assumptions. |
| SDD-06 | Preview runs before gate 1, built from the project's own components; a mockup is the fallback, labelled and materials-faithful; `## UI/UX` holds numbers, not adjectives. |
| SDD-07 | Clarify asks through the agent's question tool, one question at a time, recommendation first, no budget. |
| SDD-08 | Clarify closes only at zero open items; a skipped question becomes a recorded assumption, never a deferral. |
| SDD-09 | **Gate 1**: the owner Accepts the spec pack; nothing proceeds without it. |
| SDD-10 | Plan fills Technical Context and runs the Constitution Check before Phase 0 and again after Phase 1. |
| SDD-11 | Plan Phase 0 writes `research.md` as Decision / Rationale / Alternatives / Provenance, and exits only at zero unknowns. |
| SDD-12 | Plan Phase 1 writes `data-model.md`, `contracts/` (or an explicit `none`) and `quickstart.md`. |
| SDD-13 | `plan.md` carries the traceability table: every `FR-###`, `SC-###` and story scenario, with its component and `Verified by` = `test` · `inspection` · `manual`. |
| SDD-14 | Plan's exit gate is seven checks; no code is written and `tasks.md` is not created here. |
| SDD-15 | Checklist items are reviewer-owned; the agent generates and never ticks; files are appended, never replaced. |
| SDD-16 | Tasks are ordered by user story — Setup, Foundational, one phase per story, Polish — as `- [ ] T### [P] [USn] description with path`. |
| SDD-17 | Analyze writes `analysis.md`; gate 2 opens only at zero CRITICAL and 100% coverage; HIGH and below are reported, never fixed silently. |
| SDD-18 | **Gate 2**: present spec, plan, traceability with the verification split, every checklist unticked, tasks and analysis; every item must be ticked, and an unticked item is a change request. |
| SDD-19 | After gate 2 the run is continuous — Implement → Converge → Fold — stopping only to report or at Converge's cap. |
| SDD-20 | Implement runs phase by phase, halts on a failing sequential task, and marks tasks `[X]` as they land. |
| SDD-21 | Converge compares code against the traceability table, types each gap `missing` · `partial` · `contradicts` · `unrequested`, appends `## Phase N: Convergence`, and stops at three passes to ask. |
| SDD-22 | Completion claims are never evidence: every task is re-assessed whatever its checkbox says. |
| SDD-23 | Fold runs only at Converged, writes the typed delta into `docs/spec/<capability>.md`, is idempotent, and treats an undeclared behaviour change as CRITICAL. |
| SDD-24 | Done means Converged, Folded and reported — never "the boxes are ticked". |
| SDD-25 | A revision re-enters at the earliest stage it touches; anything before gate 1 invalidates the plan rather than patching it. |
| SDD-26 | A change too large for one spec is split by user story, by capability or by risk — never by layer. |
| SDD-27 | The closing report shows what shipped, the verification split, convergence with any accepted gaps, the capabilities folded, the branch and commit count, the version and changelog line, the PR title and body, that nothing is pushed — and then asks about pushing. |

<!-- repo:begin part=sdd -->
- **Docs-only changes** may skip the numbered spec with a short plan and owner approval.
<!-- repo:end -->

## Tests — tdd

| ID | Rule |
| --- | --- |
| TDD-01 | A failing test comes before the code for every row declared `test`. |
| TDD-02 | The test must fail for the right reason; read the assertion before making it pass. |
| TDD-03 | Classicist: real collaborators; doubles only at process boundaries — network, clock, filesystem, randomness. |
| TDD-04 | Never mock what you do not own. |
| TDD-05 | A unit is a behaviour, not a function. |
| TDD-06 | One behaviour per test, named `test_<behaviour>_<condition>`. |
| TDD-07 | A test is deleted only when the behaviour is gone or the test was wrong — never to make a change pass. |
| TDD-08 | Coverage is a diagnostic, never a gate; mutation score is the optional quality signal. |
| TDD-09 | A red test blocks; it is never skipped or quarantined silently. |

<!-- repo:begin part=tdd -->
- **Scope:** TDD governs domain and application rules. User-visible acceptance is Playwright
  (Python) E2E, run through Django's `LiveServerTestCase`.
- **Location:** a Django app's tests sit beside it (`<app>/tests.py`); cross-cutting and E2E tests
  live in `tests/`. The runner is Django's; coverage is measured with `coverage`.
<!-- repo:end -->

## Git — git-flow

| ID | Rule |
| --- | --- |
| GIT-01 | Never edit, stage or commit in a checkout of `develop` or `main`. |
| GIT-02 | A slice works in its own worktree on its own branch: `git worktree add ../<repo>-NNN -b feat/NNN-slug develop`. |
| GIT-03 | One slice, one branch, one PR; the branch carries the spec's `NNN`. |
| GIT-04 | Squash into `develop`; the squash message is the PR title plus its description. |
| GIT-05 | Merge into `main` with a merge commit — every model, never squash, never fast-forward. |
| GIT-06 | Commits start at Fold: none before it, and every commit carries a green suite. |
| GIT-07 | Push only on the owner's word — the first push and every update to an open PR. |
| GIT-08 | Never delete a local branch or worktree; remote branches follow the repo's settings. |
| GIT-09 | `release/X.Y.Z` is cut from `develop` when the slice set is complete and carries only the bump confirmation, the changelog and fixes. |
| GIT-10 | The tag is cut on `main` only, never off `main`, and the back-merge to `develop` is never skipped. |
| GIT-11 | Conventional Commits: `type(scope): subject`, subject ≤72 characters, body for the why. |

<!-- repo:begin part=git -->
- After a merge, delete the **remote** branch only; local branches and worktrees are kept.
- Never force-push `main` or `develop`; never create vendor- or agent-named branches.
- A docs-only change uses a `docs/<slug>` branch: there is no `NNN` to carry.
<!-- repo:end -->

## Versioning — semver

| ID | Rule |
| --- | --- |
| VER-01 | `VERSION` at the repo root is the single authority; tags are derived and checked against it. |
| VER-02 | One scheme per repo; the default is SemVer. |
| VER-03 | `bump` is declared at Plan and shown at gate 2. |
| VER-04 | The bump is applied immediately before the merge, in the delivery commit that also writes the changelog line and closes the card. |
| VER-05 | `bump: none` is a declared value, and it means no `VERSION` change and no changelog entry. |
| VER-06 | A released version is immutable: no retag, no reuse. |
| VER-07 | `CHANGELOG.md` always carries `## [Unreleased]`; a slice appends one line there; the release renames it and adds a fresh one. |
| VER-08 | A released changelog section is never edited. |
| VER-09 | The changelog heading is the version verbatim, `VERSION` without its `v`. |

<!-- repo:begin part=semver -->
- `CHANGELOG.md` carries the current history; everything before the 2026-09-30 adoption is
  preserved as-is in `docs/CHANGELOG-archive.md`.
<!-- repo:end -->

## Board — in-repo kanban

| ID | Rule |
| --- | --- |
| BRD-01 | Ideas land on the board first; a spec is written from one or more cards. |
| BRD-02 | A card is demand — not a spec, not a slice; several cards may share one spec. |
| BRD-03 | The states are Backlog · Speccing · Ready · In progress · In review · Done, with `Archive` as a table, not a column. |
| BRD-04 | Only the owner picks a card into `Speccing` and only the owner promotes it to `Ready`. |
| BRD-05 | `backlog/board.md` and `backlog/items/ITEM-XXX-slug.md` follow their templates verbatim; the evidence column changes with the state. |
| BRD-06 | The board ships in the same PR as the work. |
| BRD-07 | `In review` while the PR is open, `Done` before the merge — and `Done` is terminal. |
| BRD-08 | The `## Archive` table holds only cards that ended without shipping, with a reason and a date. |
| BRD-09 | Board `done` is not the spec's `Status`; board words never enter a spec, spec words never enter `status:`. |
| BRD-10 | When the remote is GitHub, one anchor issue per card is created as it enters `Ready`, its number stored in `issue:`, and PRs say `Refs`, never `Closes`. |
| BRD-11 | Only the owner closes a card; the agent may propose. |

<!-- repo:begin part=board -->
- The anchor label is `board:item`; one issue per card, created when the card enters `Ready`.
<!-- repo:end -->

## Contracts

| ID | Contract |
| --- | --- |
| C-BOARD-GIT | The branch carries the spec's `NNN`; the card records `branch` and `pr`; `Done` is set before the merge. |
| C-BOARD-VER | `release_version:` is filled at release, never at merge. |
| C-GIT-VER | The bump lands on `develop` with the squash; the release branch confirms rather than sets it; the tag matches `main`. |
| C-SDD-BOARD | Card ≠ slice; the loop moves the card; `Ready` is gate 1; an accepted Converge gap becomes a new card. |
| C-SDD-GIT | The run opens the branch at the change request; Fold makes the first commit; the merge follows the report. |
| C-SDD-TDD | `Verified by: test` is the seam: a test row becomes two tasks under TDD, one without; SDD's ordering wins over TDD's. |
| C-SDD-VER | `bump` is declared at Plan, reviewed at gate 2 and applied in the pre-merge commit. |
| C-TDD-GIT | No commit before Fold, and every commit green — no work-in-progress commits. |
| C-TDD-VER | No bump on a red suite; tests-only changes are `bump: none`; a tag comes from the released commit's own green run. |

**Board × TDD has no contract.** The board never gates on tests; Converge does, per
requirement. A second place deciding "is it done" would disagree with the first.
