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

The **app** runs in Docker Compose with local Postgres. Pytest also runs on the
**host** and loads `multimedia.settings_test`, which reuses normal settings then
**forces** Compose Postgres and **ignores** any Neon/production `DATABASE_URL`
in `.env`. pytest-django creates a separate `test_*` database so the live
Compose `multimedia` database is not wiped.

Default test DSN: `postgresql://multimedia:multimedia@127.0.0.1:59075/multimedia`
(override with `TEST_DATABASE_URL`). Port **59075** is the same high random port
`docker-compose.yml` publishes for `db` — it lives in the IANA dynamic range so
it is unlikely to collide with a local Postgres or another app. The value is a
single constant, `multimedia.env.DEFAULT_DB_HOST_PORT`, shared with the compose
file so the two cannot drift apart. If you changed `DB_PORT` in `.env`, set
`TEST_DATABASE_URL` to match.

On this machine the VirtualBox `docker-vm` NAT only forwards SSH (`2222`), so
when running the stack inside that VM you still need an SSH local forward to
reach guest Postgres on the host:

```powershell
# Start Compose DB inside docker-vm (if not already up)
C:\Users\Javan\docker-compose.cmd -f C:\Users\Javan\projects\multimedia-gkps-klender\docker-compose.yml up -d db

# Forward guest :5432 to the published port (once per session)
ssh -f -N -L 59075:127.0.0.1:5432 docker-vm
```

> **Caveat:** the project pins Django 4.0.1 and needs **Python 3.10/3.11** on
> the host. A host without one of those cannot run `pytest` at all, whatever the
> port. If `py -3.11` is missing, install it (or use `uv python install 3.11`)
> before blaming the port.

### Commands

```powershell
pytest                  # full suite + coverage summary (needs Postgres)
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

Many OBS modules expect globals such as `rxjs` from UMD script tags.
`tests/js/setup.js` installs the `rxjs` npm package onto `globalThis.rxjs` for
Vitest. Path alias `/static/helpers` mirrors browser absolute imports.

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
