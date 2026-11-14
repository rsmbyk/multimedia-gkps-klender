# Feature Specification: the computer's own fonts reach the converter

**Slice**: `specs/182-host-font-detection`
**Branch**: `feat/182-host-font-detection`
**Created**: 2026-11-01
**Status**: Accepted
**Input**: "i tried running the docker compose inside the repo on another laptop. but, it says 'The HOME variable is not set'. what am i supposed to fill it with?" — followed by "i cant guarantee me (and the other operators) can do that in every laptops/computers. cant you just detect it from the operating systems (as you mentioned, checking the C:\Windows\fonts, for example) and get the fonts from there? you can even get the other fonts available from the host machine"

## User Scenarios & Testing

### US1 — The stack starts on an operator's computer (P1)

**Why this priority**: the stack is the product's local half. A computer that cannot start it cannot
project, and today a Windows computer that follows the setup instructions still fails on the font
mount, because `HOME` is not an environment variable there.

**Independent Test**: on each platform, with `.env` filled as documented and no `HOME` exported,
`docker compose up -d` leaves `web`, `db` and `media` running, and `http://localhost:<WEB_PORT>`
answers 200.

**Acceptance scenarios**

1. **Given** a Windows computer with no `HOME` variable and no `GKPS_FONTS_DIR`, **When** the stack is
   started, **Then** all three services start and the media service's font mount points at a
   directory inside the checkout.
2. **Given** a Linux or macOS computer where `HOME` is exported, **When** the stack is started the same
   way, **Then** every service starts and a font placed in the old home-directory folder is still read.
3. **Given** a running stack, **When** the app's home page is requested, **Then** it answers 200 — the
   stack is up, not merely started.

### US2 — The converter draws the faces the computer already has (P1)

**Why this priority**: fidelity is what this surface exists for. Without this story the change only
removes a startup failure and still forces a hand-copied folder on every computer.

**Independent Test**: on a computer with Office installed, converting a deck set in `Britannic Bold`
draws it in `Britannic Bold`; on a computer without it, the recorded substitute is used.

**Acceptance scenarios**

1. **Given** a Windows computer with Office installed and the stack started by the launcher, **When**
   a deck set in an Office-only face is converted, **Then** that family is the one the converter
   draws, and the face is embedded in the PDF.
2. **Given** a computer without those faces, **When** the same deck is converted, **Then** the mapped
   substitutes are used exactly as they are today.
3. **Given** a computer that has `Calibri`, **When** a deck set in `Calibri` is converted, **Then** the
   real Calibri is drawn rather than Carlito, and a deck converted earlier is converted again because
   the renderer's font inventory changed.

### US3 — An operator can still add a face by hand (P2)

**Why this priority**: a face can be neither installed on the machine nor shipped in the image, and
the existing folder is the only route for it.

**Independent Test**: a font file dropped into the operator's directory is available to the converter
after the companion restarts, and its absence changes nothing.

**Acceptance scenarios**

1. **Given** a font file in `GKPS_FONTS_DIR`, **When** the companion starts, **Then** the family is
   available to the converter and the renderer identity changes.
2. **Given** no such directory, **When** the companion starts, **Then** it starts as it does today and
   the substitute faces are used.

### Edge Cases

- **When** a platform font directory exists but cannot be read, **Then** the launcher skips it and the
  stack still starts.
- **When** a family is installed both on the computer and in the image, **Then** the computer's is the
  one drawn.
- **When** the same family sits in both the operator's directory and the computer's font directory,
  **Then** the operator's copy is the one drawn: placing a file there is deliberate.
- **When** the computer's user name contains a space, **Then** the mount still resolves.
- **When** the stack is started with plain `docker compose up`, **Then** it starts and converts with
  the image's own faces, exactly as today.
- **When** the computer has no font directory at all, **Then** the launcher passes no font mount and
  the stack starts.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | With `GKPS_FONTS_DIR` unset and `HOME` unset, the media service's font mount SHALL resolve to a directory inside the checkout rather than to an absolute path built from an empty variable. | `new: local-stack` |
