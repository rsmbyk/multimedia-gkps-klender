# Process

This repository follows the Vex process grammar at vintage **2026-10-25**.

**Precedence:** repo conventions → Vex version → original.

The rule tables below are generated from the grammar — every rule of a selected part,
verbatim and in ID order, each with its operative detail beneath it, and the original
model's rules after it in their published order. A `repo:` block holds this repository's
own conventions and deviations for that part, and is never regenerated.

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
| SDD-01 | The constitution is optional, lives at `CONSTITUTION.md`, and is never auto-created.<br>• Path only: Spec Kit's `.specify/memory/constitution.md` is unavailable because no `.specify/` is installed.<br>• It says **how we build** — principles, quality bars, refusals, review standards — never what the product does. A line whose violation leaves the product working as specified is a principle; if violating it breaks the product, it is a requirement and belongs in the capability tree. |
| SDD-02 | One slice is one folder, `specs/NNN-slug/`, with `NNN` the next free number.<br>• Numbers are never reused, and two spec packs never share one branch. |
| SDD-03 | Specify reads `docs/spec/<capability>.md` before writing; an existing requirement is *modified*, never duplicated.<br>• Three outcomes: an existing requirement is modified and cited as `capability/R<n>`; no capability exists yet, so the slice names the capability it creates; or the request contradicts a requirement, which becomes a marker for Clarify rather than a silent overwrite.<br>• The capability tree is one file per durable behaviour area, `R<n>` stable within its capability, never reused or renumbered, and a removal is marked with its reason and date. |
| SDD-04 | Specify never asks: it leaves `[NEEDS CLARIFICATION: <question>]` markers for Clarify.<br>• The markers are the handoff contract — Clarify starts from them. They are the only thing Specify produces for the interrogation. |
| SDD-05 | `spec.md` carries prioritised user stories, each with *why this priority*, an *independent test* and Given/When/Then scenarios, then `FR-###`, `SC-###` and Assumptions.<br>• Assumptions hold every default taken when the request was silent, so a reader sees exactly what was decided without the owner.<br>• Built-in quality gate: `checklists/requirements.md` is written and the spec validated against it, up to three iterations; a failure that survives is recorded and reported.<br>• The item *"no `[NEEDS CLARIFICATION]` markers remain"* is deliberately not in that checklist — markers are supposed to exist at the end of Specify, so the box would fail every run and teach the reader to ignore the list. |
| SDD-06 | Preview runs before gate 1, built from the project's own components; a mockup is the fallback, labelled and materials-faithful; `## UI/UX` holds numbers, not adjectives.<br>• First choice: rendered by the repo's own stack, served from the project, so a click hits the real code path. An existing screen is that screen with the change; a new screen composes existing primitives; a missing component is a Plan finding, not a hand-rolled `div`.<br>• Fallback: an interactive mockup using the project's real stylesheet or exact values, class names, fonts, assets and tokens; every `## UI/UX` state reachable by hand; named `MOCKUP` with the reason a live preview was not viable, and then ported faithfully rather than reinterpreted.<br>• A screenshot, a static image and a recording are never a preview, at either tier.<br>• Skipped only when the slice touches nothing visible, and then recorded `n/a — <reason>`. When unsure whether a surface is visible, ask. |
| SDD-07 | Clarify asks through the agent's question tool, one question at a time, recommendation first, no budget.<br>• The question tool of whatever agent is running — Hermes `clarify`, Codex's prompt, Cursor's equivalent. Chat prose only where the tool has none.<br>• The ~13-category ambiguity scan runs as a completeness check behind Specify's markers, not as the source of the queue. |
| SDD-08 | Clarify closes only at zero open items; a skipped question becomes a recorded assumption, never a deferral.<br>• Every item ends answered, skipped with its recommendation recorded, or explicitly left ambiguous and recorded as such. Something that can neither be answered nor defaulted blocks the stage.<br>• A new answer is re-checked against the whole spec; a contradiction stops the queue, names the clash, and asks which statement wins — the losing one is kept as superseded, never deleted.<br>• Close-out presents the final spec, every assumption, the skipped questions with an offer to reopen, and the confirmation that zero markers remain. |
| SDD-09 | **Gate 1**: the owner Accepts the spec pack; nothing proceeds without it.<br>• What must be on screen: `spec.md` itself, the running preview with the URL or command that opens it — or the labelled mockup and its reason — the `## UI/UX` values as numbers, every assumption, every skipped question, and the zero-marker confirmation.<br>• Materials first, question last; paths rather than paraphrases; a missing material named with its reason.<br>• Accept is permission to plan, not permission to implement. |
| SDD-10 | Plan fills Technical Context and runs the Constitution Check before Phase 0 and again after Phase 1.<br>• A violation stands only if it is justified in the Complexity Tracking table: *Violation · Why Needed · Simpler Alternative Rejected Because*. |
| SDD-11 | Plan Phase 0 writes `research.md` as Decision / Rationale / Alternatives / Provenance, and exits only at zero unknowns.<br>• Research first: a question is asked only when research genuinely cannot decide. Asked questions go through the question tool, one at a time, recommendation first, and the answer records its provenance — *owner decision; research inconclusive*.<br>• Never a person's name in a repo artifact: roles only. |
| SDD-12 | Plan Phase 1 writes `data-model.md`, `contracts/` (or an explicit `none`) and `quickstart.md`.<br>• `contracts/` states `none` when the project exposes no external interface — never silently absent.<br>• `quickstart.md` links to the contracts and data model instead of duplicating them, and its commands either run or are marked not-yet-runnable with the reason. |
| SDD-13 | `plan.md` carries the traceability table: every `FR-###`, `SC-###` and story scenario, with its component and `Verified by` = `test` · `inspection` · `manual`.<br>• `test` names a file and function; `inspection` names what to look at and what to look for; `manual` gives steps a person follows.<br>• When a preview exists, its components are this table's entries — the design follows what was approved rather than re-inventing it.<br>• The rule that makes optional testing safe: a requirement may be un-tested, but it may not be un-verifiable. |
| SDD-14 | Plan's exit gate is seven checks; no code is written and `tasks.md` is not created here.<br>• Requirement coverage · entity coverage · interface coverage · decision provenance · constitution conformance · zero unknowns · verification declared — plus runnability of `quickstart.md`.<br>• A failing check is fixed before Tasks; one that cannot be fixed reopens the cycle at the stage that owns it, never carried forward as a known gap. |
| SDD-15 | Checklist items are reviewer-owned; the agent generates and never ticks; files are appended, never replaced.<br>• Items ask about the requirements — completeness, clarity, consistency, measurability, coverage — never whether the code works. Each carries a quality dimension and a traceability marker, at least 80% referenced to a section or a `[Gap]`.<br>• New file starts at `CHK001`; an existing file is appended continuing from the last ID.<br>• At most four focus areas, at most five scoping questions, a soft cap of 40 raw items collapsed by risk. |
| SDD-16 | Tasks are ordered by user story — Setup, Foundational, one phase per story, Polish — as `- [ ] T### [P] [USn] description with path`.<br>• `[P]` means order-independent, not concurrent: one agent in one thread, and the run states the order it actually used.<br>• A test task exists for each row declared `test`, and only when the repo requires tests. `inspection` and `manual` rows produce none.<br>• Delivery steps come from what the repo declares — git, a version scheme, a board — and an undeclared convention produces no step. |
| SDD-17 | Analyze writes `analysis.md`; gate 2 opens only at zero CRITICAL and 100% coverage; HIGH and below are reported, never fixed silently.<br>• `analysis.md` carries the date, the artifact SHAs it read, the metrics line, findings with a `Disposition` column, and a one-line-per-run History — so a stale report is visible as stale.<br>• Mechanical fixes are applied and reported as a delta before re-running: a requirement with no tasks, terminology drift, same-statement duplicates, stale paths and IDs.<br>• Intent fixes are the owner's: which of two conflicting requirements wins, narrowing or deleting a requirement, changing what an acceptance criterion means.<br>• Coverage reads Plan's traceability table rather than re-deriving it from tasks.<br>• A perfect Analyze is zero CRITICAL and full coverage, **not** zero findings — chasing the count pushes the writing toward satisfying the checker. |
| SDD-18 | **Gate 2**: present spec, plan, traceability with the verification split, every checklist unticked, tasks and analysis; every item must be ticked, and an unticked item is a change request.<br>• The plan is presented through the agent's plan mode/tool wherever one exists; chat prose only where there is none, and never as a preference.<br>• The verification split is stated as `n test · n inspection · n manual`, so coverage and evidence are visible rather than asserted.<br>• Every remaining finding is shown with its recommendation and the cost of leaving it; the owner decides which to fix and which to accept. |
| SDD-19 | After gate 2 the run is continuous — Implement → Converge → Fold — stopping only to report or at Converge's cap. |
| SDD-20 | Implement runs phase by phase, halts on a failing sequential task, and marks tasks `[X]` as they land.<br>• A failing `[P]` task lets its siblings finish.<br>• Project setup creates or verifies ignore files, which assumes git — a recorded exception to parts being independent, on the owner's instruction.<br>• Unchecked checklists here mean gate 2 was bypassed: stop and ask once, and never tick the files. |
| SDD-21 | Converge compares code against the traceability table, types each gap `missing` · `partial` · `contradicts` · `unrequested`, appends `## Phase N: Convergence`, and stops at three passes to ask.<br>• `contradicts` splits by root cause: code at fault becomes a task; spec at fault is a spec conflict, and the slice reopens at Specify.<br>• Each pass writes `converge.md` — pass number, what was checked, findings with evidence, outcome — because a clean run otherwise leaves no trace.<br>• At the cap the run asks, with a recommendation: continue with extra passes for this slice, accept the gaps, reopen at the stage the cause belongs to, or abandon. The answer is written into `converge.md`; a capped run is never silently finished.<br>• Each row is checked by the method it declared; `inspection` and `manual` rows are marked `checked by inspection`, so the reader can see how much rests on a command. |
| SDD-22 | Completion claims are never evidence: every task is re-assessed whatever its checkbox says. |
| SDD-23 | Fold runs only at Converged, writes the typed delta into `docs/spec/<capability>.md`, is idempotent, and treats an undeclared behaviour change as CRITICAL.<br>• The typed delta is `added` (a full block with scenarios), `modified` (the complete replacement block), `removed` (marked with its reason and date) and `renamed` (`R<n>` preserved).<br>• The header moves `last folded` to today and prepends the slice ID; `fold.md` records the capabilities touched, the operations, and the before/after counts.<br>• **Converged with accepted gaps** folds only what converged, and lists the rest in `fold.md` as `not folded — accepted gap`.<br>• A genuine refactor declares `no behaviour change` explicitly — the difference between "nobody updated the spec" and "the spec did not change".<br>• Fold cannot invent intent: it asks through the question tool, one at a time, and a skipped question becomes a recorded assumption in the capability file.<br>• No gate: gate 2 already approved the behaviour, and Fold is bookkeeping against it. |
| SDD-24 | Done means Converged, Folded and reported — never "the boxes are ticked". |
| SDD-25 | A revision re-enters at the earliest stage it touches; anything before gate 1 invalidates the plan rather than patching it.<br>• A changed requirement, story, acceptance criterion or scope re-enters at Specify; a wrongly answered or still-open question at Clarify; a design-only change at Preview.<br>• A plan built against a spec that no longer exists is cancelled, not adjusted, because every decision in it traces to an assumption that just changed. |
| SDD-26 | A change too large for one spec is split by user story, by capability or by risk — never by layer.<br>• It surfaces before gate 1 (the remainder becomes cards), at Plan (a re-entry, remainder to the board) or at Converge (the third pass finds structural gaps).<br>• Three prohibitions: two spec packs on one branch, a spec that grows after Accept, and a split where a slice cannot Fold coherently on its own. |
| SDD-27 | The closing report shows what shipped, the verification split, convergence with any accepted gaps, the capabilities folded, the branch and commit count, the version and changelog line, the PR title and body, that nothing is pushed — and then asks about pushing.<br>• The PR title and body are shown because they become the squash message. |

