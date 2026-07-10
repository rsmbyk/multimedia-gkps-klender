# Test-Driven Development (TDD)

This project uses **TDD** for behavior changes: write a failing test first, then
implement the smallest change that makes it pass, then refactor.

CI is **not** wired yet. Run the suites locally (and later in PRs by hand) until
GitHub Actions is added.

## Workflow

1. **Red** — add or change a test that describes the desired behavior; run it and
   confirm it fails for the right reason.
2. **Green** — implement just enough production code to pass.
3. **Refactor** — clean up while keeping tests green.

Apply this for Django/API work and for OBS / web static JavaScript. Pure docs or
tooling-only chores may skip tests when no product behavior changes.

## Python (Django / API)

| Piece | Location |
|-------|----------|
| Dev dependencies | `requirements-dev.txt` (includes `requirements.txt`) |
| Config | `pytest.ini`, root `conftest.py`, `multimedia/settings_test.py` |
| App tests | `multimedia/<app>/tests.py` or `multimedia/<app>/tests/` |
| Shared / toolchain tests | `tests/` |

### Setup

Use **Python 3.10 or 3.11** (Django 4.0.1). Prefer 3.11.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

The **app** runs in Docker Compose with local Postgres. Pytest runs on the
**host** and loads `multimedia.settings_test`, which reuses normal settings but
forces an **in-memory SQLite** database for test isolation only. `conftest.py`
supplies dummy `DJANGO_SECRET_KEY` / `DATABASE_URL` so settings import succeeds
before that override.

### Commands

```powershell
pytest                  # full suite + coverage summary
pytest -k name          # focused run
pytest --no-cov         # skip coverage when iterating quickly
```

Coverage defaults (see `pytest.ini`):

- Measured package: `multimedia`
- Terminal missing lines + `coverage-python.xml`

### Markers

- `@pytest.mark.unit` — fast, no external services
- `@pytest.mark.integration` — database or HTTP stack

## JavaScript (OBS docks, project sources, web static)

Frontend code is mostly ES modules under `static/` and app `static/` trees.
There is no production bundler; Vitest is **dev-only**.

| Piece | Location |
|-------|----------|
| Package manifest | `package.json` |
| Config | `vitest.config.js` |
| Colocated tests | `*.test.js` next to the module under test |
| Shared / toolchain tests | `tests/js/` |

### Setup

Requires **Node.js 20+** (LTS recommended).

```powershell
npm install
```

### Commands

```powershell
npm test                # single run
npm run test:watch      # watch mode (TDD loop)
npm run test:coverage   # coverage under coverage-js/
```

Path aliases (for imports in tests):

| Alias | Resolves to |
|-------|-------------|
| `@helpers` | `static/helpers` |
| `@obs` | `multimedia/obs/static/obs` |
| `@web` | `multimedia/web/static/web` |

Environment: **jsdom** (DOM APIs available). Vendored libraries under
`static/libs/` are excluded from coverage.

Many OBS modules expect globals such as `rxjs` from UMD script tags. When a
module under test needs those, provide them in the test file (or a small
`tests/js/setup.js` later) before importing the module.

## What to test (when we start writing cases)

Prefer behavior over implementation details:

- Django models, serializers, API permissions, and view contracts
- Pure helpers in `static/helpers/`
- OBS dock / source logic that can be isolated (state, hotkey mapping, BC
  message shapes) without a full OBS browser source

Defer brittle full-page UI snapshots until we have a clear need.

## Agent expectations

See [`.cursor/rules/tdd.mdc`](../.cursor/rules/tdd.mdc). For product behavior
changes, agents should follow red → green → refactor and leave the suite
passing.