| FR-002 | A Windows launcher SHALL mount `C:/Windows/Fonts`, and `%LOCALAPPDATA%\Microsoft\Windows\Fonts` when it exists, read-only into the media service, and then start the stack. | `new: local-stack` |
| FR-003 | A macOS/Linux launcher SHALL mount that platform's system font directories, and any existing user font directory, read-only into the media service, and then start the stack. | `new: local-stack` |
| FR-004 | Both launchers SHALL pass the stack through unchanged when a directory does not exist or cannot be read, so a machine without fonts starts exactly as it does today. | `new: local-stack` |
| FR-005 | The converter SHALL draw a family the computer has in that family, and SHALL use the recorded substitute only when the family is absent. | `media-library/R2` |
| FR-006 | The image SHALL keep shipping only the free substitutes; no file from a computer's font directory SHALL be copied into the repository or the image. | `media-library/R4` |
| FR-007 | The operator's directory SHALL remain a source, re-scanned when the companion starts; a font left in `~/.local/share/gkps-fonts` on a computer that has one SHALL still be read; and when a family exists both there and on the computer, the operator's copy SHALL be the one drawn. | `media-library/R4` |
| FR-008 | The renderer identity SHALL keep covering the font inventory, so a host face that becomes visible produces a new derivative on the next request. | `media-library/R3` |
| FR-009 | The setup documentation SHALL name the launcher as the standard start command, and plain `docker compose up` as the start that omits the computer's fonts. | `new: local-stack` |

The startup behaviour is a new capability, `local-stack`; the drawing changes modify `media-library/R2`
and `media-library/R4`.

### Key Entities

- **Host font source** — a directory on the operator's computer, mounted read-only at
  `/usr/share/fonts/host`; identity is its platform path; lifecycle: detected by the launcher at
  start, absent when plain `docker compose up` is used.
- **Operator font directory** — `GKPS_FONTS_DIR`, defaulting to `.fonts/` inside the checkout,
  mounted read-only at `/usr/share/fonts/operator`; kept for faces that are neither installed nor
  shipped.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Every platform's documented start command brings the whole stack up on a computer that does not export `HOME` | `docker compose up -d` then `curl -s -o /dev/null -w '%{http_code}' http://localhost:63404` answers `200`, and three containers are running |
| SC-002 | A deck set in an Office-only face is drawn in that face when the computer has it | inside the media container, `fc-match 'Britannic Bold'` names `Britannic Bold`, and the derivative's embedded fonts name it too |
| SC-003 | A computer without those faces renders exactly as today | `python -m multimedia.slide_fonts` prints the nine recorded mappings and the build's check passes |
| SC-004 | No font file enters the repository or the image | `git ls-files '*.ttf' '*.otf' '*.ttc'` is empty, and the image's own `fc-list` is unchanged by the slice |
| SC-005 | Starting the media service does not become slow on a rich font directory | the added start time is measured once on a 1,000-file directory and recorded in `plan.md`; the target is under 10 s |

## UI/UX

`n/a — the slice changes the local stack's environment and the renderer's font resolution; no product
surface, markup or stylesheet is touched.` The visible output it changes is the projected deck's PDF,
whose comparison is recorded in the slice's verification rather than a preview page. The owner
confirmed the `n/a` on 2026-11-01.

## Assumptions

- The launcher is additive: plain `docker compose up` keeps working unchanged, without host fonts,
  while the setup documentation names the launcher as the standard start — nobody's existing command
  may break, and a computer without the script must still be runnable.
- The default `GKPS_FONTS_DIR` moves from under `$HOME` to `.fonts/` inside the checkout, because a
  default cannot name a variable the computer may not have; existing computers keep their fonts
  because the launcher mounts `~/.local/share/gkps-fonts` when it exists.
- Only system-wide font directories are mounted by default; per-user directories are added when the
  launcher finds them.
- Windows operators have PowerShell 5.1 or newer, which Windows 10 and 11 ship — no extra install.
- The operator's directory remains the place for faces that are neither installed on the computer nor
  shipped in the image.
- The version level is declared at Plan, not here.

## Clarifications

### Session 2026-11-01

- Q: Does the startup behaviour belong in a new `local-stack` capability, or as a fifth requirement of
  `media-library`? → A: A new `local-stack` for startup and the host mount; `media-library` takes the
  font-drawing changes.
- Q: When a family exists in both the operator's directory and the computer's font directory, which
  one is drawn? → A: The operator's copy — placing a file there is deliberate.
- Q: Does the converted deck's appearance require a preview page, or does the recorded render
  comparison stand in? → A: `n/a` — no product surface changes.
- Q: Should the setup documentation name the launcher as the start command? → A: Yes; plain
  `docker compose up` is documented as the start without the computer's fonts.
