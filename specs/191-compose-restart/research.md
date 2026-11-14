# Research: Stack Restart Policy

**Slice**: `specs/191-compose-restart` · **Phase 0** · **Written**: 2026-11-14

Format per rule: Decision / Rationale / Alternatives / Provenance. **Unknowns remaining: 0.**

## D001 — The policy is `unless-stopped`

**Decision**: web and db declare `restart: unless-stopped`.
**Rationale**: it restarts a container the daemon killed at shutdown, and it honours a deliberate
stop across daemon restarts — which is US2. `always` would resurrect a stack the operator stopped
on purpose; `on-failure` does not fire on a clean daemon-shutdown kill.
**Alternatives**: `always` (rejected: fights US2); `on-failure` (rejected: daemon shutdown kills
read as success or 255 without a uniform failure signal).
**Provenance**: Docker's documented restart-policy semantics; the repo's own precedent — the
`media` service has carried `unless-stopped` since spec 002's stack; observed on this machine
2026-11-13→14: after a reboot, media returned by itself while web stayed `Exited (255)` and db
only came up when started by hand (`docker inspect`, RestartPolicy and State read directly).

## D002 — The policy lives in `docker-compose.yml`, not only on the running containers

**Decision**: write `restart: unless-stopped` into the file for web and db.
**Rationale**: compose recreates containers from the file; a policy set only via
`docker update` is silently lost on the next recreation, and the machine drifts away from the
file while still looking configured.
**Alternatives**: `docker update` only (rejected: lost on recreate; this was applied out-of-band
on 2026-11-14 as the interim repair and this slice supersedes it in the file).
**Provenance**: observed on this machine — db was recreated ~9 h after the reboot and came back
with `policy=no` because the file carried none (`docker inspect`, RestartPolicy `no`).

## D003 — The requirement covers web and db only; media is already correct

**Decision**: FR-001 (web) and FR-002 (db); media keeps its existing policy unchanged.
**Rationale**: media already declares `unless-stopped` in the file and demonstrated the behaviour.
**Alternatives**: restating media's policy in the spec (rejected: duplicates an existing fact,
SDD-03's no-duplicate rule).
**Provenance**: `docker-compose.yml` line 64; `tests/test_docker_compose.py` already asserts it.

## D004 — The boot-order window is covered by retry-under-policy, not by a health-gate change

**Decision**: no change to `depends_on`; the web service's restart policy absorbs the window where
db is not yet healthy after a daemon start.
**Rationale**: `depends_on: service_healthy` orders a compose `up`; a daemon-side restart follows
the engine's dependency order without the health gate, so web may start while db initialises — its
entrypoint fails, the policy retries with backoff, and the stack converges without a manual step.
**Alternatives**: composing a health-gated dependency for daemon restarts (rejected: no compose
native mechanism; complexity without a second use).
**Provenance**: compose `depends_on` semantics; observed convergence of media after the 2026-11-13
reboot on this machine. The window is recorded as an Edge Case in the spec, and US2's manual proof
exercises the ordinary path.

## D005 — `bump: patch`

**Decision**: the slice declares `bump: patch`.
**Rationale**: a fix to the local operator stack's behaviour; the level maps from what changed
(fix → patch). Local-stack slices have taken bumps before (spec 182, a feat, took `minor`).
**Alternatives**: `none` (rejected: VER-05 reserves it for refactors/tests/internal docs; this
changes observable behaviour of the stack the team runs).
**Provenance**: repo VERSION history and spec 182's card (`bump: minor`, released 1.29.0).

## D006 — Verification: the file rows are `test`; the daemon-restart proofs are `manual`

**Decision**: FR-001/FR-002 verify through a new test in `tests/test_docker_compose.py`; the
daemon-restart and deliberate-stop proofs are manual.
**Rationale**: the file is the deployable unit and already has a YAML-parsing guard module with
PyYAML imported; the runtime behaviour needs a real daemon restart, which the Django suite cannot
perform, and a requirement may be un-tested but not un-verifiable.
**Alternatives**: driving dockerd lifecycle from a test (rejected: destroys the operator's running
stack); inspection-only for the file (rejected: a one-line mechanical guard is exactly what the
existing test module pins).
**Provenance**: `tests/test_docker_compose.py` structure (SimpleTestCase, `yaml.safe_load`,
per-concern test classes); spec 182's traceability put its compose-file row on `test` in the same
module.
