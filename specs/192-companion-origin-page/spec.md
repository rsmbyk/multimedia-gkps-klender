# Feature Specification: The companion's page manages this computer's origins

**Slice**: `specs/192-companion-origin-page`
**Branch**: `feat/192-companion-origin-page`
**Created**: 2026-11-14
**Status**: Draft
**Input**: "can you make the up.ps1 or up.sh to be some kind of a setup shell …" — withdrawn 2026-11-14 (see Clarifications) — and: "how about you make a page in media server to configure the list of origin. so, when executing the up.ps1/sh, it does not need to know the MULTIMEDIA_GKPS_KLENDER_PRODUCTION_ORIGIN. the operator can just open the configuration page and add/edit/delete origins. also, they can see the font directories detected on the machine"

## User Scenarios & Testing

### US1 — The companion serves its own configuration page on this computer (P1)

**Why this priority**: The origins a projector computer accepts are that computer's own
configuration; today they are frozen into compose at start from an `.env` variable, which is why a
first start on a new computer fails at an interpolation error. The companion is already the local
service, and its own loopback origin never needs the allowlist — so the page is reachable from the
first second of a first-ever start.

**Independent Test**: Start the stack on a fresh checkout with no `.env` at all; open
`http://127.0.0.1:63174/`; the page renders with the empty recorded list, the read-only
always-allowed local origins, and the font directories the converter sees.

**Acceptance scenarios**

1. **Given** the stack running with no `.env`, **When** the operator opens
   `http://127.0.0.1:63174/`, **Then** the page renders: the recorded origins (empty on first run,
   said outright), the always-allowed local origins, and the font directories the converter sees.
2. **Given** a computer whose recorded set was configured earlier, **When** the page is opened,
   **Then** the recorded origins are read from the companion's volume — no `.env` variable is
   involved anywhere.
3. **Given** the page open at any time, **When** the recorded set is empty, **Then** the page itself
   still works: its own origin never needs the allowlist.

### US2 — The operator adds, edits and deletes recorded origins on the page (P2)

**Why this priority**: The deployments this computer projects from — production, staging — are
known by hand; the list must be reworkable in place, by the same means, on the machine that owns it.

**Independent Test**: Add an origin with a trailing slash (the rule is named under the form), add
two valid origins, edit one, delete one, reload the page — the edited set persists.

**Acceptance scenarios**

1. **Given** the add form, **When** an entry that breaks a rule is submitted (spaces, missing or
   unsupported scheme, credentials, a path or trailing slash, missing hostname, a malformed port),
   **Then** the first broken rule is named under the form and nothing is recorded.
2. **Given** a valid origin in the add form, **When** it is submitted, **Then** it joins the
   recorded list in submission order.
3. **Given** an origin already recorded, **When** it is submitted again — as an add or as an edit of
   another row — **Then** it is refused as already recorded.
4. **Given** a recorded row, **When** Edit is used, **Then** the row becomes an input validated by
   the same rules, with Save and Cancel; **When** Delete is used, **Then** the row is removed and
   the list renumbers.
5. **Given** a reworked set, **When** the companion is restarted or the machine reboots, **Then**
   the recorded set survives — it is stored in the companion's volume.

### US3 — Only the recorded origins may use the companion, and a refusal names the page (P2)

**Why this priority**: The allowlist is the companion's security boundary; moving it from
startup-frozen `.env` to runtime state must not loosen it, and an operator whose origin is not yet
recorded must be told where to record it instead of finding the helper silently unreachable.

**Independent Test**: With only staging recorded, a request bearing the production origin is
refused with 403 and a message naming the page; a request bearing a recorded origin succeeds; the
local web app works with nothing recorded at all.

**Acceptance scenarios**

1. **Given** the recorded set (possibly empty), **When** any request reaches the companion, **Then**
   it is allowed exactly when its origin is one of the compose-provided local seeds or a recorded
   origin — checked per request, so a page change takes effect without a restart.
2. **Given** a request from an origin outside that set, **When** it is refused, **Then** the 403
   names the configuration page (`http://127.0.0.1:63174/`) as the place to record it, and no CORS
   headers are sent.