<!-- repo:begin part=sdd -->
- **Docs-only changes** may skip the numbered spec with a short plan and owner approval.
<!-- repo:end -->

**The original — Spec Kit's loop as published.**

- [SK:constitution] The constitution is optional, lives at `.specify/memory/constitution.md`, is loaded by every downstream stage *IF EXISTS*, and is never created automatically.
- [SK:specify] Specify asks up to three clarifying questions, batched, and defers the rest.
- [SK:specify] `spec.md` carries user stories prioritised P1/P2/P3, each with *why this priority*, an *independent test* and Given/When/Then scenarios, plus edge cases, `FR-###`, `SC-###` and assumptions.
- [SK:specify] Specify maintains `checklists/requirements.md` as a self-check, re-running up to three times.
- [SK:clarify] Clarify caps at five questions per session, one at a time, recommendation first; leftovers go on a Deferred list.
- [SK:plan] Plan fills Technical Context, runs the Constitution Check before Phase 0 and after Phase 1, writes `research.md`, `data-model.md`, `contracts/` and `quickstart.md`, then stops.
- [SK:checklist] Checklist items are requirements-quality questions, reviewer-owned and reviewer-ticked; Implement asks once and proceeds if any are unchecked.
- [SK:tasks] Tasks are ordered by user story — Setup, Foundational, one phase per story, Polish — with `[P]` meaning parallel.
- [SK:analyze] Analyze is read-only, writes nothing, grades findings and offers remediation the user applies.
- [SK:implement] Implement runs phase by phase, halts on a failing sequential task, asks once about unchecked checklists, and marks `[X]` as tasks land.
- [SK:converge] Converge assesses the present code against the artifacts, appends one task per finding, and loops back to Implement with no ceiling on passes.
- [SK:layout] Specs live at `specs/NNN-slug/`; the tooling lives in `.specify/`; the `specify` CLI is the runtime.

