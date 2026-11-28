# Research: Cloud Run writes pass CSRF

## Decision / Rationale / Alternatives / Provenance

### D001 — Fix the scheme decision at its source

- **Decision**: set `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")` in
  `multimedia/settings.py`.
- **Rationale**: Django 4.0's `HttpRequest.is_secure()` reads that setting; without it a TLS-terminating
  proxy makes every request look like http, so `CsrfViewMiddleware._origin_verified()` compares the
  browser's `https://host` against `http://host`. The same wrong scheme also affects absolute URLs the
  app builds.
- **Alternatives**: (a) `CSRF_TRUSTED_ORIGINS` with the two fixed live hostnames — fixes the symptom but
  leaves every generated URL http and needs editing per deployment; (b) exempting endpoints from CSRF
  — removes a security control and was rejected outright; (c) terminating TLS in gunicorn — new
  certificates and a new failure mode for a one-line problem.
- **Provenance**: Django 4.0 source (`django/http/request.py:scheme`, `django/middleware/csrf.py:_origin_verified`) and the live probes recorded in the spec.

### D002 — Regression test as a CSRF-only request

- **Decision**: `tests/test_cloudrun_csrf.py` uses a tiny view behind the real `CsrfViewMiddleware`, a
  real CSRF cookie/token, and a Cloud Run-shaped WSGI request (Host without port, `SERVER_PORT=8080`,
  `X-Forwarded-Proto: https`, HTTPS `Origin`).
- **Rationale**: it exercises the exact failing layer with no database and no writes. A negative case
  overrides the setting to `None` and asserts 403, so the test cannot pass by disabling CSRF.
- **Alternatives**: an E2E test against staging needs a deployment and would write data; a pure unit
  test of `is_secure()` would miss the middleware's origin check.
- **Provenance**: `tests/` convention (cross-cutting tests live at the repo root), TDD-01/TDD-02.

### D003 — Bump

- **Decision**: `patch`, applied in the delivery commit as the grammar requires.
- **Rationale**: a broken write path is restored; no new capability, no incompatible change.
- **Alternatives**: `none` would leave a user-visible fix unrecorded; `minor` would overstate it.
- **Provenance**: VER-10, C-SDD-VER.

### D004 — Capability fold

- **Decision**: create `docs/spec/deployment.md` with `R1`, rather than folding into `local-stack` or
  `routing`.
- **Rationale**: the requirement is about how deployed instances interpret proxy requests; neither
  existing capability owns deployment transport.
- **Alternatives**: `local-stack/R5` describes the wrong host class; `routing/R<n>` describes URL
  redirects, not TLS termination.
- **Provenance**: SDD-03 (a capability is one durable behaviour area), existing `docs/spec/` files.

**Unknowns remaining: 0.**
