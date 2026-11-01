# Tasks: the computer's own fonts reach the converter

**Spec**: `specs/182-host-font-detection/spec.md`
**Plan**: `specs/182-host-font-detection/plan.md`
**Verification split**: 3 test · 11 inspection · 7 manual

## Phase 1 — Setup

- [X] T001 `.gitignore`: ignore `.fonts/` and the generated launcher override

## Phase 2 — Foundational

- [X] T002 `docker-compose.yml`: mount `${GKPS_FONTS_DIR:-./.fonts}` at `/usr/share/fonts/operator`, replacing the `$HOME` default

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the stack starts on a computer with no `HOME`, and the launcher mounts that platform's own
font directories.
**Independent test**: `env -u HOME docker compose config` names a path inside the checkout, and
`./docker/up.sh --print` lists this machine's font directories.

- [X] T003 [P] [US1] failing test `test_the_font_mount_default_needs_no_home` in `tests/test_docker_compose.py`
- [X] T004 [US1] make it pass: the compose default from T002 is what the test reads
- [X] T005 [P] [US1] `tests/test_docker_compose.py`: the media volumes assertion learns the font mount (it is red on `develop` today)
- [X] T006 [US1] `docker/up.sh`: POSIX launcher — detect macOS/Linux directories, write the override, pass the command through, `--print`
- [X] T007 [US1] `docker/up.ps1`: PowerShell launcher — `C:/Windows/Fonts` and the per-user directory, same contract
- [X] T008 [US1] `docs/local-media-companion.md`: the first-time setup names the launcher; plain compose is the start without host fonts (FR-009)

## Phase 4 — US2 (P1)

**Goal**: a family the computer has is drawn in that family; the substitutes are only the fallback.
**Independent test**: with Office present, `fc-match 'Britannic Bold'` inside the media container
names it; without, the mapping is unchanged.

- [X] T009 [P] [US2] failing test `test_every_alias_yields_to_an_installed_family` in new `tests/test_slides_fonts_conf.py`
- [X] T010 [P] [US2] failing test `test_the_operator_directory_precedes_the_host_directory` in the same file
- [X] T011 [US2] `docker/slides-fonts.conf`: every alias `binding="weak"`; explicit `<dir>` order — operator, then host
- [X] T012 [US2] `docker/entrypoint.sh`: refresh the font cache when either `/usr/share/fonts/operator` or `/usr/share/fonts/host` exists

## Phase 5 — US3 (P2)

**Goal**: the operator's own directory still works, and an old computer's fonts are not stranded.
**Independent test**: a font in `~/.local/share/gkps-fonts` is mounted by the launcher; a font in
`.fonts/` wins a same-family clash.

- [X] T013 [US3] `docker/up.sh` and `docker/up.ps1`: include `~/.local/share/gkps-fonts` when it exists (FR-007)
- [X] T014 [US3] `.env.example` and `docs/local-media-companion.md`: `GKPS_FONTS_DIR` with its new default, and what the folder is for

## Phase 6 — Polish

- [ ] T015 Run every `inspection` and `manual` row of the traceability table that this machine can run; record the numbers in `analysis.md`
- [ ] T016 `VERSION` → `1.26.0` and the `CHANGELOG.md` line, in the pre-merge commit
- [ ] T017 Closing report: verification split, capabilities folded, branch and commit count, PR title and body

## Phase 7 — Convergence

<!-- written by Converge only; absent until it runs -->
