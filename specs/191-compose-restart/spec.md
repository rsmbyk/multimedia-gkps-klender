# Feature Specification: Stack Restart Policy

**Slice**: `specs/191-compose-restart`
**Branch**: `feat/191-compose-restart`
**Created**: 2026-11-14
**Status**: Draft
**Input**: "the docker compose of the project does not start on system restart. can you fix that?"

## User Scenarios & Testing

### US1 — The stack returns after a machine restart (P1)

**Why this priority**: The stack is the operator's local instance of the app; today every machine
restart leaves the database and web containers exited until someone starts them by hand, so the
first person to open the site after a reboot finds it down.

**Independent Test**: With the stack running, restart the Docker daemon (machine reboot, or a
Docker Desktop restart), and observe every service running again and the site answering on the
published web port with no manual start.

**Acceptance scenarios**

1. **Given** the stack is running, **When** the machine restarts and the Docker daemon comes back,
   **Then** the web, database and media services are running again without a manual start, and the
   web service answers on its published port.
2. **Given** the web service was killed by the daemon shutdown, **When** the daemon comes back,
   **Then** the web service returns on its own restart policy, not by a manual start.

### US2 — A deliberately stopped stack stays stopped (P2)

**Why this priority**: The policy must not fight the operator: a stack stopped on purpose
(maintenance, port conflict, machine handover) must not resurrect itself on the next daemon start.

**Independent Test**: Stop the stack (`docker compose stop`), restart the Docker daemon, and
observe every service still stopped.

**Acceptance scenarios**

1. **Given** the operator stopped the stack with `docker compose stop` (or `down`), **When** the
   Docker daemon restarts, **Then** no service starts itself.

### Edge Cases

- **When** the web service starts while the database is still initialising after a restart,
  **Then** the web service fails, its restart policy retries with backoff, and the stack converges
  to healthy once the database is ready — no manual step.
- **When** a single service crashes while the machine keeps running, **Then** that service is
  restarted by its own policy.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The `web` service SHALL declare the `unless-stopped` restart policy in `docker-compose.yml`. | `local-stack/R3` |
| FR-002 | The `db` service SHALL declare the `unless-stopped` restart policy in `docker-compose.yml`. | `local-stack/R3` |

### Key Entities

None — the change is compose configuration; no models, no stored state.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | After a daemon restart, the whole stack is serving with no manual step | `docker ps` shows web, db and media `Up`, and the site answers on the published web port |

## UI/UX

`n/a — compose configuration only; no visible surface changes.`

## Assumptions

- `unless-stopped` over `always` — the `media` service already carries `unless-stopped`, and it
  honours a deliberate stop across daemon restarts (US2); `always` would restart a stack the
  operator stopped on purpose.
- The policies are written in `docker-compose.yml`, not set only on the running containers — the
  file is what a future `docker compose up` recreates from; a policy applied only via
  `docker update` is lost on the next recreation.
- The `media` service keeps its existing policy unchanged.
- The machine's Docker daemon itself starts on boot (Docker Desktop's user service is enabled);
  this slice only makes the containers return with it.
- The stack's start order at daemon restart is the engine's (`db` before `web`); the web service's
  retry-under-policy covers the window where the database is not yet healthy.

## Clarifications

### Session 2026-11-14

- No questions asked; no `[NEEDS CLARIFICATION]` markers remain.
- The owner chose the route through the process: a normal slice, the spec presented at Gate 1.
