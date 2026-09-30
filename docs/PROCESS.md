# Process

Locked way of working for **this repository** and every project spawned from it. Vexbook is the live example: it follows this file the same way a child repo does. Stack and language are **not** locked here — see [KICKOFF.md](./KICKOFF.md). **SemVer is locked.** Git model is chosen at kickoff for each spawned project; this repo uses GitHub Flow (see [ARCHITECTURE.md](./ARCHITECTURE.md)).

Humans and AIs follow this file and [KICKOFF.md](./KICKOFF.md). Do not invent a second process for vexbook.

## Adopt / sync

- **Greenfield** (spawn from the GitHub template): [KICKOFF.md](./KICKOFF.md).
- **Existing** repo, or **keep-up** when behind a newer vexbook process: [ADOPT.md](./ADOPT.md). Owner-triggered only — agents never sync unprompted.

## Must-apply shared docs

Agents and humans that implement here must apply these docs (re-read when working):

| Doc | Role |
| --- | --- |
| [`docs/rules/SDD-GATE.md`](./rules/SDD-GATE.md) | Hard SDD permission gate |

When a future always-on process doc is added, append it to this table. See [Vendor project rules](#vendor-project-rules).

## Spec-Driven Development (SDD)

Every behavior, CSS, or copy change follows this loop.

1. **Plan** — what / why / scope / edges (short is fine). Manual notes or any AI agent plan mode both count.
2. **Draft** — write `specs/NNN-slug/{plan,spec,tasks}.md` with Given / When / Then **before** any implementation.
3. **STOP** — wait for the project owner’s explicit Accept / OK **on that Draft**. Plan work **stops at Draft specs**. Approving a plan is not permission to implement. If you are unsure whether Accept / OK applies to this Draft, **ask again** — do not treat ambiguous “proceed”, plan-UI accept, or “OK” on a different artifact as implement permission.
4. **Execute** — TDD (red → green → refactor) for domain and application rules; E2E for user-visible acceptance using whatever tool this project chose at scaffold. One branch per spec. Land via the git model chosen at kickoff.
5. **Done** — PR links the spec; behavior changes without a matching spec update are incomplete.

“Proceed” on a **new** ask means advance the current SDD step (usually: write Drafts). It does not mean implement. “Proceed” / Accept on an **already Accepted** Draft means implement that spec only.

### Spec layout

- One folder per slice: `specs/NNN-slug/{plan,spec,tasks}.md`.
- IDs are **consecutive integers**. Never skip. If two concerns merge into one spec, the next slice still uses the next integer.
- **Spec 000** is reserved for **project scaffolding** and must stay **one spec** (including CI once a stack exists).
- Drafts include all three files (plan, spec, tasks) before Accept.
- One concern per spec. Split unrelated work.
- A spec may be written from **one or more** ITEMs.

Ops / docs-only / hotfix one-liners may skip a numbered spec, but still get a short plan and OK when more than trivial. CSS and copy **do not** skip a numbered spec.

## TDD

Default implementation loop for domain and application rules:

1. Red — failing test
2. Green — minimal code
3. Refactor — keep green

Name test files in `tasks.md`. The E2E tool is chosen per project (not named in vexbook).

## ITEM board

Every project keeps a Kanban:

- Index: [`backlog/board.md`](../backlog/board.md)
- One file per item: `backlog/items/ITEM-XXX.md` from [`backlog/items/_template.md`](../backlog/items/_template.md)

Ideas land on the board first. A spec is written **from one or more items**. Board, ITEM, tasks, and (when `bump` is not `none`) `VERSION`/changelog all land in **the same PR** as the work. Extra commits on that PR are fine, before or after Accept. Do not merge and then open another PR to finish them.

Priority is **P0** (highest) … **P3**. **Only the Backlog column is sorted by priority** (P0 first; ties by ID). Speccing / Ready / In progress / In review / Done stay in workflow order.

Typical `ITEM-000` → spec 000 (scaffold).

### One PR is complete

Vexbook and spawned projects share this — vexbook is the live example, not an exception. Extra commits on the branch are fine. A PR must not merge until it already has:

| Git | Already in that PR |
| --- | --- |
| Draft or ready PR open | ITEM **In review**, `pr:` set, draft-PR task checked |
| About to merge | ITEM **Done**; tasks that this merge completes are checked |
| `bump` is not `none` | `VERSION` bumped, changelog `## [X.Y.Z]`, `release_version` set |
| `bump` is `none` | `VERSION` unchanged; no tag |

After merge, if the slice versions: annotated tag `vX.Y.Z` and GitHub Release in the **same session** (a tag is not a commit). Do not open a follow-up PR to move the ITEM, check boxes, or bump the version.

Never force-push `main`, `develop`, or other protected branches.

## Git (choose at kickoff)

vexbook records **both** models. The project picks one at kickoff and writes it in `docs/ARCHITECTURE.md` or an ADR.

### GitHub Flow

- `main` is always deployable.
- Short-lived branches: `feat/*`, `fix/*`, `chore/*`, `docs/*`.
- Open a PR into `main`.
- **Normal features / chores / docs:** squash-merge.
- **Hotfixes only:** merge commit (preserve hotfix history).
- Scaffold may land on `main` **once**. After that, branches + PRs.

### Git Flow

- `main` is production.
- `develop` is integration.
- Features from `develop` (`feat/*`, …). Hotfixes from `main`.
- Default PR target for features: `develop`.
- Release cuts `main` when the owner says release.

### Shared hygiene (always)

- Never create `cursor/`, vendor-named, or other **non-standard / agent-related** branches. Use only the documented flow prefixes (`feat/*`, `fix/*`, `chore/*`, `docs/*`, …).
- Never force-push protected branches (`main`, `develop`) unless the owner explicitly asks.
- Never commit secrets.

## Vendor project rules

The committed template does **not** ship vendor agent directories (`.cursor/`, `.claude/`, and so on). Do **not** add those paths to `.gitignore` on vexbook to hide them.

**First session** (and whenever the must-apply list gains an entry): if this agent’s project-rules dir is missing or incomplete, create or update minimal local vendor rules that **reference every** [must-apply shared doc](#must-apply-shared-docs). Example for Cursor: `.cursor/rules/` entries with `alwaysApply` that defer to those paths. Do not invent process; only wire the vendor loader to the shared docs.

- **Vexbook:** leave that local vendor dir **untracked**. Do not commit it.
- **Spawns:** default leave untracked. **Commit** the vendor rules dir when the **owner** decides it is needed **or** the **agent** judges it is needed (tell the owner; record in child `ARCHITECTURE.md` or kickoff notes).

## Versioning (locked)

Every project from this template uses **SemVer**. There is no project-level “no versioning” choice. Kickoff does not ask.

Conventional Commits stay as they are. They do **not** decide the bump. The ITEM/spec `bump` field does.

### Version identity

Three records, one number:

- **Canonical published version:** annotated git tag `vX.Y.Z` on `main`
- **In-tree current version:** repo-root [`VERSION`](../VERSION) — one line `X.Y.Z` (no `v`)
- **History:** [`CHANGELOG.md`](../CHANGELOG.md) in Keep a Changelog shape (`## [Unreleased]`, then `## [X.Y.Z] - YYYY-MM-DD`). Spawned projects start from [`templates/changelog.md`](../templates/changelog.md) (copy over `CHANGELOG.md` at kickoff; then remove the entire `templates/` directory).
- **Traceability:** ITEM `bump` (intent for this slice) and `release_version` (filled when the item is in a tagged release)

A child Spec 000 may **mirror** `VERSION` into language tooling (`package.json`, and so on). That mirror is not a second source of truth. Record those paths in the child [`ARCHITECTURE.md`](./ARCHITECTURE.md).

Create a GitHub Release for each tag. The body is that version’s changelog section.

### When to bump

Each ITEM/spec sets `bump:` to exactly one of:

- `major` — breaking for consumers (API, data model, or locked process that others must follow)
- `minor` — backward-compatible capability
- `patch` — backward-compatible fix
- `none` — no shipped version impact

**The spec PR is the release** when `bump` is not `none`. In **that same PR** (extra commits are fine):

- `VERSION` = current plus this slice’s bump (highest bump if several ITEMs share the PR)
- `CHANGELOG.md` `## [X.Y.Z] - <date>` for this slice (keep an empty `[Unreleased]` heading)
- `release_version: X.Y.Z` on included ITEMs

Arithmetic is ordinary SemVer (`0.1.0` + major → `1.0.0`, + minor → `0.2.0`, + patch → `0.1.1`). Spawned projects start at `0.0.0`; Spec 000 with `minor` is usually `0.1.0`.

`bump: none` does not change `VERSION`, does not add a version section, and is not tagged.

There is no second PR whose job is only to bump the version or promote the changelog. Spec 001’s separate `chore/release-*` path is superseded.

### How a versioned slice lands

1. Same PR already has `VERSION`, changelog section, `release_version`, ITEM Done, and tasks checked.
2. Merge per git model.
3. **Same session:** annotated tag `vX.Y.Z` on `main`; GitHub Release body = that changelog section.

**GitHub Flow:** squash-merge into `main`, then tag that commit.

**Git Flow:** the spec PR (already versioned) targets `develop`. When the owner cuts `main`, tag the `VERSION` already on that cut. Merge back to `develop` so `VERSION` matches.

**Hotfix:** default `bump: patch`. The fix PR is the patch release. Git model unchanged (GitHub Flow: merge commit; Git Flow: from `main`).

## Commits and PRs

- Conventional Commits: `type(scope): imperative subject`.
- Agent commits end with a `Co-authored-by` trailer for **the vendor product that authored the commit**. Never copy another vendor’s trailer. Examples (illustrative, not exhaustive): Cursor → `Co-authored-by: Cursor <cursoragent@cursor.com>`; Claude Code → `Co-authored-by: Claude <noreply@anthropic.com>`; other vendors → that product’s published agent trailer.
- Open **draft** PRs. Body uses the repository PR template (Summary / Spec / Test plan).

## Architecture

Not locked by vexbook. The implementer chooses a pattern (layers, ports, or otherwise) and may migrate mid-project.

On every decide or change: **tell the project owner**, then write or update [`ARCHITECTURE.md`](./ARCHITECTURE.md) and an ADR so humans and AIs follow the doc, not memory.

## Definition of done (feature PR)

- [ ] Spec added or updated
- [ ] ITEM + board + tasks complete **in this PR** (In review while open; Done before merge). Extra commits on the PR are fine.
- [ ] ITEM and spec `bump` set (`major` / `minor` / `patch` / `none`)
- [ ] If bump is not `none`: `VERSION` + changelog `## [X.Y.Z]` + `release_version` are in **this PR**
- [ ] If bump is `none`: `VERSION` unchanged; no tag
- [ ] Tests for new domain/application rules (TDD)
- [ ] E2E for new acceptance, or explicitly deferred in spec out-of-scope
- [ ] Conventional Commit; PR Summary + Spec + Test plan filled
- [ ] Merge session: tag `vX.Y.Z` + GitHub Release when bump is not `none`
