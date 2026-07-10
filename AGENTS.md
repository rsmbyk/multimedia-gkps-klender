# Agent guide

Project conventions for humans and coding agents. Prefer these docs over
guessing.

## Branching and releases

- **Model:** Git Flow — [`docs/GIT_FLOW.md`](docs/GIT_FLOW.md)
- **Versions (single SemVer) / changelog area labels:** [`docs/VERSIONING.md`](docs/VERSIONING.md)
- **Shipped history:** [`CHANGELOG.md`](CHANGELOG.md)
- **Production deploy:** [`docs/DEPLOY.md`](docs/DEPLOY.md)

## Testing (TDD)

- **Guide:** [`docs/TDD.md`](docs/TDD.md)
- **Python:** `pytest` / `requirements-dev.txt` / `pytest.ini`
- **JavaScript:** Vitest / `package.json` / `vitest.config.js`
- Behavior changes: failing test first, then implementation.

## Specs (SDD)

- **Guide:** [`docs/SDD.md`](docs/SDD.md) (includes Spec ID conventions)
- **Tree:** [`specs/`](specs/) (constitution, templates, per-feature specs)
- **Product overview:** [`specs/app/`](specs/app/) (`APP`) + registry in
  [`specs/README.md`](specs/README.md)
- Spec-anchored intent before code for in-scope product work; TDD still proves
  each implementation task. Cross-ref criteria as `OBS-SONGS-AC3`, etc.

## Backlog and tracker

- **Guide:** [`docs/BACKLOG.md`](docs/BACKLOG.md)
- **Board:** [`backlog/README.md`](backlog/README.md) (`BL-*` items under
  `backlog/items/`)
- Backlog is “what we might do”; specs remain intent once work is in scope.

## Cursor rules

Agent-oriented summaries live under [`.cursor/rules/`](.cursor/rules/). They
point at the docs above; the markdown in `docs/` is the source of truth.