3. **Given** the local seeds only (nothing recorded), **When** the local web app at
   `http://localhost:63404` or `http://127.0.0.1:63404` uses the companion, **Then** it works —
   today's behaviour, preserved without any configuration.
4. **Given** the web app's media picker finding the companion unreachable, **When** the refusal
   payload carries a reason, **Then** the picker surfaces that reason instead of the generic
   unavailable text.

### US4 — The launcher starts the stack without any origin configuration (P3)

**Why this priority**: With the origins on the page, the start has nothing to ask; the compose
guard that made `.env` mandatory disappears, and a fresh clone starts with no copy and no prompt.

**Independent Test**: On a fresh checkout with no `.env`: plain `docker compose up -d` starts all
three services; `docker\up.ps1` starts the same stack with fonts; neither prints an origin prompt.

**Acceptance scenarios**

1. **Given** either launcher, **When** the stack starts, **Then** no origin is resolved, prompted
   or displayed — the launcher's only setup output is the font listing.
2. **Given** plain `docker compose up` with no `.env`, **When** compose runs, **Then** every service
   starts — the `:?` interpolation guard is gone.
3. **Given** a computer whose `.env` still carries the old origin variable, **When** the stack
   starts, **Then** the line is ignored without error — documented as dead.

### US5 — The page shows the font directories the converter sees (P3)

**Why this priority**: The silent-empty-mount failure class (slice 182) is invisible from outside
the container; the companion can answer what actually mounted, which is truer than any start-time
guess — and it is the same page the operator already opens for the origins.

**Independent Test**: On a computer with fonts mounted, the page lists the directories under
`/usr/share/fonts/host` and the operator's directory with the family count of each; on a computer
with none, it says so outright.

**Acceptance scenarios**

1. **Given** font directories mounted by the launcher, **When** the page is opened, **Then** each
   mounted directory is listed with its family count.
2. **Given** the operator's `.fonts/` directory holding files, **When** the page is opened, **Then**
   it is listed with its own count.
3. **Given** no font directory found, **When** the page is opened, **Then** it says no font
   directory was found, outright.

### Edge Cases

- **When** the page's own origin requests the companion, **Then** no allowlist entry is consulted —
  same-origin management always works.
- **When** a request carries a Host header other than the companion's loopback forms, **Then** it is
  refused as today; when it carries no `Origin` header at all, **Then** only a top-level navigation
  to the page itself is served.
- **When** an add or edit is padded with spaces, **Then** it is trimmed before validation.
- **When** deleting the last recorded origin, **Then** the list is empty and said outright — the
  local seeds remain allowed.
- **When** `docker compose down -v` removes the volumes, **Then** the recorded origins go with the
  library — documented in the companion's doc page.
- **When** the web app cannot reach the companion at all, **Then** its unavailable state is
  unchanged from today.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The companion SHALL serve its configuration page at `/` on its loopback origin (`http://127.0.0.1:63174` and `http://localhost:63174`), reachable in every start mode and regardless of the recorded set; the page shows the recorded origins numbered one per line, the always-allowed local origins read-only, and the font directories the converter sees (FR-005). | `media-library/R5` |