**The original — the family's shared shape, true of every model we support.**

- [FAM:trio] Requirements → design → tasks: three artifacts, produced in that order, each read back by the next stage.
- [FAM:what-before-how] The specification states what and why, before any technical decision is taken.
- [FAM:scenarios] Requirements are written as scenarios — Given/When/Then — so each one can be checked.
- [FAM:agent-reads-spec] The implementing agent consumes the specification at every stage, rather than once at the start.

## Tests — tdd

| ID | Rule |
| --- | --- |
| TDD-01 | A failing test comes before the code for every row declared `test`. |
| TDD-02 | The test must fail for the right reason; read the assertion before making it pass.<br>• A test that fails on an import error or a typo has proven nothing about the behaviour. |
| TDD-03 | Classicist: real collaborators; doubles only at process boundaries — network, clock, filesystem, randomness.<br>• Prefer a fake to a mock where one is cheap: an in-memory repository is honest, and it survives the interface moving.<br>• A double that must be updated whenever production code changes was testing structure — the classicist diagnosis. |
| TDD-04 | Never mock what you do not own.<br>• A double for a vendor SDK encodes a belief about the SDK and silently survives the SDK changing underneath it. |
| TDD-05 | A unit is a behaviour, not a function.<br>• The smallest thing a requirement can name. If you cannot name the behaviour, you are testing structure. |
| TDD-06 | One behaviour per test, named `test_<behaviour>_<condition>`.<br>• The name is the contract; a test called `test_works` documents nothing. |
| TDD-07 | A test is deleted only when the behaviour is gone or the test was wrong — never to make a change pass.<br>• Rewriting a test to match new code is a red flag: if the behaviour did not change, the test should not have to. |
| TDD-08 | Coverage is a diagnostic, never a gate; mutation score is the optional quality signal.<br>• Coverage says which lines ran. A threshold rewards suites with no assertions — a suite that reports well and catches nothing. |
| TDD-09 | A red test blocks; it is never skipped or quarantined silently.<br>• Quarantine is allowed only with a recorded reason and an owner. |

