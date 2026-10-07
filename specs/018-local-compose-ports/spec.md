# Spec: Local Compose ports

- **ID:** 018
- **Status:** Accepted
- **Item:** [ITEM-011](../../backlog/items/ITEM-011-local-compose-random-ports.md)
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

The local Docker Compose stack must start reliably on a machine that already
runs other apps, without editing tracked files to dodge a port conflict, and
without a manual `.env` copy step on a fresh clone.

`web` and `db` are published on random high ports chosen from the IANA dynamic
range (`49152`-`65535`) and verified free on this host, overridable per clone
via `.env`. The host-side pytest DSN and the published database port share one
source of truth so they cannot drift apart again.

## Scope

### In scope

- `docker-compose.yml` published host ports for `web` and `db`.
- Optional `env_file` so the stack runs without `.env`.
- One shared default for the host-published database port, consumed by the
  pytest bootstrap and the toolchain smoke test.
- Documentation that names the actual ports: `README.md`, `docs/TDD.md`,
  `.env.example`.
- An additive note on Accepted spec `015` recording that its `127.0.0.1:8000`
  acceptance criterion is superseded by this spec.

### Out of scope

- Container-internal ports (`8000` for `web`, `5432` for Postgres) — unchanged.
- The in-network `DATABASE_URL` (`postgresql://…@db:5432/…`) — unchanged.
- Production / Vercel configuration and `docs/DEPLOY.md`.
- `CHANGELOG.md` history entries that mention the old test port.
- Provisioning a Python 3.10/3.11 interpreter on the host. The port default is
  corrected here, but host-side `pytest` still needs a supported interpreter,
  which this machine does not have.
- The dead `grep -v '^psycopg2=='` line in the `Dockerfile`.
- Auto-detecting a free port at run time. The ports are constants in the
  compose file; `.env` is the override.

## Domain rules

- **Random, not memorable.** Published host ports are drawn from `49152`-`65535`
  (IANA dynamic/private range) and MUST NOT be `8000` or `5432`.
- **Host port is configurable, container port is not.** `web` and `db` keep
  their internal ports; only the published side changes.
- **One source of truth for the test DSN.** The default host port used by
  `conftest.py` / `multimedia/settings_test.py` is the same constant the
  compose file publishes, so pytest and the stack cannot disagree.
- **`.env` is optional.** Compose supplies safe defaults for every variable the
  app needs to boot, so a fresh clone runs without a manual copy step. When
  `.env` *is* present it still wins, so the documented "add your LAN IP to
  `DJANGO_ALLOWED_HOSTS`" workflow keeps working.
- **`TEST_DATABASE_URL` still overrides everything.** An explicit override
  (CI, SSH tunnel) takes precedence over the shared default.
- Docs MUST state the effective app URL and the escape hatch for a collision.

## Acceptance scenarios

### Scenario: stack starts on a clean clone with no `.env`

- **Given** a fresh clone with no `.env` file
- **When** running `docker compose config`
- **Then** compose resolves the project without an `env file … not found` error
- **And** running `docker compose up --build` starts `db` and `web` and
  applies migrations

### Scenario: ports avoid the crowded well-known range

- **Given** a machine that already runs other Compose projects and apps
- **When** inspecting the published ports of `web` and `db`
- **Then** both are in `49152`-`65535`
- **And** neither is `8000` nor `5432`
- **And** both are free on the host at start time

### Scenario: app is reachable on the published port

- **Given** a running stack
- **When** requesting `http://127.0.0.1:<WEB_PORT>/`
- **Then** Django answers (not a connection-refused error)

### Scenario: collision is recoverable without editing tracked files

- **Given** the published port is already taken by another process
- **When** setting `WEB_PORT` (or `DB_PORT`) in `.env`
- **Then** `docker compose up` binds the overridden port instead

### Scenario: host pytest reaches the published database

- **Given** the stack running with no `TEST_DATABASE_URL` set, and a supported
  interpreter (3.10/3.11) available
- **When** running `pytest`
- **Then** the DSN host is loopback and the port is the same value compose
  publishes — not a hardcoded literal that can drift
- **And** no SSH tunnel is required on Linux

### Scenario: existing overrides still win

- **Given** a `.env` that sets `DJANGO_ALLOWED_HOSTS` to include a LAN IP
- **When** running `docker compose up`
- **Then** that value is used rather than the compose default
- **And** the app answers on that LAN IP

### Scenario: suite stays green

- **Given** the port change
- **When** running `pytest` and `npm test`
- **Then** both suites pass

## Traceability

- Domain/app tests: `tests/test_toolchain.py` —
  `test_compose_db_port_avoids_well_known_ports` and
  `test_default_test_database_url_matches_compose_db_port` (new, encode the
  dynamic-range and single-source-of-truth domain rules) plus the existing
  `test_django_settings_test_uses_postgres`, now asserting the shared constant
  instead of the literal `5433` and honoring a `TEST_DATABASE_URL` override.
  Red first: `ImportError: cannot import name 'DEFAULT_DB_HOST_PORT'`.
- E2E: N/A — declared out of scope. Verified by hand instead: `docker compose
  config` with `.env` removed, `docker compose up -d` with no `.env` (HTTP 200
  on 63404), and a `WEB_PORT=61234` override in `.env` (binds 61234, releases
  63404, HTTP 200). Old ports 8000 / 5432 confirmed released.
- Implementation: `docker-compose.yml`, `.env.example`, `multimedia/env.py`,
  `conftest.py`, `multimedia/settings_test.py`, `tests/test_toolchain.py`,
  `README.md`, `docs/TDD.md`, `specs/015-deploy-local/`.

> **Not verified here:** the default-path branch of
> `test_django_settings_test_uses_postgres` (loopback host + published port).
> It only runs on a host with Python 3.10/3.11, and this machine has only
> 3.14.7 — see the out-of-scope note. The two new unit tests cover the
> constant's correctness independently of that.
>
> **Release-mirror side effect:** `bump: patch` moved `VERSION` to `0.5.2`, so
> `multimedia/obs/static/obs/common/version.js` and the literals in
> `version.test.js` were updated in the same PR.
