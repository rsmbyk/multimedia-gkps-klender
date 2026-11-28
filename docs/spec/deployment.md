# deployment

**capability**: `deployment`
**last folded**: 2026-11-28
**slices**: `251-cloudrun-csrf-origin`

How a deployed instance interprets the requests its platform forwards to Django. Created by spec 251 —
before it, the TLS boundary was recorded in operations notes but not as product behaviour.

### R1 — A forwarded HTTPS request is secure

Django SHALL treat a request whose trusted proxy header says `https` as secure, so that a same-origin
HTTPS write reaches its view instead of failing the CSRF origin check. A request without that header
SHALL keep the WSGI scheme and the existing CSRF behaviour. (spec 251)

**Scenarios**

- **Given** a Cloud Run request carrying `X-Forwarded-Proto: https` and a valid CSRF cookie/token,
  **When** a same-origin HTTPS POST reaches a write endpoint, **Then** the origin check accepts it and
  the view runs.
- **Given** the same request on either the production or the staging service, **When** a nonexistent
  record is POSTed to its delete endpoint, **Then** the answer is 404 from the view, not a 403 from
  CSRF.
- **Given** no forwarded header (the local Compose server over http), **When** a POST carries an HTTPS
  Origin, **Then** it is still rejected — the fix is a proxy-header decision, not a CSRF exemption.
