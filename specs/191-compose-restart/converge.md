# Converge: Stack Restart Policy

**Slice**: `specs/191-compose-restart` · **Pass 1** · **Run**: 2026-11-14

## What was checked

Every traceability row (Plan) against the code, by the method it declared:

| Row | Declared | Evidence |
| --- | --- | --- |
| FR-001 web policy | `test` | Red first: `AssertionError: None != 'unless-stopped' : web stays exited after a daemon restart without a restart policy`; after T002 the module runs `Ran 9 tests … OK`. `docker compose config` renders `restart: unless-stopped` under `web`, `db` and `media`; `docker compose config -q` accepts the file. |
| FR-002 db policy | `test` | Same test, same green run. |
| US1 scenarios 1–2 | `manual` | Executed in session: `systemctl --user restart docker-desktop.service` → first poll shows all three containers `Up 5 seconds` with no manual start; `curl /` → `200` after ~30 s of boot, `/songs/` → `200`. **Scope note, recorded honestly:** the running containers carried the policy from the 2026-11-14 out-of-band `docker update` (web/db) and from the compose file (media) — this proves the runtime mechanism; the file rows added by this slice guarantee the same policy on every future `docker compose up` recreation, which is what the test pins. |
| US2 scenario 1 | `manual` | Executed in session: `docker compose stop` (all three `Stopped`), then a second daemon restart → `web Exited (0)`, `db Exited (0)`, `media Exited (255)` — nothing started itself. The stack was then brought back (`docker compose start`, db waited for healthy, web started) and answers `200`. |
| SC-001 | `manual` | Shares US1's proof: `docker ps` three `Up`, site `200`. |

## Findings

| Row | Type | Evidence |
| --- | --- | --- |
| — | — | No `missing`, `partial`, `contradicts` or `unrequested` gaps found in pass 1. The working tree contains exactly the two FR behaviours, their test, and the spec-pack/board files the traceability table names. |

## Outcome

**Converged** at pass 1 — no accepted gaps, no extra passes needed. Fold executed (see `fold.md`):
`local-stack/R3` added; `last folded` moved to 2026-11-14; slice prepended to the capability's
slices list.