<!-- repo:begin part=tdd -->
- **Scope:** TDD governs domain and application rules. User-visible acceptance is Playwright
  (Python) E2E, run through Django's `LiveServerTestCase`.
- **Location:** a Django app's tests sit beside it (`<app>/tests.py`); cross-cutting and E2E tests
  live in `tests/`. The runner is Django's; coverage is measured with `coverage`.
<!-- repo:end -->

**The original — the Chicago/classicist school as published.**

- [CL:state-verification] Verify the state of the system after the behaviour, not the conversations it had.
- [CL:real-collaborators] Use the real collaborators; a test that mocks its own objects tests the mocks.
- [CL:boundary-doubles] Substitute only at awkward boundaries — network, clock, filesystem, randomness.
- [CL:fake-over-mock] Prefer a small fake to a mock where one is cheap.

**The original — Kent Beck's practice, 2002.**

- [BK:two-rules] Write no production code except to pass a failing test; eliminate the duplication that test exposes.
- [BK:cycle] Red → green → refactor: a test that fails, the least code that passes it, then design work while green.
- [BK:test-first] A test is written before the code it covers, and run to see it fail.
- [BK:small-steps] Small, frequent steps, with the suite run often enough that a break is found within minutes.
- [BK:kept] Tests stay after the code works: they are the specification of the code at unit level.

## Git — git-flow

| ID | Rule |
| --- | --- |
| GIT-01 | Never edit, stage or commit in a checkout of a receiving branch — the one that accumulates merged work, or the one that holds what shipped.<br>• A checkout of either is a place to read, not to write. Which branches those are comes from the flow's tip.<br>• Reading is not working: `log`, `diff`, `show`, inspecting behaviour — all fine. The rule is about writes. |
| GIT-02 | A slice works in its own worktree on its own branch: `git worktree add ../<repo>-NNN -b feat/NNN-slug develop`.<br>• One worktree, one branch, no switching. Under GIT-01 the main checkout stays on `develop` untouched. |
| GIT-03 | One slice, one branch, one PR; the branch carries the spec's `NNN`.<br>• The branch belongs to the slice, not to the card: `feat/106-tags-focused-row-hover` on card `ITEM-114` is correct. |
| GIT-04 | Squash into the integration branch; the squash message is the PR title plus its description.<br>• A slice's internal commits are noise once it lands, and the PR title already says what it did.<br>• The PR body is the authoring surface for the commit message: what is written there lands verbatim and stays. |
| GIT-05 | Merge into the shipped branch with a merge commit — every model, never squash, never fast-forward.<br>• This overrides GIT-04 where they meet: under a flow whose integration branch *is* the shipped branch, a merge is still a merge commit.<br>• A release must be a visible join between the line that shipped and the line it shipped from. |
| GIT-06 | Commits start at Fold: none before it, and every commit carries a green suite.<br>• No ceiling on how many follow, only a floor: none before Fold. No work-in-progress commits — a commit a later commit fixes is a commit `bisect` will land on. |
| GIT-07 | Push only on the owner's word — the first push and every update to an open PR.<br>• Local commits at Fold are expected output; the push is not. **An open PR is not standing permission.**<br>• The vault is the deliberate opposite — there the push *is* the sync. |
| GIT-08 | Never delete a local branch or worktree; remote branches follow the repo's settings.<br>• They are the undo trail: a merged slice may still need reverting, comparing, cherry-picking or explaining.<br>• No `branch -d` as a delivery step, no routine `prune`, and "clean up the branches" is not an instruction to delete. |
| GIT-09 | `release/X.Y.Z` is cut from `develop` when the slice set is complete and carries only the bump confirmation, the changelog and fixes.<br>• It may not change the number, except to drop a pre-release suffix — the bump arrives from the slices.<br>• **This overrides [GF:release]**, where the release branch sets the bump. |
| GIT-10 | The tag is cut on `main` only, never off `main`, and the back-merge to `develop` is never skipped.<br>• A release that does not return leaves `develop` numbered below `main`, so the next slice bumps from a stale base and the release after it collides. |
| GIT-11 | Conventional Commits: `type(scope): subject`, subject ≤72 characters, body for the why.<br>• The subject becomes the squash subject, so it is also the line that appears in `git log` forever. |

