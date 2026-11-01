# Implementation Plan: the computer's own fonts reach the converter

**Spec**: `specs/182-host-font-detection/spec.md`
**Branch**: `feat/182-host-font-detection`
**Bump**: `minor`
**Preview**: `n/a — no product surface, markup or stylesheet changes; the effect is the projected deck's PDF (owner decision, 2026-11-01)`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | POSIX `sh` for macOS and Linux, PowerShell 5.1+ for Windows, Python 3.12 for the tests |
| Primary dependencies | Docker Compose v2, fontconfig and LibreOffice in the `media` image, Django's test runner |
| Storage | filesystem only — two bind mounts into the `media` container; no database change |
| Testing | `SimpleTestCase` in `tests/`; no database is touched by the new rows |
| Target platform | the operators' computers: Windows 10/11, macOS, Linux |
| Project type | local deployment stack plus renderer configuration |
| Performance goals | media start adds under 10 s on a directory of 1,000 font files (measured once, recorded) |
| Constraints | no font file enters the image or the repository; plain `docker compose up` keeps working; PowerShell 5.1 ships with Windows 10/11 |
| Scale / scope | 3 services, 2 launcher scripts, 1 fontconfig file, 1 entrypoint, docs, tests |

## Constitution Check

No `CONSTITUTION.md` exists in this repository, so there are no principles to check against (SDD-01
makes it optional and it is never auto-created). Re-checked after Phase 1: nothing to re-check.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Nine decisions, each measured on the working machine:
the compose default (D001), where detection lives (D002), the generated override (D003), the mount
point (D004), directory precedence (D005), the alias binding (D006), the per-platform directories
(D007), the cache refresh (D008), the version level (D009).

## Phase 1 — Design

- `data-model.md` — the two font sources (host directory and operator directory) as filesystem
  entities, their mounts, and the precedence between them.
- `contracts/launcher.md` — the command-line contract both launchers share: sub-command handling,
  `--print`, environment read, temp file written, exit codes.
- `quickstart.md` — the commands that demonstrate every row below, and which of them run on this
  machine today.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `docker-compose.yml` | `test` → `tests/test_docker_compose.py::DockerComposePortRulesTests::test_the_font_mount_default_needs_no_home` | the default must not name `$HOME` |
| FR-002 | `docker/up.ps1` | `manual` — on a Windows computer with Office, run `docker\up.ps1 -Print`, then `docker/up.ps1`, then `docker compose exec media fc-match "Britannic Bold"` | needs a Windows machine |
| FR-003 | `docker/up.sh` | `inspection` — `docker/up.sh --print` on this Linux machine; the generated override names `/usr/share/fonts` and, when present, `~/.local/share/fonts` | |
| FR-004 | `docker/up.sh`, `docker/up.ps1` | `inspection` — delete a directory from the candidate list and re-run `--print`: it is skipped, no mount is emitted | |
| FR-005 | `docker/slides-fonts.conf` | `test` → `tests/test_slides_fonts_conf.py::test_every_alias_yields_to_an_installed_family` | `binding="weak"` on every alias |
| FR-006 | `Dockerfile`, `.gitignore` | `inspection` — `git ls-files '*.ttf' '*.otf' '*.ttc'` is empty; `grep -n 'fonts' Dockerfile` shows only packages and the conf copy | |
| FR-007 | `docker/slides-fonts.conf` | `test` → `tests/test_slides_fonts_conf.py::test_the_operator_directory_precedes_the_host_directory` | operator first, then host |
| FR-008 | `multimedia/local_media.py` | `inspection` — `renderer_identity()` still concatenates `font_inventory()`; a mount changes it, so the derivative key changes | |
| FR-009 | `docs/local-media-companion.md` | `inspection` — the first-time setup step names `docker/up.ps1` / `docker/up.sh`, and plain compose is described as the start without host fonts | |
| SC-001 | `docker/up.sh`, `docker/up.ps1`, `docker-compose.yml` | `manual` — on each platform, with `HOME` unset: `docker/up.sh` then `curl -s -o /dev/null -w '%{http_code}' http://localhost:63404` answers `200` | |
| SC-002 | `docker/slides-fonts.conf`, `docker/up.ps1` | `manual` — on a Windows computer with Office: `fc-match "Britannic Bold"` inside the media container names it; the converted PDF embeds it | |
| SC-003 | `docker/slides-fonts.conf`, `multimedia/slide_fonts.py` | `inspection` — `docker compose exec media python -m multimedia.slide_fonts` prints the nine recorded mappings, and the build's own check ran green | |
| SC-004 | `Dockerfile`, `.gitignore` | `inspection` — `git ls-files` for font extensions is empty; `docker compose exec media fc-list \| wc -l` after a plain compose start equals the image's own count | |
| SC-005 | `docker/up.sh` | `manual` — time `docker compose up -d media` with a 1,000-file directory mounted; record the delta | |
| US1/AC1 | `docker-compose.yml`, `docker/up.ps1` | `manual` — a Windows computer without `HOME` starts all three services | |
| US1/AC2 | `docker/up.sh` | `inspection` — `docker/up.sh --print` on a machine with `~/.local/share/gkps-fonts` includes that directory | |
| US1/AC3 | the whole stack | `manual` — the home page answers `200` after the launcher's start | |
| US2/AC1 | `docker/slides-fonts.conf` | `manual` — the Office face is drawn and embedded on a machine that has it | |
| US2/AC2 | `docker/slides-fonts.conf` | `inspection` — with no host mount, `fc-match` answers the recorded substitute for each of the nine families | |
| US2/AC3 | `multimedia/local_media.py` | `manual` — convert a Calibri deck, add a font, convert again: the derivative differs and the second conversion happens | |
| US3/AC1 | `docker/entrypoint.sh` | `inspection` — the cache refresh runs for `/usr/share/fonts/operator` as before | |
| US3/AC2 | `docker-compose.yml` | `inspection` — with no `.fonts/` present, the media service still starts (the directory is created empty by the mount, as before) | |

**Verification split**: 3 test · 11 inspection · 7 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| Two launcher scripts instead of one documented `docker compose up` | the platform can only be detected on the host, and the two shells do not run each other's scripts | a single Python launcher would be simpler, but the operator computers are not guaranteed to have Python, while PowerShell ships with Windows and `sh` with macOS and Linux |

## Project Structure

### Documentation

```
specs/182-host-font-detection/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/launcher.md
  checklists/requirements.md
```

### Source

```
docker-compose.yml          the operator mount's default becomes ./.fonts
docker/up.sh                macOS and Linux launcher (POSIX sh)
docker/up.ps1               Windows launcher (PowerShell 5.1+)
docker/slides-fonts.conf    weak aliases; operator directory listed before the host one
docker/entrypoint.sh        cache refresh when either font directory exists
.env.example                GKPS_FONTS_DIR documented with its new default
.gitignore                  .fonts/ and the generated override
docs/local-media-companion.md   the launcher as the standard start; host fonts explained
tests/test_docker_compose.py    the default needs no HOME; media volumes updated
tests/test_slides_fonts_conf.py new: weak aliases; directory precedence
```

### Structure Decision

The launchers live in `docker/` beside `entrypoint.sh` and `slides-fonts.conf`, which is where the
existing container-side configuration already sits; nothing new is added at the repository root. The
tests join the existing `tests/` run, next to `test_docker_compose.py`, which already parses the
compose file for exactly this kind of rule.