| FR-002 | The page SHALL add, edit and delete recorded origins: each entry validated as an exact origin — `http://` or `https://` scheme, no whitespace, no credentials (`@`), no path, query or fragment, a hostname present, a numeric in-range port when present — with the first broken rule named under the form; a duplicate refused; a deletion renumbering the list; and the recorded set SHALL persist in the companion's volume, surviving companion restarts, daemon restarts and machine reboots. | `media-library/R5` |
| FR-003 | The companion SHALL enforce the allowlist per request as the union of the compose-provided local seeds and the recorded set; a request outside it SHALL be refused with 403, without CORS headers, and its payload SHALL name the configuration page as the place to record an origin. | `media-library/R5` |
| FR-004 | The page's own endpoints SHALL accept only requests whose Host is one of the companion's loopback forms and whose `Origin`, when present, is the companion's own origin; the media session token SHALL NOT be required for them — the page is itself loopback-only. | `media-library/R5` |
| FR-005 | The page SHALL list the font directories the companion sees — the mounted host directories and the operator's directory, each with its family count — and SHALL say outright when none is found. | `media-library/R5` |
| FR-006 | The launchers SHALL start the stack without resolving any origin variable — no prompt, no display — and `docker-compose.yml` SHALL interpolate only the fixed local seeds (`http://localhost:<WEB_PORT>`, `http://127.0.0.1:<WEB_PORT>`) into `GKPS_MEDIA_ALLOWED_ORIGINS`: the `:?` guard is removed, and the operator variable `GKPS_MEDIA_PRODUCTION_ORIGIN` is removed everywhere it appears today (compose, `.env.example`, README, `docs/local-media-companion.md`, `docs/ARCHITECTURE.md`, `tests/test_docker_compose.py`) with no occurrence left. | `local-stack/R1` |
| FR-007 | Started through either launcher, the start output SHALL name every font directory the launcher mounts — the count line followed by each path on its own indented line, the count equal to the number of paths — and SHALL say outright that no font directory was found when none is. A directory the daemon cannot read stays named as skipped with its reason, as published (spec 182). | `local-stack/R2` |
| FR-008 | The web app's media-picker unavailable state SHALL surface the companion's refusal message when the refusal payload carries one, instead of the generic unavailable text. | `media-library/R5` |

### Key Entities

- **The recorded origin set** — an ordered, unique list of exact origins, stored in the companion's
  volume beside its library (`index.sqlite3`); read at start, mutated by the page, persisted across
  restarts; removed with the volume.
- **The local seeds** — the compose-interpolated localhost origins, read-only everywhere, never
  editable from the page.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A fresh computer needs no `.env` to reach a working setup | Fresh checkout, no `.env`: the stack starts, the page renders empty, one added production origin makes the production site's media picker reach the companion |
| SC-002 | The recorded set outlives restarts | `docker compose restart media` and a daemon restart: the page and the enforcement carry the same set |
| SC-003 | The boundary holds and explains itself | A request from an unrecorded origin: 403, no CORS headers, payload naming the page; a recorded origin passes; the local seeds pass with nothing recorded |
| SC-004 | Every stored origin is exact | Each recorded value passes the companion's `parse_allowed_origins` unchanged |
| SC-005 | The page shows the truth about fonts | The listed directories equal the mounts the converter sees, counts agreeing, or the none-found line |
| SC-006 | No origin configuration exists at start | Repo-wide: no occurrence of `GKPS_MEDIA_PRODUCTION_ORIGIN`; fresh no-`.env` start via plain compose and via both launchers, no origin prompt anywhere |
| SC-007 | The launcher still names what it mounts | The start transcript names every mounted font directory — count and paths agreeing — or carries the none-found line |

## UI/UX

**Static preview** at `specs/192-companion-origin-page/preview/index.html` — the page itself,
functional: add, edit, delete, validation, duplicates, renumbering, persistence in the browser; the
terminal walk-through of the withdrawn launcher design is kept beside it at
`preview/terminal.html`. The page wears the product's own design system — `tokens.css` and
`fonts.css` linked from `static/styles/design/`, the editor's field vocabulary (38px fields, 9px
radius, `--rail-bg` ground, focus ring, `--danger` invalid), quiet inline-SVG icon actions, the
spec-086 sheet treatment, and the dark review theme. The page's copy is fixed verbatim so Converge
can diff the served page against it:

**Page heading**:

```text
Media companion — this computer
served at http://127.0.0.1:63174 — this computer only (loopback)
```

**Section — origins**:

```text
Origins this computer accepts
```

**Empty state** (nothing recorded):

```text
no origins recorded yet — add the production site's origin below; until then only this page and
the always-allowed local origins may use the companion
```

**Recorded rows** — numbered, one per line, each with `Edit` and `Delete`; an edit turns the row
into the editor field with `Confirm` (solid) and `Discard` (outlined); a pointer press outside the
editing row discards the edit:

```text
1. https://multimedia.example.org      [Edit] [Delete]
2. https://staging.multimedia.example.org   [Edit] [Delete]
```

**Add form** — input plus `Add`; the example origin is the placeholder:

