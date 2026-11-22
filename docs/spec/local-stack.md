# local-stack

**capability**: `local-stack`
**last folded**: 2026-11-21
**slices**: `218-restart-log`, `217-entrypoint-shadowed`, `216-windows-checkout-start`, `191-compose-restart`, `182-host-font-detection`

The local Docker Compose stack on an operator's computer: what it needs from the machine it runs on,
and how it reaches the fonts that machine already has. Created by spec 182 — before it, the stack's
startup assumptions were only recorded as compose defaults.

### R1 — The stack starts on an operator's computer

The stack SHALL start on a computer that follows the documented setup, whatever the shell exports:
no value the compose file relies on may be one that some platform does not define. A source it mounts
SHALL resolve on every platform it supports, and a font directory the machine does not provide SHALL
not prevent the other services from starting. A machine that provides no font directory at all SHALL
start exactly as it does with none. (spec 182) The stack SHALL start with no `.env` at all — the
media companion's origin set is configured on the companion's own page after the start, not in the
project's environment. (spec 192)

**Scenarios**

- **Given** a Windows computer that does not export `HOME` and a checkout with `.env` filled as
  documented, **When** the stack is started, **Then** the web, database and media services start and
  the font mount resolves to a directory inside the checkout.
- **Given** a fresh checkout with no `.env` whatsoever, **When** the stack is started through the
  launcher or plain Compose, **Then** every service starts and the companion's page is where origins
  are recorded. (spec 192)
- **Given** a computer whose `~/.local/share/gkps-fonts` holds fonts from an older setup, **When** the
  stack is started through the launcher, **Then** that directory is still mounted.
- **Given** a computer with no font directory whatsoever, **When** the stack is started, **Then** the
  launcher mounts nothing extra and every service starts.

### R2 — The stack reads the fonts the computer already has

Started through the launcher, the stack SHALL mount the computer's own font directories read-only
beside the operator's directory, and the converter SHALL draw a family so mounted in that family. The
image SHALL keep shipping only free substitutes — no file from a computer's font directory SHALL be
copied into the repository or the image — and a directory the daemon cannot read SHALL be skipped and
named rather than mounted as an empty directory. (spec 182) The launcher SHALL name what it mounts —
the count and each directory's path, zero said outright — and SHALL pass each mount's on-disk source
to the companion so the page can show where the faces came from. (spec 192)

**Scenarios**

- **Given** a computer with Microsoft Office installed, **When** a deck set in `Britannic Bold` is
  converted after a launcher start, **Then** `Britannic Bold` is the family drawn.
- **Given** the same deck on a computer without that face, **When** it is converted, **Then** the
  recorded substitute is drawn, exactly as before.
- **Given** a Docker daemon that shares only part of the host filesystem, **When** the launcher runs,
  **Then** the unreadable directory is skipped with a message naming it, and a start that mounted
  nothing visible is reported rather than passing silently.
- **Given** a launcher start that mounts font directories, **When** the listing prints, **Then** the
  count and the paths are named line by line, and each path reaches the companion as a label on its
  mount. (spec 192)

### R3 — The stack returns when the daemon restarts

Every always-on service SHALL declare the `unless-stopped` restart policy: a machine or daemon
restart returns the web, database and media services without a manual start, and a stack the
operator stopped on purpose stays stopped across daemon restarts. (spec 191)

**Scenarios**

- **Given** the stack running, **When** the machine restarts and the Docker daemon comes back,
  **Then** the web, database and media services are running again and the web service answers on
  its published port with no manual step.
- **Given** the operator stopped the stack (`docker compose stop` or `down`), **When** the daemon
  restarts, **Then** no service starts itself.
- **Given** the web service starts while the database is still initialising after a restart,
  **When** its entrypoint fails, **Then** the policy retries with backoff and the stack converges
  to healthy with no manual step.

### R4 — The stack starts from a checkout made on any platform

The stack SHALL start from a checkout made on any platform it supports, whatever line endings that
checkout's git produced, and whatever the stack mounts over the working directory: the repository
SHALL pin its shell scripts to LF, the image SHALL strip `\r` from the entrypoint it runs, and that
entrypoint SHALL live outside the directory the local stack bind-mounts from the host, so a mounted
checkout cannot replace the copy the build prepared. The pin SHALL cover `*.sh` only — a PowerShell
script keeps CRLF. Because none of this depends on a launcher, a plain `docker compose up` SHALL start
as the launcher does, and a checkout made before the pin existed SHALL start without being re-cloned.
(spec 216, revised by spec 217)

**Scenarios**

- **Given** a checkout whose `docker/entrypoint.sh` carries CRLF line endings, **When** the image is
  built and the stack started, **Then** the entrypoint reaches its `exec "$@"` and the web and media
  services stay up rather than restarting.
- **Given** the `web` service, which mounts the checkout over its working directory, **When** the
  container starts, **Then** it runs the image's own entrypoint, not the mounted file, and an LF and a
  CRLF checkout behave identically.
- **Given** a checkout made with `core.autocrlf=true`, **When** the shell scripts are inspected,
  **Then** they hold LF, and `docker/up.ps1` does not.
- **Given** a checkout that predates the pin, **When** the stack is started, **Then** it starts
  anyway — the strip is a build step, not a repository state.

### R5 — A launcher start reports what it could not inspect

The launchers' post-start font check SHALL report, never abort: when the check cannot run — the
companion is not running — the launcher SHALL print one line naming the companion as not running, the
companion's own last log line when it has one, and a line naming `docker compose logs media` and
`docker compose build` as the next step, and SHALL NOT print the empty-mount message instead. The
check SHALL NOT change the exit status of the start it follows, a start that failed SHALL run no check
at all, and no log SHALL be requested unless the companion could not be reached. Both launchers SHALL
behave identically. (spec 216, revised by spec 218)

**Scenarios**

- **Given** a start that succeeded and a companion that is restarting, **When** the check runs,
  **Then** one line names the companion, its own last line follows, `docker compose build` is named,
  and the launcher exits with the status the start returned.
- **Given** a companion that never started and has no log, **When** the check runs, **Then** the log
  line is omitted and the other lines are printed.
- **Given** a companion that answers the check, **When** the launcher finishes, **Then** it requests no
  log and prints nothing extra.
- **Given** a start that succeeded and a running companion that sees no mounted font, **When** the
  check runs, **Then** the File-Sharing message is printed, unchanged.
- **Given** a start that failed, **When** the launcher finishes, **Then** no check runs and the
  failing status is what it exits with.
