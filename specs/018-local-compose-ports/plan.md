# Plan 018: Local Compose ports

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-011](../../backlog/items/ITEM-011-local-compose-random-ports.md)
- **Bump:** patch

## Why

The local Compose stack publishes `web` on `8000` and `db` on `5432` — two of
the most contended ports on a developer machine. This host already runs other
Compose projects (`yggnet` on `39523`, `duz0-dev`, `pocket-ledger`), and a
Windows-native Postgres commonly owns `5432`. The stack currently fails to
start on a conflict with no obvious remedy short of editing the tracked
compose file.

Verification during planning also found two related defects:

1. `docker compose config` **fails outright** when `.env` is absent, because
   `env_file: - .env` is a hard requirement. `.env` is gitignored, so any fresh
   clone that skips the manual `copy .env.example .env` step cannot start the
   stack at all — even though compose already defaults `DJANGO_SECRET_KEY`, so
   `.env` is not actually required.
2. The host pytest DSN (`127.0.0.1:5433` in `conftest.py` /
   `multimedia/settings_test.py`) does **not** match the port compose actually
   publishes (`5432`). Verified: with the stack up, `5432` is the only
   Postgres listener and nothing listens on `5433`, so the documented host-side
   `pytest` workflow cannot reach the database without the Windows
   `docker-vm` SSH tunnel in `docs/TDD.md`. Note this machine is *also*
   missing a supported interpreter (only Python 3.14.7 is installed; the
   project needs 3.10/3.11 for Django 4.0.1), so host `pytest` is blocked
   twice over. This slice removes the port blocker; provisioning an
   interpreter is explicitly out of scope.

## Scope / edges

**In:**

- Publish `web` and `db` on random high ports from the IANA dynamic range
  (`49152`-`65535`), verified free on this host.
- Make both ports overridable via `.env` (`WEB_PORT`, `DB_PORT`) without
  editing the tracked compose file.
- Make `env_file: .env` optional so a fresh clone runs without a manual copy.
- Give the host-side pytest DSN and the compose published DB port **one**
  shared source of truth, so they cannot drift again.
- Update the docs that hardcode the old ports (`README.md`, `docs/TDD.md`,
  `.env.example`).
- Reconcile Accepted spec `015` (`DEPLOY-LOCAL-AC4` names `127.0.0.1:8000`)
  with the new behavior, per `specs/README.md` rule 7.

**Out:**

- Container-internal ports. `web` still listens on `8000` and Postgres on
  `5432` inside the Compose network; only the published host ports change.
- Any change to `DATABASE_URL` inside the network (`db:5432` is unchanged).
- Production / Vercel configuration.
- Automatically picking a *different* random port per machine. The ports are
  fixed constants in the compose file, overridable per clone via `.env`.
- The Windows `docker-vm` SSH-tunnel instructions, which stay valid but get
  their numbers updated.
- Provisioning a Python 3.10/3.11 interpreter on this host. The project pins
  Django 4.0.1, which predates Python 3.11 support; the host only has 3.14.7.
  Host-side `pytest` therefore stays unrunnable here regardless of ports.

## Approach

1. **`docker-compose.yml`** — publish `"${WEB_PORT:-63404}:8000"` and
   `"${DB_PORT:-59075}:5432"`. Compose reads the project `.env` for
   interpolation, so the same block also supplies a safe default when `.env`
   is missing. Add a matching `DJANGO_ALLOWED_HOSTS` default for the same
   reason (`.env` still wins, so the documented "add your LAN IP" workflow
   keeps working).
2. **`.env.example`** — document `WEB_PORT` / `DB_PORT` and the resulting app
   URL.
3. **`multimedia/env.py`** — add a side-effect-free `DEFAULT_DB_HOST_PORT` and
   `DEFAULT_TEST_DATABASE_URL`. This module is already imported by
   `conftest.py` before Django settings load, so both the root `conftest.py`
   and `multimedia/settings_test.py` can read the same constant.
4. **`tests/test_toolchain.py`** — assert against that shared constant instead
   of the literal `5433`, and skip the port assertion when an explicit
   `TEST_DATABASE_URL` override is in play (CI, tunnels).
5. **Docs** — `README.md` and `docs/TDD.md` reflect the new ports and the now
   consistent Linux path (no SSH tunnel needed).
6. **Spec 015** — add a note recording the superseded `8000` acceptance
   criterion, preserving the migrated EARS body verbatim for traceability.

## TDD

- Domain/app tests: `tests/test_toolchain.py` (existing toolchain smoke check
  — extended, not a new suite).
- E2E: N/A. Declared out of scope in the spec; the real proof is
  `docker compose up` plus an HTTP request to the published port.

## Risks

- **Stale `5433` references.** `docs/TDD.md`, `conftest.py`,
  `settings_test.py`, and the `CHANGELOG.md` history all mention the old port.
  The changelog is a historical record and is left alone; the shared constant
  plus a repo-wide re-grep is the check.
- **Port collision is still possible.** Random picks lower the odds; they do
  not eliminate them. `WEB_PORT` / `DB_PORT` in `.env` are the escape hatch,
  and that has to be obvious in the docs or the win is lost.
- **Spec 015 drift.** Rewriting migrated EARS would falsify history, so the
  change is additive: a dated note pointing at spec 018.
- **Host `pytest` still will not run here.** Aligning the DSN fixes the port
  mismatch, but without a 3.10/3.11 interpreter the suite cannot execute on
  this machine. Do not let a green port check imply a green suite.
- **Scope creep into the Dockerfile.** The `grep -v '^psycopg2=='` line in the
  `Dockerfile` is dead (requirements pin `psycopg2-binary`), but it is
  harmless. Left alone unless the build proves otherwise.
