# Project constitution

Ubiquitous constraints for this repository. Prefer linking to the detailed docs
over duplicating them here. Agents and humans must treat these as always-on.

## Process

- THE project SHALL follow Spec-Driven Development for in-scope product work as
  defined in [`docs/SDD.md`](../docs/SDD.md).
- THE project SHALL use Test-Driven Development for product behavior changes as
  defined in [`docs/TDD.md`](../docs/TDD.md).
- THE project SHALL use Git Flow and pull requests as defined in
  [`docs/GIT_FLOW.md`](../docs/GIT_FLOW.md).
- THE project SHALL use a single SemVer and changelog area labels as defined in
  [`docs/VERSIONING.md`](../docs/VERSIONING.md). Feature PRs into `develop`
  SHALL NOT bump SemVer; they SHALL add `## Unreleased` bullets when warranted.

## Production and local runtime

- Production hosting and Vercel constraints SHALL follow
  [`docs/DEPLOY.md`](../docs/DEPLOY.md). Do not “simplify” legacy `vercel.json`
  routing without a tested plan.
- Local app runtime expectations (Compose / Postgres / env) SHALL follow the
  deploy and Docker docs already in the repo; do not reintroduce host-only app
  runtimes that contradict those docs.

## Dependencies and scope

- Prefer the existing stack (Django, pytest, Vitest, current OBS/static
  patterns). THE agent SHALL ask before adding large or uncommon libraries.
- Specs SHALL state out-of-scope items explicitly so agents do not invent
  adjacent features.

## Specs as source of intent

- WHEN product behavior changes, THE corresponding spec under `specs/` SHALL be
  created or updated in the same change (or an explicit note why no spec
  applies).
- IF implementation and the agreed spec disagree, THEN the spec SHALL be
  clarified or updated before treating the code as correct.
- Specs SHALL use stable Spec IDs (`CODE`, `CODE-US*`, `CODE-AC*`, `CODE-T*`)
  as defined in [`docs/SDD.md`](../docs/SDD.md#spec-ids); new capabilities
  SHALL be registered in [`specs/README.md`](README.md) and
  [`specs/app/spec.md`](app/spec.md).
