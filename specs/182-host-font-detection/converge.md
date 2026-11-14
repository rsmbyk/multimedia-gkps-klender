# Converge — the computer's own fonts reach the converter

## Pass 1 — 2026-11-01

**Checked**: every row of `plan.md`'s traceability table against the code in the tree, the two new
tests, the launcher's own output on this machine, and the font behaviour inside the `media` image with
the new configuration mounted over it.

### Findings

| ID | Type | Finding | Evidence | Outcome |
| --- | --- | --- | --- | --- |
| F1 | `missing` | The launcher mounted every platform directory it could find. Docker Desktop mounts a path it cannot read as an **empty directory**, so on a Desktop install the stack would start, look healthy, and silently draw with the image's faces — FR-004's "cannot be read" was never detected. | `docker run --rm -v /usr/share/fonts:/probe:ro alpine:latest sh -c 'ls /probe \| wc -l'` → `0`, while `docker inspect` reported the bind; `docker info --format '{{.OperatingSystem}}'` → `Docker Desktop`. | Fixed. `docker/up.sh` asks the daemon what it is and skips the system directories on Desktop with a printed reason; both launchers look inside the container after a start and warn when no mounted directory showed a font; `docs/local-media-companion.md` states it. Recorded as research D010. |
| F2 | `missing` | `--print` appended the default `up -d`, so the documented inspection command ended in `unknown shorthand flag: 'd' in -d`. | `./docker/up.sh --print` on this machine. | Fixed: the print branch runs before the default command is applied, in both launchers. |
| F3 | `contradicts` | The plan said every alias becomes `binding="weak"`. Measured, a weak alias is **ignored** for a generic family: `sans-serif` stayed `Noto Sans` where the same alias with `binding="same"` answered `Noto Serif`. Making the generic aliases weak would have removed the guarantee that a generic request is never answered with a monospaced face. | `FONTCONFIG_FILE=<conf> fc-match -f '%{family}' sans-serif` for `weak`, `same` and the control. | Fixed by narrowing the rule: the ten named families are `weak`, `sans-serif` and `serif` stay `same`; both are asserted in `tests/test_slides_fonts_conf.py`, and the file's own comment says why. |
| F4 | `unrequested` | `tests/test_docker_compose.py::DockerComposePortRulesTests::test_media_companion_uses_private_loopback_port_and_named_volume` was red before this slice: it still expected `media.volumes` to hold only the named volume, which spec 166 changed. | The test failed on the untouched branch tip. | Fixed in the slice (T005): the assertion now expects the named volume first and exactly one operator mount, plus the new default test. |
| F5 | `partial` | The media image was not rebuilt on this machine; the font behaviour was verified by mounting the new `slides-fonts.conf` over the running image's copy. The Dockerfile's `RUN python -m multimedia.slide_fonts` gate therefore runs on the next build, not here. | `docker run --rm -v <new conf>:/etc/fonts/conf.d/99-gkps-slides.conf:ro … media:latest` | Accepted as evidence, with the rebuild named in the closing report as the one step this machine did not take. The mounted configuration is byte-identical to the file the build copies. |

### Rows checked by their declared method

- **test** — FR-001, FR-005, FR-007: green. `manage.py test tests.test_docker_compose tests.test_slides_fonts_conf` → 11 tests, OK.
- **inspection** — FR-003: `./docker/up.sh --print` mounted `1` directory and skipped `/usr/share/fonts`
  with the File Sharing hint. FR-004: the same run shows a skipped directory passing through instead
  of failing. FR-006: `git ls-files '*.ttf' '*.otf' '*.ttc'` empty; `Dockerfile` copies no font. FR-008:
  `font_inventory()` is still part of `renderer_identity()`. FR-009: the setup step names both
  launchers. SC-003: with the new configuration mounted, `python -m multimedia.slide_fonts` prints the
  nine mappings and `nine families resolve, none monospaced`. SC-004: no font file in the tree; the
  image's `fc-list` count unchanged. US1/AC2: `~/.local/share/fonts` is in the generated override.
  US2/AC2: without a host mount, `Calibri → Carlito` and `Britannic Bold → Noto Sans` as recorded.
  US3/AC1–AC2: the entrypoint branch is in place; the operator's directory is still mounted by the base
  file, so its absence cannot stop the start.
- **manual** — unrun on this machine, as the plan declares: FR-002, SC-001, SC-002, SC-005 and
  US1/AC1, US1/AC3, US2/AC1, US2/AC3 need a Windows computer with Office. `quickstart.md` §6 and §7 carry
  the steps.

### Outcome

Converged with one accepted partial (F5). Behaviour matched to the traceability table; the two rules
that carry the slice now fail loudly if they regress.
