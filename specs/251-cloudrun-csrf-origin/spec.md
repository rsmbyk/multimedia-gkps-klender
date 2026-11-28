# Feature Specification: Cloud Run writes pass CSRF

**Slice**: `specs/251-cloudrun-csrf-origin`
**Branch**: `fix/251-cloudrun-csrf-origin`
**Created**: 2026-11-28
**Status**: Accepted (Gate 1, 2026-11-28 — the owner read the diagnosis and the proposed fix, then said "proceed")
**Input**: "can you check why i cant do any add/edit/delete on the production and staging server?" followed by "proceed"

## User Scenarios & Testing

### US1 — A same-origin HTTPS write reaches its view (P1)

**Why this priority**: Both live sites moved to Cloud Run on 27 November. Cloud Run terminates TLS, so
Django sees plain HTTP. With no `SECURE_PROXY_SSL_HEADER`, `request.is_secure()` is false and the CSRF
origin check expects `http://<host>` while the browser sends `https://<host>`. Every add, edit and
delete POST is rejected before its view runs; reading is unaffected.

Measured on both live services: `GET /editor/songbook/new/` → 200 with a CSRF cookie; POST to a
nonexistent delete PK with `Origin: https://<live host>` → **403 CSRF verification failed**; the same
POST with `Origin: http://<live host>` → **404** (the view ran and found no record).

**Independent Test**: A POST with a valid cookie/token and a genuine HTTPS Origin reaches the view —
for a nonexistent record it answers 404, never 403.

**Acceptance scenarios**

1. **Given** a Cloud Run request bearing `X-Forwarded-Proto: https` and a same-origin HTTPS `Origin`,
   **When** a write endpoint is POSTed, **Then** CSRF accepts it and the view runs.
2. **Given** the same request on production and on staging, **When** each is probed with a nonexistent
   delete PK, **Then** both answer 404 rather than 403 after deployment.
3. **Given** the local Compose site over plain HTTP, **When** a write is POSTed, **Then** its behaviour
   is unchanged (the header is absent and the scheme stays http).

### Edge Cases

- **When** no `Origin` header is present on an HTTPS request, **Then** Django's stricter Referer check
  applies, as before.
- **When** an `X-Forwarded-Proto` value other than `https` arrives, **Then** the request is treated as
  http, so a browser's HTTPS Origin still cannot pass by spoofing an unrelated value.
- **When** a request is made directly to gunicorn without a proxy, **Then** no forwarded header is
  present and the scheme remains the WSGI one.
- **When** the token itself is wrong or missing, **Then** the request is still rejected; this slice
  changes only the scheme decision, not token validation.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | Django SHALL treat a request whose trusted proxy header says `https` as secure, so an HTTPS `Origin` matching the request host is accepted. | `deployment/R1` |
| FR-002 | A same-origin HTTPS POST to any write endpoint SHALL pass the CSRF origin check and reach its view. | `deployment/R1` |
| FR-003 | The change SHALL be configuration only: no model, template, static asset, URL or editor endpoint changes. | `deployment/R1` |

### Key Entities

None — one Django setting and one regression test module. No stored state.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A Cloud Run-shaped POST is accepted | Local simulation: 403 before the fix, 200 after, with `Origin: https://<host>` and `X-Forwarded-Proto: https` |
| SC-002 | Both deployments accept writes | After redeploy, the nonexistent-PK probe answers 404 on both live hosts, not 403 |
| SC-003 | Local HTTP writes are unchanged | `tests.test_cloudrun_csrf` asserts the fix is a proxy-header setting, not a CSRF bypass |

## UI/UX

`n/a — the slice changes one server setting; no product surface, markup or stylesheet changes.`

## Assumptions

- Cloud Run sets `X-Forwarded-Proto` on every request and overwrites client-supplied values, so the
  header can be trusted as a proxy signal. The setting is scoped to that header/value pair only.
- `ALLOWED_HOSTS=*` remains as deployed; the origin check still requires the Origin host to match the
  request's host.
- The Vercel aliases now answer 402 Payment Required, so the Cloud Run services are the live sites.
- The fix must be deployed to both `develop`→staging and `main`→production; a settings change alone
  cannot repair a running revision.

## Clarifications

### Session 2026-11-28

- Q: Does "proceed" authorize gate 1 for this fix? → A: yes — the diagnosis, the proposed one-line
  setting and the verification command were on screen; the word accepted that fix. No other stage was
  authorized: the branch stays unpushed until a separate word.

No `[NEEDS CLARIFICATION]` markers remain.
