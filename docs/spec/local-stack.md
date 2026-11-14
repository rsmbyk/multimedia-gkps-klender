# local-stack

**capability**: `local-stack`
**last folded**: 2026-11-14
**slices**: `191-compose-restart`, `182-host-font-detection`

The local Docker Compose stack on an operator's computer: what it needs from the machine it runs on,
and how it reaches the fonts that machine already has. Created by spec 182 — before it, the stack's
startup assumptions were only recorded as compose defaults.

### R1 — The stack starts on an operator's computer

The stack SHALL start on a computer that follows the documented setup, whatever the shell exports:
no value the compose file relies on may be one that some platform does not define. A source it mounts
SHALL resolve on every platform it supports, and a font directory the machine does not provide SHALL
not prevent the other services from starting. A machine that provides no font directory at all SHALL
start exactly as it does with none. (spec 182)

**Scenarios**

- **Given** a Windows computer that does not export `HOME` and a checkout with `.env` filled as
  documented, **When** the stack is started, **Then** the web, database and media services start and
  the font mount resolves to a directory inside the checkout.
- **Given** a computer whose `~/.local/share/gkps-fonts` holds fonts from an older setup, **When** the
  stack is started through the launcher, **Then** that directory is still mounted.
- **Given** a computer with no font directory whatsoever, **When** the stack is started, **Then** the
  launcher mounts nothing extra and every service starts.

### R2 — The stack reads the fonts the computer already has

Started through the launcher, the stack SHALL mount the computer's own font directories read-only
beside the operator's directory, and the converter SHALL draw a family so mounted in that family. The
image SHALL keep shipping only free substitutes — no file from a computer's font directory SHALL be
copied into the repository or the image — and a directory the daemon cannot read SHALL be skipped and
named rather than mounted as an empty directory. (spec 182)

**Scenarios**

- **Given** a computer with Microsoft Office installed, **When** a deck set in `Britannic Bold` is
  converted after a launcher start, **Then** `Britannic Bold` is the family drawn.
- **Given** the same deck on a computer without that face, **When** it is converted, **Then** the
  recorded substitute is drawn, exactly as before.
- **Given** a Docker daemon that shares only part of the host filesystem, **When** the launcher runs,
  **Then** the unreadable directory is skipped with a message naming it, and a start that mounted
  nothing visible is reported rather than passing silently.

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