<!-- repo:begin part=git -->
- After a merge, delete the **remote** branch only; local branches and worktrees are kept.
- Never force-push `main` or `develop`; never create vendor- or agent-named branches.
- A docs-only change uses a `docs/<slug>` branch: there is no `NNN` to carry.
<!-- repo:end -->

**The original — Driessen, *A successful Git branching model* (2010), as published.**

- [GF:develop] Two long-lived branches: `main` holds what shipped, `develop` accumulates integrated work.
- [GF:branching] `feat/*` and `fix/*` branch off `develop` and merge back into it.
- [GF:release] `release/X.Y.Z` is cut from `develop` when the slice set is complete, carries the version bump, and merges to `main` and back to `develop`.
- [GF:hotfix] `hotfix/X.Y.Z` branches from `main` for an urgent fix and merges to `main` and back to `develop`.
- [GF:tag-main] `main` is tagged on every release.
- [GF:merged-branch] A merged branch is deleted. *(Retired by GIT-08.)*

**The original — git itself publishes no branching model; Conventional Commits publishes the commit grammar.**

- [GIT:branch-per-change] A change is made on a branch and reaches the integration line by merge, never by editing that line.
- [GIT:integration-line] One branch receives integrated work; which branch that is depends on the flow.
- [GIT:immutable-history] Published history is not rewritten; a fix is a new commit.
- [CC:type-scope] A commit subject is `type(scope): description`, imperative, one line.

## Versioning — semver

| ID | Rule |
| --- | --- |
| VER-01 | `VERSION` at the repo root is the single authority; tags are derived and checked against it.<br>• Every other copy — manifest, tag, changelog heading — is derived and checked, never independently set. |
| VER-02 | One scheme per repo, declared by the repo; the grammar recommends SemVer and never assumes it.<br>• The five questions every scheme must answer: what is versioned · what the number claims · where the truth lives · when it moves · who sets the level.<br>• Five invariants: one authority · a tag is `v` plus the authoritative version, cut only from a commit where the two match · a released version is immutable · a changelog section exists if and only if that version was released · version tags never share a namespace with branch-archive tags. |
| VER-03 | `bump` is declared at Plan and shown at gate 2.<br>• `bump: none \| patch \| minor \| major`. `none` is a declared value, never a silence.<br>• A `major` declaration is the most consequential line in the pack and belongs on screen before code. |
| VER-04 | The version change is applied immediately before the merge, in the delivery commit that also writes the changelog line and closes the card.<br>• Whatever the scheme calls the act — a bump, a date, a serial — it is stamped against what actually landed, not at the start of the slice. |
| VER-05 | `bump: none` is a declared value, and it means no `VERSION` change and no changelog entry.<br>• Internal refactors, test-only changes and internal docs are not notable changes to a user.<br>• A test change that accompanies a behaviour change takes the level **of the behaviour**, not of the test. |
| VER-06 | A released version is immutable: no retag, no reuse.<br>• A wrong entry is corrected by the next release, exactly as a released version is never retagged. |
| VER-07 | `CHANGELOG.md` always carries `## [Unreleased]`; a slice appends one line there; the release renames it and adds a fresh one.<br>• One line per user-visible change, past tense, naming the behaviour rather than the file: *"Saved views now survive a restart"*, never *"refactor ReadingView"*. |
| VER-08 | A released changelog section is never edited. |
| VER-09 | The changelog heading is the version verbatim, `VERSION` without its `v`.<br>• The six headings are a closed set — Added · Changed · Deprecated · Removed · Fixed · Security — and a section appears only when it has an entry.<br>• The normative template is below, and a repo copies it verbatim. |
| VER-10 | The level maps from what changed: a breaking change is `major`, a new capability is `minor`, a fix is `patch`.<br>• This mapping is the whole of SemVer's contribution to a plan, and it is why a plan may not declare a level the change does not support. |

<!-- repo:begin part=semver -->
- `CHANGELOG.md` carries the current history; everything before the 2026-09-30 adoption is
  preserved as-is in `docs/CHANGELOG-archive.md`.
<!-- repo:end -->

**The original — SemVer 2.0.0 as published.**

- [SV:levels] `MAJOR.MINOR.PATCH` — MAJOR for incompatible changes, MINOR for compatible additions, PATCH for compatible fixes.
- [SV:immutability] A published version is immutable; a change is a new version.
- [SV:pre] Pre-release (`-rc.1`) and build metadata (`+build`) are suffixes with their own ordering rules.
- [SV:public-api] `1.0.0` defines the public API; below it, anything may change.
- [SV:by-what-changed] The level is decided by what changed, not by how much work it took.

