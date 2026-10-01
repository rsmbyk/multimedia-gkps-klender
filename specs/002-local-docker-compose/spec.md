# Spec: Local Docker Compose stack

- **ID:** 002
- **Status:** Accepted
- **Item:** ITEM-003
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** none

## Intent

Give this project a one-command local stack so a fresh clone can run without a
hand-built Python environment or a separately installed PostgreSQL. `docker
compose up --build` starts Django and PostgreSQL, applies migrations, and serves
the app over HTTP.

`web` and `db` are published on random high host ports from the IANA dynamic
range (`49152`-`65535`) so the stack does not collide with the well-known `8000`
and `5432` that other local apps and a native Postgres commonly hold. Both ports
are overridable per clone through `.env`, without editing a tracked file. This
capability previously existed on the archived line (`v0.5.2`) and is restored
here on the current line.

## Scope

### In scope

- `docker-compose.yml`: `web` + `db` services, published host ports, optional
  `env_file`, forced local `DATABASE_URL`, `db` healthcheck.
- `Dockerfile` (Python 3.12 slim) and `docker/entrypoint.sh` (optional
  `migrate` / `collectstatic`).
- `.dockerignore` and `.env.example`.
- `README.md` quick start for the Docker path.
- `tests/test_docker_compose.py` pinning the port rules.

### Out of scope

- Production / Vercel configuration and `vercel.json`.
- CI.
- Container-internal ports (`web` `8000`, Postgres `5432`) and the in-network
  `DATABASE_URL` (`…@db:5432/…`) — unchanged.
- Auto-detecting a free port at run time. Ports are constants; `.env` overrides.
- Provisioning anything on the host beyond Docker and Compose.

## Domain rules

- **Random, not memorable.** The published host ports for `web` and `db` MUST be
  in `49152`-`65535` and MUST NOT be `8000` or `5432`.
- **Host port configurable, container port fixed.** `web` and `db` keep their
  internal ports; only the published side changes.
- **`.env` is optional.** Compose supplies safe defaults for every variable the
  app needs to boot, so a fresh clone runs with no manual copy step. When `.env`
  is present it still wins, so the documented "add your LAN IP" workflow keeps
  working.
- **Local database is forced.** Compose sets the in-network `DATABASE_URL`
  itself; a stray production URL in `.env` MUST NOT override it for the `web`
  service.
- **Collision is recoverable without tracked edits.** Setting `WEB_PORT` or
  `DB_PORT` in `.env` changes the published port.
- Docs MUST state the effective app URL and the collision escape hatch.

## Acceptance scenarios

### Scenario: stack starts on a clean clone with no `.env`

- **Given** a fresh clone with no `.env` file
- **When** running `docker compose config`
- **Then** compose resolves the project without an `env file … not found` error
- **And** `docker compose up --build` starts `db` and `web` and applies migrations

### Scenario: published ports avoid the crowded well-known range

- **Given** a machine that already runs other Compose projects and apps
- **When** inspecting the published ports of `web` and `db`
- **Then** both are in `49152`-`65535`
- **And** neither is `8000` nor `5432`
- **And** the container-side ports remain `8000` and `5432`

### Scenario: app is reachable on the published port

- **Given** a running stack
- **When** requesting `http://127.0.0.1:<WEB_PORT>/`
- **Then** Django answers (not a connection-refused error)

### Scenario: collision is recoverable without editing tracked files

- **Given** the published port is already taken by another process
- **When** setting `WEB_PORT` (or `DB_PORT`) in `.env`
- **Then** `docker compose up` binds the overridden port instead

### Scenario: existing overrides still win

- **Given** a `.env` that sets `DJANGO_ALLOWED_HOSTS` to include a LAN IP
- **When** running `docker compose up`
- **Then** that value is used rather than the compose default

### Scenario: a local database is always used

- **Given** a `.env` that sets `DATABASE_URL` to a remote URL
- **When** running `docker compose up`
- **Then** the `web` service still uses the local `db:5432` database

### Scenario: port rules stay enforced

- **Given** the compose file
- **When** running `python manage.py test tests.test_docker_compose`
- **Then** the dynamic-range and non-well-known-port assertions pass

## Traceability

- Domain/app tests: `tests/test_docker_compose.py` —
  `test_services_present`,
  `test_published_ports_avoid_well_known_range`,
  `test_container_ports_are_conventional`, and
  `test_env_example_matches_compose_defaults`. Run in-container:
  `docker compose run --rm web python manage.py test tests.test_docker_compose`.
- E2E: N/A — declared out of scope. Verified by hand instead: `docker compose
  config` resolved both with and without `.env` (defaults `63404` / `59075`),
  `docker compose up --build` served `HTTP 200` on `http://127.0.0.1:63404/`,
  and `WEB_PORT=61234 DB_PORT=61235 docker compose config` re-bound both.
- Implementation: `docker-compose.yml`, `Dockerfile`, `docker/entrypoint.sh`,
  `.dockerignore`, `.env.example`, `README.md`.

> **Verified:** 21 tests green in the built image (`tests.test_docker_compose`
> plus the `multimedia.*` app suites). E2E remains out of scope.
