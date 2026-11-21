# Feature Specification: The runtime entrypoint survives the bind mount

**Slice**: `specs/217-entrypoint-shadowed`
**Branch**: `fix/217-entrypoint-shadowed`
**Created**: 2026-11-21
**Status**: Draft
**Input**: "i tried it and it still does not work … the media and web are not running. also the media still showing docker/entrypoint.sh: 2: set: Illegal option -"

## User Scenarios & Testing

### US1 — A CRLF checkout starts both services (P1)

**Why this priority**: Spec 216 stripped `docker/entrypoint.sh` inside the image, but the `web`
service bind-mounts the checkout over `/app` (`docker-compose.yml:25`), so the file that actually runs
is the host's — still CRLF. Measured: the image alone runs (`OK`, exit 0); the same image with the
checkout mounted prints `docker/entrypoint.sh: 2: set: Illegal option -` and exits 2. The previous
slice's fix therefore cannot work for `web` on any checkout, whatever the build does.

**Independent Test**: Run the built image with the checkout bind-mounted at `/app`, the way the `web`
service runs it, and observe the entrypoint reach its command rather than dying at `set -e`.

**Acceptance scenarios**

1. **Given** an image built from a CRLF checkout, **When** it is run with that checkout mounted at
   `/app`, **Then** the entrypoint runs to `exec "$@"` and the command executes.
2. **Given** the same image and the same mount, **When** `web` starts, **Then** it stays up and serves,
   rather than restarting.
3. **Given** a checkout whose `docker/entrypoint.sh` has already been normalised to LF, **When** the
   stack starts, **Then** nothing changes — the same entrypoint runs.

### Edge Cases

- **When** no bind mount is present (a plain `docker run`, or `media`'s own service), **Then** the
  entrypoint still resolves and runs.
- **When** the checkout is on Linux, **Then** the image's copy and the host's file are both LF and the
  change is invisible.
- **When** the entrypoint's path inside the container is inspected, **Then** it is outside the
  directory the local stack mounts, so no mount can replace it.
- **When** the entrypoint runs, **Then** the commands it executes and their order are unchanged from
  spec 216 — migrations, `collectstatic` and the font-cache refresh are untouched.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The image SHALL run its entrypoint from a path outside `/app`, the directory `docker-compose.yml` bind-mounts from the host, so a mounted checkout cannot replace the entrypoint the build prepared. | `local-stack/R4` |
| FR-002 | The image SHALL strip `\r` from that copy before making it executable, so a CRLF build context cannot produce an entrypoint `/bin/sh` refuses. | `local-stack/R4` |
| FR-003 | The `Dockerfile`'s `ENTRYPOINT` SHALL name that path, and no file inside the mounted tree SHALL be required for the container to start. | `local-stack/R4` |
| FR-004 | `media` (no bind mount) and `web` (bind-mounted) SHALL both start from a CRLF checkout. | `local-stack/R4` |

### Key Entities

None — the change is a `Dockerfile` copy path and its `ENTRYPOINT`. No models, no stored state.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The bind-mounted shape runs | The built image run with `-v <crlf-checkout>:/app` reaches its command and exits 0 (today: exit 2, `set: Illegal option -`) |
| SC-002 | The entrypoint is outside the mount | The image's `ENTRYPOINT` path does not begin `/app/`, asserted from the `Dockerfile` and from the running container |
| SC-003 | Both services start from a CRLF checkout | `docker compose build && docker compose up -d` with a CRLF `docker/entrypoint.sh`; `docker ps` shows `web` and `media` `Up` |

## UI/UX

`n/a — the slice changes the image's entrypoint path; no product surface, markup or stylesheet changes.`

## Assumptions

- The bind mount is the cause for `web`, and it is measured rather than inferred: the same image
  passes without the mount and fails with it.
- `media` failed on the operator's machine for the other reason — `up -d` reused an image built before
  spec 216 — which is an operator step (`docker compose build`), not a defect this slice can fix in
  code. Filed separately as `ITEM-233` so the trap is recorded rather than quietly relied on.
- The entrypoint keeps its contents; only its path in the image and the `ENTRYPOINT` line change, so
  the commands it runs are untouched.
- `/usr/local/bin` is outside `/app` in every image this repository builds and is already on the
  image's `PATH`, so the path needs no further setup.
- The copy in the image is made from the build context's `docker/entrypoint.sh`, which is what the
  `.gitattributes` pin and the strip both serve; keeping the file in the repository is what lets an
  operator read what runs.

## Clarifications

### Session 2026-11-21

- Q: Does the stale-image case (`up -d` reusing an image built before a `Dockerfile` change) belong in
  this slice? → A: no — filed as `ITEM-233`; this slice fixes the shadowing only, so a blocked operator
  is not waiting on a launcher feature.

- Gate 1 taken as accepted 2026-11-21: after the requirement was explained, the owner reported from
the machine that `media` started with `--build` and `web` still fails — the diagnosis this spec is
built on, confirmed by the failing service.

No `[NEEDS CLARIFICATION]` markers remain.
