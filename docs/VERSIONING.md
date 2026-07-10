# Versioning

This project uses a **single [Semantic Versioning](https://semver.org/)
(`MAJOR.MINOR.PATCH`)** number for the whole application (Django, API, web
admin, and all OBS docks / sources).

See [`CHANGELOG.md`](../CHANGELOG.md) for shipped history. Branching and when
the version is finalized are defined in [`GIT_FLOW.md`](GIT_FLOW.md).

## Current scheme (from `0.5.0`)

Format: `MAJOR.MINOR.PATCH` (e.g. `0.5.0`)

Git tags use a `v` prefix: `v0.5.0`.

| Bump | When |
|------|------|
| **MAJOR** | Breaking changes (API contracts, OBS message shapes, incompatible data migrations) |
| **MINOR** | New features or notable backward-compatible behavior |
| **PATCH** | Bug fixes, deploy/plumbing, small tweaks, docs that ship with a tagged release |

There is **one** product version. There are no per-plugin counters (`b` / `s` /
`t` / `p` / `dj`) and no `v0.4.s30`-style strings in the new scheme.

### Jump to `0.5.0`

Production on the old scheme ended at **`0.4.17`** (per-app counters in the
changelog and hardcoded OBS template strings). The **first release under this
document is `0.5.0`**, which marks the versioning switch. Until that release is
cut and tagged on `main`, develop may document upcoming work under
`## Unreleased` while production remains `0.4.17`.

Older `CHANGELOG.md` sections keep their historical **App Versions** blocks for
archive; do not add new ones.

## When the version changes

| On | Action |
|----|--------|
| Feature / fix / chore PR into **`develop`** | **Do not** bump SemVer. Add bullets under `## Unreleased` with area labels (below). |
| **`release/x.y.z`** branch | Choose and finalize `MAJOR.MINOR.PATCH`, rename/move `Unreleased` into `## Version x.y.z`, set the centralized version constant, update the shared OBS footer. |
| Tag on **`main`** after release merge | `vX.Y.Z` |
| **`hotfix/*`** | Usually a **PATCH** bump on the hotfix branch; same finalize steps, then merge to `main` and `develop`. |

## Changelog area labels (non-version)

Bullets still carry **area labels** so history stays skimmable. Labels do **not**
include version numbers.

```text
[songs] Restore songbooks dropdown loading after Rx regression
[bible, project] Fix arrow-key navigation in dock and source
[deploy] Restore vercel.json WSGI routing for production
[docs] Adopt Git Flow and SemVer versioning
```

Suggested labels (use what fits; combine with commas when needed):

| Label | Surface |
|-------|---------|
| `songs` | Songs OBS dock / source |
| `bible` | Bible OBS dock / source |
| `tatib` | Tatib OBS dock / source |
| `project` | Project OBS source / settings |
| `api` | REST API |
| `web` | Django web admin UI |
| `deploy` | Hosting, Vercel, Docker, static serving |
| `docs` | Documentation / project conventions |
| `test` | Test toolchain |

## UI display (planned; not implemented in this docs pass)

- **One shared footer** on OBS pages shows the single app version (e.g. `0.5.0`).
- **One JS-readable constant** is the source of truth for that string (exact path
  to be added when the UI work lands). Templates and docks must not hardcode
  divergent per-app versions.

Until that lands, old per-app strings in templates may still be visible in
`0.4.x` production; remove them as part of the `0.5.0` release work.

## Checklist: change on `develop`

1. Implement the behavior (TDD where applicable — see [`TDD.md`](TDD.md)).
2. Add changelog bullet(s) under `## Unreleased` with area label(s).
3. Do **not** bump SemVer or create a release section yet.

## Checklist: cutting a release

1. Branch `release/x.y.z` from `develop`.
2. Decide `MAJOR` / `MINOR` / `PATCH` from the Unreleased bullets.
3. Turn `Unreleased` into `## Version x.y.z` (no App Versions block).
4. Set the centralized JS-readable version constant to `x.y.z`.
5. Confirm the shared OBS footer reads that constant.
6. Merge to `main` (merge commit), tag `vX.Y.Z`, merge back to `develop`.
