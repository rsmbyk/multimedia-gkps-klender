# Git Flow

This project uses **Git Flow** with two long-lived branches and short-lived
topic branches. Production deploys from **`main`** (Vercel). Day-to-day work
integrates on **`develop`**.

Version numbers and changelog tags are defined in [`VERSIONING.md`](VERSIONING.md).
This document only covers **when** and **how** those bumps happen in the branch
lifecycle.

## Branch roles

| Branch | Lifetime | Purpose |
|--------|----------|---------|
| `main` | Permanent | Production-ready code only. What Vercel deploys. |
| `develop` | Permanent | Integration branch. Default base for new work. |
| `feature/*` | Short | New capabilities. |
| `fix/*` | Short | Bug fixes that are not production hotfixes. |
| `chore/*` | Short | Tooling, docs, deps, non-product chores. |
| `release/x.y.z` | Short | Prepare a named release from `develop`. |
| `hotfix/*` | Short | Emergency fixes branched from `main`. |

### Who may land on `main`

**Only** pull requests from:

- `release/*`
- `hotfix/*`

No feature, fix, or chore work merges directly into `main`.

## Pull requests (always)

Every change lands through a **pull request**. Do not push commits straight onto
`main` or `develop` for product work.

Suggested PR title style: Conventional Commits subject
(e.g. `fix(obs): restore songbooks dropdown loading`).

## Merge methods

| Target | Source | Method | Why |
|--------|--------|--------|-----|
| `develop` | `feature/*`, `fix/*`, `chore/*`, `docs/*` | **Squash merge** | One clean commit per topic on develop. |
| `develop` | `release/*`, `hotfix/*` | **Merge commit (standard merge)** | Preserve the release/hotfix join; do not squash. |
| `main` | `release/*`, `hotfix/*` | **Merge commit (standard merge)** | Preserve release/hotfix history on production. |

Rules:

- Topic branches (`feature/*`, `fix/*`, `chore/*`, `docs/*`) into `develop`:
  **always squash merge**.
- **Any** merge into `main` (only `release/*` or `hotfix/*` may target it):
  **always a standard merge (merge commit), never squash**.
- Never squash a release or hotfix PR, regardless of target.

When using the GitHub UI, pick the matching merge button. Do not squash a
release or hotfix into `develop` or `main`.

## Branch deletion

- After a merge, delete **only the remote branch** (e.g.
  `git push origin --delete <branch>`, or rely on the repo's
  “Automatically delete head branches” setting, which removes the remote head
  branch only).
- **Leave local branches intact.** Each developer prunes their own locals when
  they no longer need them (e.g. `git branch -d <branch>`).

## Day-to-day feature / fix / chore

```text
develop ──► feature/my-change ──(PR, squash)──► develop
```

1. Update local `develop` and create a branch:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/short-name
   ```
2. Implement, commit (Conventional Commits), push the branch.
3. Open a PR **into `develop`**.
4. Before merge: add changelog bullets under `## Unreleased` with **area
   labels** (e.g. `[songs]`, `[deploy]`). Do **not** bump SemVer on develop.
   See [`VERSIONING.md`](VERSIONING.md).
