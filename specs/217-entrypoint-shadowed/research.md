# Research: the runtime entrypoint survives the bind mount

**Spec**: `specs/217-entrypoint-shadowed/spec.md`
**Unknowns remaining**: 0

## D001 — The runtime entrypoint moves to `/usr/local/bin`, outside the mounted tree

- **Decision**: `COPY docker/entrypoint.sh /usr/local/bin/gkps-entrypoint.sh`, strip and `chmod` that
  copy in the same `RUN`, and `ENTRYPOINT ["/bin/sh", "/usr/local/bin/gkps-entrypoint.sh"]`.
- **Rationale**: measured on the image spec 216 produced — no mount, exit 0; the checkout mounted at
  `/app`, `docker/entrypoint.sh: 2: set: Illegal option -`, exit 2. The image's copy held 0 CR bytes
  and the mounted tree's held 19, so the mount, not the build, decided what ran. A path outside `/app`
  is the only place compose cannot overwrite.
- **Alternatives considered**: `ENTRYPOINT ["/bin/sh", "-c", "sed -i 's/\\r$//' docker/entrypoint.sh; exec /bin/sh docker/entrypoint.sh \"$@\"", "--"]`
  — rejected: it rewrites the operator's working tree from inside the container on every start, and
  turns a readable script into an inline string; removing the `.:/app` bind mount — rejected: it is
  what makes local Django reload and is the documented development setup; `dos2unix` in a launcher —
  rejected: the launcher is optional (`local-stack/R1`), and the container must start from plain
  `docker compose up` too.
- **Provenance**: research (measured both shapes on the built image).

## D002 — The entrypoint's contents do not change

- **Decision**: `docker/entrypoint.sh` keeps its contents and its place in the repository; only the
  image's copy and the `ENTRYPOINT` line change.
- **Rationale**: the file is what an operator reads to know how the container starts, and the commands
  it runs — migrations, `collectstatic`, the font-cache refresh, `exec "$@"` — are behaviour spec 216
  verified. Moving the file would move the command order with it.
- **Alternatives considered**: inlining the three commands into `ENTRYPOINT` — rejected: the same
  commands written twice (once per service) and unreadable in the repository.
- **Provenance**: research.

## D003 — The stale-image trap is filed, not built here

- **Decision**: `docker\up.ps1`'s `up -d` reusing an image older than the `Dockerfile` becomes
  `ITEM-233`, not a requirement of this slice.
- **Rationale**: the operator is blocked on a wrong path, and a launcher warning needs image
  timestamps, compose's generated image names and a two-shell implementation — a second behaviour
  riding on a fix that has to land now. `ITEM-233` carries the observation and the acceptance sketch.
- **Alternatives considered**: `up -d --build` by default — rejected: it puts a full build (LibreOffice
  install) in front of every start, including the ones that changed nothing.
- **Provenance**: `owner decision` — the operator chose to split it.

## D004 — Bump: `patch`

- **Decision**: `1.36.2` → `1.36.3`.
- **Rationale**: a fix that corrects a landed fix; no capability is added for an operator who had a
  working stack (`VER-10`).
- **Alternatives considered**: none — a correction of a defect is `patch` under every reading.
- **Provenance**: research (`VERSION` at `1.36.2` on `develop` @ `0198a3c8`).

## D005 — Verification: the bind-mount shape is a command, not an inspection

- **Decision**: SC-001 is proven by running the built image with the CRLF checkout mounted at `/app`;
  the `Dockerfile`'s own rules are unit-tested; no PowerShell is involved, so nothing is
  inspection-only that was not already.
- **Rationale**: the defect was invisible to every test spec 216 wrote because none of them ran the
  container the way compose does. The new test module asserts the path relationship, and the manual
  row asserts the runtime shape — the pair that would have caught this.
- **Alternatives considered**: a compose-level test — rejected: it would take the port bindings of the
  running stack and a full build per run.
- **Provenance**: research.

## Open

<!-- empty — Phase 0 finished -->