## Board — kanban

| ID | Rule |
| --- | --- |
| BRD-01 | Ideas land on the board first; a spec is written from one or more cards. |
| BRD-02 | A card is demand — not a spec, not a slice; several cards may share one spec.<br>• Measured: five cards on one spec in one repo, four on another, two in a third. |
| BRD-03 | The states are Backlog · Speccing · Ready · In progress · In review · Done, with `Archive` as a table, not a column.<br>• Backlog is the only priority-sorted column (P0 first, ties by ID); the others stay in workflow order, oldest first.<br>• The evidence column changes with the state: `Branch` in progress, `PR` in review, `Merged` in Done — `develop via #369`, a destination and a PR, never a commit hash. |
| BRD-04 | Only the owner picks a card into `Speccing` and only the owner promotes it to `Ready`.<br>• `Ready` is gate 1 seen from the board: an agent that moves a card there has granted itself an approval it does not have. |
| BRD-05 | `backlog/board.md` and `backlog/items/ITEM-XXX-slug.md` follow their templates verbatim; the evidence column changes with the state.<br>• Templates are normative: same header, same section order, same column order, same separator row, same frontmatter key order.<br>• The frontmatter carries the seams: `spec`, `branch`, `pr`, `issue`, `bump`, `release_version`. Empty cells are `—`, never blank and never `N/A`.<br>• The card body stays short — summary, notes, an acceptance sketch, links. A card carrying a full plan has become a spec.<br>• **A markdown board cannot enforce a WIP limit** ([KB:wip]): the limit is a rule the agent obeys, not a constraint the tool applies. |
| BRD-06 | The board ships in the same PR as the work. |
| BRD-07 | `In review` while the PR is open, `Done` before the merge — and `Done` is terminal.<br>• A finished card stays in Done forever, which is why that section grows without limit: a card that disappears takes its history with it. |
| BRD-08 | A card that ended without shipping is archived with a reason and a date, in the board's own archive or table.<br>• `cancelled`, `superseded`, `abandoned` — the record that non-shipped demand still existed. The index is the record of the card; the card is the record of the demand. |
| BRD-09 | A board word never enters a spec, and a spec word never enters a card's status.<br>• A spec is `Draft` or `Accepted` and never changes after gate 1. |
| BRD-10 | When the remote is GitHub, every card past `Speccing` carries one anchor issue: created as the card enters `Ready`, backfilled when an agent works with a card that reached those states with `issue:` empty; the number is stored in `issue:`, and PRs say `Refs`, never `Closes`.<br>• The anchor is **not** a second board and not a sync target: title `ITEM-120 — <title>`, a one-line pointer body, one `board:item` label, nothing else. Nothing is ever read back.<br>• **The trigger is the card's state, not the transition** — a card written after the work, a board adopted late or a status set by hand never passed through `Ready`. Backfill is per card and forward-looking. |
| BRD-11 | Only the owner closes a card; the agent may propose. |

<!-- repo:begin part=board -->
- The anchor label is `board:item`; one issue per card — created as the card enters `Ready`, and
  backfilled the first time an agent works with a card past `Speccing` that has no `issue:`. The
  backfill is reported in the slice's closing report.
<!-- repo:end -->

**The original — Kanban as published.**

- [KB:columns] Columns are workflow states, and work flows through them continuously.
- [KB:pull] An item is pulled when there is capacity, not pushed when there is a plan.
- [KB:wip] Work in progress is limited, and the limit is what makes the flow honest.
- [KB:picture] The board is a picture of the work in flight, not of everything anyone wants.
- [KB:cadence] Nothing is committed to a fixed iteration; the cadence is the arrival of work.

## Contracts