5. **Squash merge** into `develop`.
6. Delete the remote topic branch only (see [Branch deletion](#branch-deletion));
   keep the local branch.

Docs-only or pure tooling chores still use a PR; add `[docs]` / `[test]`
bullets when the change is worth recording, otherwise a PR description is
enough.

## Release flow

```text
develop ──► release/x.y.z ──(PR, merge)──► main   (tag vX.Y.Z)
                 │
                 └──(PR, merge)──► develop
```

1. When `develop` is ready to ship, branch from it:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b release/0.5.0
   ```
2. On the release branch **only**:
   - Choose and finalize **SemVer** (`MAJOR.MINOR.PATCH`) in `CHANGELOG.md`
   - Move `## Unreleased` into `## Version x.y.z` (no App Versions block)
   - Set the centralized JS-readable version constant (when it exists)
   - Confirm the shared OBS footer shows that version (when it exists)
3. Open a PR: `release/x.y.z` → **`main`**. **Merge commit** (not squash).
4. Tag the release on `main`:
   ```bash
   git checkout main
   git pull origin main
   git tag v0.5.0
   git push origin v0.5.0
   ```
   Optionally create a GitHub Release from that tag.
5. Open a PR: `release/x.y.z` → **`develop`** (or merge `main` back if that is
   cleaner after the tag). **Merge commit** (not squash).
6. Delete the remote release branch after both merges; keep the local branch
   (see [Branch deletion](#branch-deletion)).

Vercel deploys from `main` after step 3. The tag labels the shipped commit; it
does not replace the production branch.

## Hotfix flow

```text
main ──► hotfix/short-name ──(PR, merge)──► main   (tag if patch release)
               │
               └──(PR, merge)──► develop
```

1. Branch from production:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/short-name
   ```
2. Fix the issue. If this ships as a patch release, bump SemVer and the
   changelog on the hotfix branch (same finalize rules as a mini release).
3. PR → **`main`**, **merge commit**. Tag if you cut a patch (`vX.Y.Z`).
4. PR → **`develop`**, **merge commit** (not squash). Reconcile changelog /
   Unreleased if develop had moved ahead.
5. Delete the remote hotfix branch only; keep the local branch (see
   [Branch deletion](#branch-deletion)).

## Checklist: shipping a normal change

- [ ] Branched from latest `develop`
- [ ] PR targets `develop`
- [ ] `## Unreleased` changelog bullets + area labels (if product-facing)
- [ ] SemVer **not** bumped on this PR
- [ ] Squash merge into `develop`
- [ ] Remote topic branch deleted (local kept)

## Checklist: cutting a release

- [ ] `release/x.y.z` cut from latest `develop`
- [ ] SemVer + changelog finalized on the release branch (from Unreleased)
- [ ] Version constant + shared footer updated when that UI exists
- [ ] Merge commit into `main`
- [ ] Tag `vX.Y.Z` pushed
- [ ] Merge commit back into `develop`
- [ ] Remote release branch deleted (local kept)

## Checklist: production hotfix

- [ ] `hotfix/*` cut from latest `main`
- [ ] Merge commit into `main` (+ tag if patch release)
- [ ] Merge commit into `develop`
- [ ] Remote hotfix branch deleted (local kept)

## What not to do

- Do not commit feature work on `main`
- Do not merge `feature/*` / `fix/*` / `chore/*` into `main`
- Do not squash `release/*` or `hotfix/*` into `main` or `develop`
- Do not keep long-lived branches other than `main` and `develop`
- Do not finalize the `MAJOR.MINOR.PATCH` release version on a feature PR —
  that happens on `release/*` (or on `hotfix/*` for a patch)

## GitHub repository settings

Configured for this private repo (Free plan):

| Setting | Value |
|---------|--------|
| Default branch | `develop` |
| Allow merge commits | Yes (use for `release/*` / `hotfix/*` → `main` and → `develop`) |
| Allow squash merging | Yes (use for `feature/*` / `fix/*` / `chore/*` → `develop`) |
| Allow rebase merging | No |
| Automatically delete head branches | Yes (removes the remote head branch only; local branches are never touched) |
| Squash commit title / message | PR title / commit messages |
| Merge commit title / message | PR title / PR body |

### Branch protection (not available on Free private repos)

Classic branch protection and repository rulesets require **GitHub Pro** (or a
public repository). Until that is available, enforce the merge matrix by
discipline and by following this doc:

- Never merge into `main` except from `release/*` or `hotfix/*`
- Never squash a release or hotfix PR — anything merged into `main` uses a
  standard merge (merge commit)
- Squash-merge topic branches (`feature/*`, `fix/*`, `chore/*`, `docs/*`) into
  `develop`
- Delete only remote branches after merge; leave local branches intact
- Prefer the GitHub merge button that matches the table above

When Pro is enabled, add protection roughly as follows:

**`main`**

- Require a pull request before merging
- Restrict who can push (optional)
- Do not allow force pushes or deletions
- Prefer requiring merge commits only if the UI allows limiting methods per
  branch; otherwise keep both merge + squash enabled at repo level and choose
  the correct button per PR type

**`develop`**

- Require a pull request before merging
- Do not allow force pushes or deletions
