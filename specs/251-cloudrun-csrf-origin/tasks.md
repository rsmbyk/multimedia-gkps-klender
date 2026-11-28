# Tasks: Cloud Run writes pass CSRF

**Spec**: `specs/251-cloudrun-csrf-origin/spec.md`
**Plan**: `specs/251-cloudrun-csrf-origin/plan.md`
**Verification split**: `3 test · 2 inspection · 1 manual`

## Phase 1 — Setup

- [x] T001 [Setup] Branch cut at the change request; no further setup (C-SDD-GIT).

## Phase 2 — Foundational

- [x] T002 [Foundational] No new dependency, migration or interface.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: a same-origin HTTPS POST from behind Cloud Run passes CSRF and reaches its view.
**Independent test**: a Cloud Run-shaped request gets 200 on the probe view, 403 without the setting.

- [x] T003 [US1] Write the failing test `CloudRunCsrfTests.test_a_forwarded_https_request_is_accepted` in `tests/test_cloudrun_csrf.py`: real CSRF middleware, Cloud Run host, `X-Forwarded-Proto: https`, HTTPS `Origin`; assert 200. Red today (403).
- [x] T004 [US1] Write `CloudRunCsrfTests.test_without_the_proxy_header_the_https_origin_is_rejected` in the same module: with `SECURE_PROXY_SSL_HEADER=None`, assert 403 — the guard against turning CSRF off.
- [x] T005 [US1] Make T003 pass by setting `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")` in `multimedia/settings.py`, with a comment naming Cloud Run.
- [x] T006 [US1] `test` — run `tests.test_cloudrun_csrf` red before T005 and green after; record both outputs.

## Phase 4 — Polish

- [x] T007 [Polish] `inspection` — `git diff --stat` confirms the code change is settings + tests + docs only (FR-003).
- [x] T008 [Polish] Fold: add `docs/spec/deployment.md` with `R1` and `fold.md` naming the delta.
- [x] T009 [Polish] First commit at Fold: spec pack, code, test, capability, card `ITEM-268` and its board row.
- [ ] T010 [Polish] Delivery after a separate owner word: PR draft → ready, card `In review` with `pr:`, then pre-merge `VERSION` → `1.37.9`, changelog Fixed line and card `Done` in the same PR.
- [ ] T011 [Polish] `manual` — after deployment, re-run the live probe on both hosts: 404, not 403 (SC-002).