```text
[https://multimedia.example.org____________] [Add]
```

**Form errors** — the first broken rule, named under the form; no position prefix:

```text
an origin is one line with no spaces
an origin starts with its scheme — http:// or https://
an origin carries no credentials — no @
an origin carries no path, query or trailing slash
an origin needs a hostname after the scheme
an origin needs a numeric port in range
that origin is already recorded
```

**Section — local seeds** (read-only):

```text
Always allowed on this computer
http://localhost:63404
http://127.0.0.1:63404
(compose seeds — read-only)
```

**Section — fonts**:

```text
Font directories the converter sees
/usr/share/fonts/host/1 — mounted from C:/Windows/Fonts — 214 families
/usr/share/fonts/operator — mounted from .fonts/ — 2 families
```

**Fonts empty state**:

```text
no font directory found on this computer
```

## Assumptions

- The operator-supplied env variable is removed entirely, not kept as an optional seed — one
  configuration surface, the page. The rename revision dies with the variable; a laptop configured
  under the old design carries a dead `.env` line, documented as ignored.
- The local origins stay compose-pinned seeds, read-only on the page — today's zero-config local
  behaviour preserved, and the page manages only the remote set.
- The recorded set lives in the companion's volume beside `index.sqlite3` (the storage shape — JSON
  file or table — is a Plan decision).
- The launcher keeps its font-listing start output (start-time truth about what mounted) beside the
  page's companion-side fonts view; they answer different moments and both stay.
- The page is dependency-free — server-rendered HTML with vanilla script, matching the product's
  no-framework convention — and is served loopback-only, as the companion already is.
- One slice: page + runtime enforcement + compose/launcher simplification + fonts view belong
  together; they fold into `media-library` (new R5) and `local-stack` (R1 and R2 modifications).
- The docs rewritten in the same slice: README first-time section and
  `docs/local-media-companion.md` steps 2–3 become "start the stack, open the page"; the volume-
  removal note gains the recorded origins.
- The docs' statement that the allowlist comes from a required `.env` value (also
  `docs/ARCHITECTURE.md`) is rewritten for the runtime model.

## Clarifications

### Session 2026-11-14

- The launcher-prompt design (revisions recorded below) is **withdrawn** at the owner's direction:
  the origins move to a configuration page served by the media companion, and the launcher no
  longer knows any origin variable. What survives from that design: the exact-origin validation
  grammar (now the page form's), the font listing in the start output (FR-007), and the numbered
  display form (now the page's list). The record below stays for the trail.
- Q: (gate-1 revision) which variable does the launcher prompt for? → A: the operator-supplied
  production-origin variable, renamed `GKPS_MEDIA_PRODUCTION_ORIGIN` →
  `MULTIMEDIA_GKPS_KLENDER_PRODUCTION_ORIGIN` everywhere it appears. *(Withdrawn with the prompt
  design — no operator variable remains.)*
- Q: can the operator input several origins — e.g. the staging environment? → A: yes; the set is
  stored as a list. *(Now: the page's recorded set.)*
- Q: can the start also show the font directories found on the computer? → A: yes (kept — FR-007;
  the page adds the companion's own view, FR-005).
- Q: (gate-1 revision) can the input be one origin at a time, with what is recorded shown cleanly?
  → A: yes. *(Withdrawn with the prompt design.)*
- Q: (gate-1 revision) is the list displayed always, fresh or configured? → A: yes. *(Withdrawn
  with the prompt design.)*
- Q: (gate-1 revision) can a recorded origin be edited or deleted? → A: yes. *(Now: on the page —
  FR-002.)*
- Q: (direction change) can the origins be configured on a page in the media server instead, so the
  launchers need no origin variable, with the fonts visible there too? → A: yes — this
  specification. The page is served by the companion on its loopback origin, so it needs no
  allowlist entry itself; enforcement becomes per-request over the local seeds plus the recorded
  set (FR-001–FR-005).
- No `[NEEDS CLARIFICATION]` markers remain.
- The route through the process: a normal slice; the withdrawn design and this page design were
  both presented at Gate 1; the page design is the live one.
