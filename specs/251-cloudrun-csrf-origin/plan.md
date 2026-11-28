# Implementation Plan: Cloud Run writes pass CSRF

**Spec**: `specs/251-cloudrun-csrf-origin/spec.md` (Accepted, Gate 1 2026-11-28)
**Branch**: `fix/251-cloudrun-csrf-origin`
**Bump**: `patch` (D003; shown at Gate 2)
**Preview**: `n/a — one server setting; no product surface, markup or stylesheet changes`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0.1 |
| Primary dependencies | none new |
| Existing patterns | cross-cutting tests at `tests/`; `multimedia/settings.py` already loads deployment values through `config()` |
| Storage | none |
| Testing | new `tests/test_cloudrun_csrf.py`; `SimpleTestCase` with the real CSRF middleware, no DB |
| Target platform | Cloud Run (`@vercel/python` retired from the live path); local Compose over http |
| Project type | Django server-rendered web app + REST API |
| Performance goals | unchanged |
| Constraints | no endpoint, model, template or static file changes; no CSRF exemption; nothing pushed without a separate owner word |
| Scale / scope | 1 setting, 1 new test module, 1 new capability file, 1 card |

## Constitution Check

No `CONSTITUTION.md` in this repository — nothing to check (SDD-01). Re-checked after Phase 1:
unchanged.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Four decisions: source fix (D001), test shape (D002),
bump (D003), capability (D004).

## Phase 1 — Design

- `data-model.md` — `n/a — no stored state`.
- `contracts/none.md` — explicitly none: the write endpoints and request bodies do not change.
- `quickstart.md` — the exact red→green commands and the live probe.

### Design notes

- The setting names one header and one value, so a request without the proxy header keeps the WSGI
  scheme. It is not a global "always secure" switch.
- The comment in `settings.py` names Cloud Run, because the next reader must know which proxy makes
  the header trustworthy.
- The negative test overrides the new setting to `None`; without that case a test could pass by
  turning CSRF off.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 (proxy https is secure) | `multimedia/settings.py` | `test` → `tests.test_cloudrun_csrf.CloudRunCsrfTests.test_a_forwarded_https_request_is_accepted` | Cloud Run-shaped request, real middleware |
| FR-002 (HTTPS Origin reaches the view) | `tests/test_cloudrun_csrf.py` | `test` → the same test | 403 before the fix, 200 after |
| FR-003 (configuration only) | slice diff | `inspection` — `git diff --stat` names only `multimedia/settings.py`, tests and docs | no endpoint/template/static edits |
| SC-001 (local red→green) | `tests/test_cloudrun_csrf.py` | `test` → both methods in the module | negative case pins 403 without the setting |
| SC-002 (both deployments) | live hosts | `manual` — after redeploy, the nonexistent-PK probe answers 404 on both | cannot be run before a deploy |
| SC-003 (local HTTP unchanged) | `tests/test_cloudrun_csrf.py` | `test` → `…::test_without_the_proxy_header_the_https_origin_is_rejected` | proves CSRF is still enforced |
| US1/AC1–2 | settings + probe | `test` + `manual` | as above |
| US1/AC3 (plain HTTP) | settings | `inspection` — no forwarded header means `scheme` comes from WSGI | |

**Verification split**: `3 test · 2 inspection · 1 manual`.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/251-cloudrun-csrf-origin/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  analysis.md  converge.md  fold.md
  contracts/none.md  checklists/requirements.md
```

### Source

```
multimedia/settings.py                 (SECURE_PROXY_SSL_HEADER)
tests/test_cloudrun_csrf.py            (new red/green regression)
docs/spec/deployment.md                (new capability, R1)
backlog/board.md, backlog/items/ITEM-268-cloudrun-csrf-origin.md
CHANGELOG.md, VERSION                  (delivery commit)
```

### Structure Decision

The regression joins the root `tests/` package beside the other cross-cutting configuration tests;
the capability gets its own file rather than overloading `local-stack`, whose scope is one operator's
computer.