| ID | Contract |
| --- | --- |
| C-SDD-TDD | `Verified by: test` is the seam: a test row becomes two tasks under TDD, one without; SDD's ordering wins over TDD's.<br>• **Handoff.** Plan declares `Verified by: test` for a requirement; that row is the handoff. A row marked `inspection` or `manual` **never enters TDD**, and TDD may not demand a test for it.<br>• **Splitting.** With TDD active a `test` row becomes two tasks — *write a failing test for `US1/AC2`* and *make `US1/AC2` pass*. Without TDD it is one task; ids, `[P]` markers and ordering are unchanged.<br>• **Ordering.** SDD decides the sequence of tasks; TDD decides the sequence inside a task. A failing test cannot jump ahead of a foundational task.<br>• **Evidence.** A TDD test is stronger evidence than a written one because it failed first, and SDD still runs it rather than trusting that it exists.<br>• **Fold ignores it.** Behaviour is folded regardless of how it was verified; method is a slice fact, not a capability fact.<br>• **Ownership.** SDD owns the requirement and its verification method, the task set, the definition of done and the evidence standard for Converge. TDD owns red → green → refactor inside one behaviour, and when that behaviour counts as implemented.<br>• **Prohibitions.** TDD may not invent requirements — a test with no `Verified by` row behind it is `unrequested` work. SDD may not demand a test where its own table says `inspection`; changing the table is a gate-2 decision, never a mid-implementation one. Neither may close the other's loop: a passing test does not prove a task done, and a ticked task does not prove a behaviour works. |
| C-SDD-GIT | The run opens the branch at the change request; Fold makes the first commit; the merge follows the report.<br>• **The branch opens the slice.** It is cut when the change request arrives, not at delivery, because Specify writes `specs/NNN-slug/spec.md` into the repo and that file belongs to the same reviewed unit as the code. Cut later and the spec reviews in one PR while the implementation reviews in another.<br>• **One slice, one branch, one PR**, named by the flow the repo declares (`feat/NNN-slug`), with `NNN` matching the spec folder.<br>• **Deliver in the flow's shape.** Conventional commits; the feature branch squashed into the integration branch, its subject the PR title and its body the PR description.<br>• **Commits begin at Fold.** Nothing is committed while Specify, Clarify, Preview, Plan, Checklist, Tasks, Analyze, Implement or Converge run — the work stays in the tree. Fold makes the first commit: spec pack, code, board row and capability delta together, and only with the suite green. How many commits follow is not fixed.<br>• **Merging is not the finish line.** The slice ends at Converged + Folded + reported; the merge is the delivery step after it. A PR merged before Converge is a slice declared done on the strength of its checkboxes.<br>• **Ownership.** SDD owns when work starts and finishes and what the slice produces; git owns the base, the name, the target, the merge strategy and the PR mechanics.<br>• **Prohibitions.** SDD may not merge, tag or push. Git may not declare a slice done — green CI and an approved PR are not Converged, and a merged PR is not Folded. Neither may let a branch outlive its slice. The delivery phase merges and stops there: no branch deletion, no worktree removal, no prune. |
| C-SDD-VER | `bump` is declared at Plan, reviewed at gate 2 and applied in the pre-merge commit.<br>• **Declared.** `bump: none \| patch \| minor \| major` under a levelled scheme; `release: yes \| no` under CalVer or a serial. `none` / `no` is a declared value, never a silence.<br>• **Shown.** The bump is on screen at gate 2 — a `major` declaration is the most consequential line in the pack and belongs there before code, not in a changelog afterwards.<br>• **Applied late.** `VERSION` and the `## [Unreleased]` line are written immediately before the merge, in the same commit that closes the card — so the level is stamped against what actually landed after review, and the number never sits open across concurrent slices for the whole of a Fold.<br>• **Converge** does nothing with it, except that a released version is immutable: a finding is never satisfied by editing one.<br>• **Fold ignores it.** Versions are a repo fact, not a capability fact.<br>• **Ownership.** SDD owns the declaration in the plan and that the shipped change is recorded; versioning owns what each level means, whether the scheme has levels at all, where the truth lives and how the tag derives from it.<br>• **Prohibitions.** SDD may not invent a level the scheme does not have — `bump: patch` under CalVer or `bump: major` under 0ver is a malformed plan, rejected at gate 2, never silently downgraded. Versioning may not move the number without a declaration. Neither may be inferred from the other: a changelog entry does not imply a bump, and a bump does not imply a written entry. |
| C-SDD-BOARD | Card ≠ slice; the loop moves the card; `Ready` is gate 1; an accepted Converge gap becomes a new card.<br>• **Card ≠ slice.** The card is demand; the spec pack is work. One spec may consume several cards, and one card may wait years for its spec. The card's `spec:` field is written when Specify starts and names one folder — several cards pointing at the same folder is normal.<br>• **The loop moves the card.** Specify → `Speccing` · gate 1 Accept → `Ready` · Implement → `In progress` · PR open → `In review` · before merge → `Done`.<br>• **The move to `In review` is delivery's step, not Converge's or Fold's.** Converge ends with the code matching the traceability table and Fold writes the capability delta; neither has a PR, so a card moved there claims a review that has not started. The move waits until the push has opened the PR — the `pr:` field cannot be written before its number exists — and lands as the slice's last commit on that same PR. `Done` takes the same shape one step later: a commit before the merge, not a stage of the loop.<br>• **`Ready` is gate 1 seen from the board.** Only the owner promotes a card, and only a card whose spec passed gate 1 can be promoted. An agent that moves a card to `Ready` has granted itself an approval it does not have.<br>• **`done` is not the spec's status.** Merged is a board fact; a spec's `Status` is `Draft` or `Accepted` and never changes after gate 1. Board words never enter a spec's status, and spec words never enter `status:`.<br>• **A gap is fresh demand.** An accepted Converge gap becomes a new card; folding it back into the finished card would make `Done` mean "mostly done".<br>• **Ownership.** SDD owns the slice — pack, gates, Converge, Fold and what done means for the work. The board owns the item — capture, ordering, commitment, and which demand produced which slice.<br>• **Prohibitions.** SDD may not write the board as if it were an artifact: the spec pack never edits `backlog/`, and the agent moves the card as a step visible in the same PR. The board may not gate the spec: no card state can block gate 1 or gate 2. Neither may call a slice Done while it is unconverged. |
| C-TDD-GIT | No commit before Fold, and every commit green — no work-in-progress commits.<br>• A commit claims this tree is worth keeping; a red tree is not. The suite runs before the commit, not after it.<br>• Commits start at Fold, so the first commit records converged work rather than work in progress. There is no ceiling on how many follow — a revision adds one, so does the delivery bookkeeping — only a floor: none before Fold.<br>• Nothing is committed between red and green. The working tree and `git stash` exist for that; history does not, because a commit a later commit fixes is a commit `bisect` will land on.<br>• **Ownership.** TDD owns whether the suite is green and what green means; git owns when a commit exists and what it contains.<br>• **Prohibitions.** git may not require a commit between red and green — the cycle is unobservable in history by design, and the squash plus the first-commit-at-Fold rule both erase it. Neither may impose a commit count. TDD may not commit to save work: if the tree must be preserved mid-slice, that is a stash, a patch or a worktree — never a red commit with an apologetic message. |
| C-TDD-VER | No bump on a red suite; tests-only changes are `bump: none`; a tag comes from the released commit's own green run.<br>• The delivery step that moves `VERSION` runs only after Converge, and Converge does not report Converged over failing tests.<br>• A test change that accompanies a behaviour change takes the level **of the behaviour**, not of the test.<br>• **Ownership.** TDD owns whether the suite is green and what green means; versioning owns what the number claims and which level a change takes.<br>• **Prohibitions.** Versioning may not read a green suite as evidence for a level — a passing build says nothing about compatibility. TDD may not decide the number — "we added tests for it" is not a reason to bump. Neither may release a red suite by retagging: a red `main` is a hotfix, not a new tag. |
| C-GIT-VER | The bump lands on `develop` with the squash; the release branch confirms rather than sets it; the tag matches `main`.<br>• **Per slice.** Each merged slice applies its declared level, written on the slice branch in the pre-merge commit, so `develop`'s `VERSION` runs **ahead of every tag — by design, not drift**.<br>• **The release branch promotes.** It carries `develop`'s version to `main` and may not change it, except to drop a pre-release suffix.<br>• **The tag matches `main`.** Versioning's invariant is scoped accordingly: a tag that disagrees with `main` is an error; a tag behind `develop` is normal.<br>• **Ownership.** git owns when a version is promoted and that only `main` is released and tagged; versioning owns what the number means and where the truth lives.<br>• **Prohibitions.** git may not tag off `main`. Versioning may not move `main`'s number outside a release or hotfix merge. Neither may skip the back-merge — it leaves `develop` numbered below `main`, so the next slice bumps from a stale base and the release after it collides. |
| C-BOARD-GIT | The branch carries the spec's `NNN`; the card records `branch` and `pr`; `Done` is set before the merge.<br>• The branch belongs to the slice, not the card: `feat/106-tags-focused-row-hover` on card `ITEM-114`, never `feat/ITEM-114`.<br>• `branch:` and `pr:` are written when they exist, never predicted. A card in `In review` with no `pr:` is a card nobody can check.<br>• **The `In review` move is a commit after the PR exists.** It happens once the push has created the PR and returned its number, so it is normally the branch's second commit — the slice, then the move. That is the shape "in the same PR" allows: the move must appear in that PR's diff before the merge, and it may not appear earlier, because the number it carries does not exist yet. `Done` follows the same pattern in the pre-merge commit.<br>• `Done` is set before the merge and `In review` while the PR is open: merge is git's act, and the card is closed on the way through it.<br>• The branch outlives the merge, so the card keeps pointing at something that still resolves — the cleanup rule in vexbook-git is what keeps that field honest years later.<br>• **Ownership.** The board owns what the card says and when it moves; git owns the branch, the PR and the merge.<br>• **Prohibitions.** The card may not name a branch that does not exist. git may not move cards — no hook, no post-merge automation; the agent moves the card in the same PR, where the move is reviewable. Neither may treat a green build as `Done`: that is Converge's call, not CI's. |
| C-BOARD-VER | `release_version:` is filled at release, never at merge.<br>• The card's `bump:` is declared at Plan and must equal the slice's `VERSION` change; a card with `bump: none` landing inside a patch release is one decision recorded twice, disagreeing.<br>• Merged is not shipped: a card claiming `1.12.1` while sitting on `develop` is claiming a release that has not happened.<br>• The release is assembled from cards — the changelog states *what changed*, the board answers *which demand*.<br>• **Ownership.** The board owns which card shipped and in which release; versioning owns the number and its level.<br>• **Prohibitions.** The board may not invent a version — only the release sets `release_version`, and an agent filling it at merge is guessing at a future it does not control. Versioning may not demand a card per commit: one card, one slice, one bump; the card is not a journal. Neither may let a card's `release_version` disagree with the tags — if the card says `1.12.1` and no such tag exists, one of them is wrong. |

**Board × TDD has no contract.** The board never gates on tests; Converge does, per
requirement. A second place deciding "is it done" would disagree with the first.
