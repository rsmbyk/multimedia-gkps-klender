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
| `develop` | `feature/*`, `fix/*`, `chore/*` | **Squash merge** | One clean commit per topic on develop. |
| `develop` | `release/*`, `hotfix/*` | **Merge commit** | Preserve the release/hotfix join; do not squash. |
| `main` | `release/*`, `hotfix/*` | **Merge commit** | Preserve release/hotfix history on production. |

When using the GitHub UI, pick the matching merge button. Do not squash a
release or hotfix into `develop` or `main`.

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
4. Before merge: bump **app counters** for every app you changed (`b` / `s` /
   `t` / `p` / `dj`), update templates if OBS-facing, and add changelog bullets
   with the correct `[tag]` prefixes. See [`VERSIONING.md`](VERSIONING.md).
5. **Squash merge** into `develop`.
6. Delete the topic branch (local and remote).

Docs-only or pure tooling chores that do not change any app may omit an app
counter bump; still open a PR and squash into `develop`.

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
   git checkout -b release/0.4.18
   ```
2. On the release branch **only**:
   - Finalize the **release version** (`MAJOR.MINOR.PATCH`) in `CHANGELOG.md`
   - Sync the **App Versions** block for that release
   - Finish any remaining release-section changelog polish
   - Ensure OBS template version strings match the App Versions table
3. Open a PR: `release/x.y.z` → **`main`**. **Merge commit** (not squash).
4. Tag the release on `main`:
   ```bash
   git checkout main
   git pull origin main
   git tag v0.4.18
   git push origin v0.4.18
   ```
   Optionally create a GitHub Release from that tag.
5. Open a PR: `release/x.y.z` → **`develop`** (or merge `main` back if that is
   cleaner after the tag). **Merge commit** (not squash).
6. Delete the release branch after both merges.

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
2. Fix the issue. If this ships as a patch release, bump the release version and
   changelog on the hotfix branch (same finalize rules as a mini release).
3. PR → **`main`**, **merge commit**. Tag if you cut a patch (`vX.Y.Z`).
4. PR → **`develop`**, **merge commit** (not squash). Carry any app-counter or
   changelog updates develop still needs.
5. Delete the hotfix branch.

## Checklist: shipping a normal change

- [ ] Branched from latest `develop`
- [ ] PR targets `develop`
- [ ] App counters + changelog updated for affected apps (if any)
- [ ] Squash merge into `develop`
- [ ] Topic branch deleted

## Checklist: cutting a release

- [ ] `release/x.y.z` cut from latest `develop`
- [ ] Release version + App Versions + changelog finalized on the release branch
- [ ] Merge commit into `main`
- [ ] Tag `vX.Y.Z` pushed
- [ ] Merge commit back into `develop`
- [ ] Release branch deleted

## Checklist: production hotfix

- [ ] `hotfix/*` cut from latest `main`
- [ ] Merge commit into `main` (+ tag if patch release)
- [ ] Merge commit into `develop`
- [ ] Hotfix branch deleted

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
| Automatically delete head branches | Yes |
| Squash commit title / message | PR title / commit messages |
| Merge commit title / message | PR title / PR body |

### Branch protection (not available on Free private repos)

Classic branch protection and repository rulesets require **GitHub Pro** (or a
public repository). Until that is available, enforce the merge matrix by
discipline and by following this doc:

- Never merge into `main` except from `release/*` or `hotfix/*`
- Never squash a release or hotfix PR
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
