# Agent guide

Project conventions for humans and coding agents. Prefer these docs over
guessing.

## Branching and releases

- **Model:** Git Flow — [`docs/GIT_FLOW.md`](docs/GIT_FLOW.md)
- **Versions (single SemVer) / changelog area labels:** [`docs/VERSIONING.md`](docs/VERSIONING.md)
- **Shipped history:** [`CHANGELOG.md`](CHANGELOG.md)

## Testing (TDD)

- **Guide:** [`docs/TDD.md`](docs/TDD.md)
- **Python:** `pytest` / `requirements-dev.txt` / `pytest.ini`
- **JavaScript:** Vitest / `package.json` / `vitest.config.js`
- Behavior changes: failing test first, then implementation.

## Cursor rules

Agent-oriented summaries live under [`.cursor/rules/`](.cursor/rules/). They
point at the docs above; the markdown in `docs/` is the source of truth.
