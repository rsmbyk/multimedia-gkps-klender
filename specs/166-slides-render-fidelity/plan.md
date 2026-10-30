# Implementation Plan: a converted deck keeps the deck's own layout

**Spec**: `specs/166-slides-render-fidelity/spec.md`
**Branch**: `fix/166-slides-render-fidelity`
**Bump**: `patch` — 1.23.2 → 1.23.3 (a fix: the projection shows what the deck shows; no new command,
no new screen, nothing an operator can do that they could not do before)
**Preview**: `specs/166-slides-render-fidelity/preview/index.html` — static, opened directly

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 (the companion), Dockerfile, fontconfig XML, shell (entrypoint), compose |
| Primary dependencies | three Debian font packages added (`fonts-crosextra-carlito`, `fonts-crosextra-caladea`, `fonts-noto-core`); no Python dependency added |
| Base image | `python:3.12-slim-bookworm` → `python:3.12-slim-trixie` (LibreOffice 7.4.7.2 → 25.2.3.2) |
| Storage | none added: the derivative directory and its naming are unchanged except for the key's inputs |
| Testing | `multimedia/test_local_media.py` (Django `TestCase`); the font guard's pure function gets its own cases |
| Target platform | the media companion's Linux container; the web container shares the image and is unaffected |
| Project type | server-rendered Django app plus a loopback companion; no build step |
| Performance goals | one `libreoffice --version` and one `fc-list` per process, memoized; no change to conversion time, memory ceiling (2 GB) or file ceiling (400 MB) |
| Constraints | the conversion command, its timeout, its private profile and its process-group kill are untouched; the HTTP surface is frozen by `contracts/http.md`; the library's identity and deadlines are untouched; no deck enters the repository |
| Scale / scope | 1 Dockerfile, 1 new fontconfig file, 1 new 60-line module, ~15 lines in `local_media.py`, 1 compose volume, 3 lines in the entrypoint, ~6 new test cases, 1 changelog line |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check does not apply. The
Constraints row stands in its place.

Re-checked after Phase 1: **pass** — no new request, no new stored entity, no dependency the project
does not already ship, and the one interface it touches (the companion's routes) is frozen by
`contracts/http.md`.

## Phase 0 — Research

See [`research.md`](research.md). Eight decisions, each measured on the reported deck: the base-image
move (D001), the font set and the explicit mapping (D002), leaving the conversion command alone (D003),
the derivative identity (D004), the operator's font directory (D005), the build guard (D006), the
test split (D007), and keeping the deck out of the repository (D008). **Unknowns remaining: 0.**

## Phase 1 — Design

- [`data-model.md`](data-model.md) — the derivative's path and key, the three parts of the converter
  identity and their invariants, the font mapping's location, and the operator's directory.
- [`contracts/http.md`](contracts/http.md) — the companion's routes, statuses and headers frozen; the
  one new environment variable; `convert_slides`' signature kept because the tests pass through it.
- [`quickstart.md`](quickstart.md) — the `fc-match` inspection inside the image, the version floor,
  converting the reported deck, the named test cases, and the two things that cannot be run here.

### The design

**1. The image.** `python:3.12-slim-trixie`; `fonts-liberation` stays, and `fonts-crosextra-carlito`,
`fonts-crosextra-caladea` and `fonts-noto-core` join it. `docker/slides-fonts.conf` is copied to
`/etc/fonts/conf.d/99-gkps-slides.conf` and names every family the decks use — Calibri and Calibri Light
to Carlito, Cambria to Caladea, Arial to Liberation Sans, Arial Narrow to Liberation Sans Narrow, Times
New Roman to Liberation Serif, Courier New to Liberation Mono, and the two Office display faces to Noto
Sans Bold until the operator supplies them.

**2. The guard.** `multimedia/slide_fonts.py` holds `mapping()` (each family the decks use, resolved
through `fc-match`), `violations(mapping)` (the pairs where a proportional request answered a monospaced
face) and a `main()` that exits non-zero on any violation. The Dockerfile runs it after `COPY . .`, so an
image whose mapping regressed never finishes building.

**3. The identity.** `local_media.converter_identity(version)` returns
`version ⏎ CONVERTER_REVISION ⏎ font_inventory`, and `slide_pdf()` hashes that where it used to hash the
version. `font_inventory()` reads `fc-list : family` before each conversion; if `fc-list` is missing the
inventory is empty and the version still keys the derivative.

**4. The operator's fonts.** Compose mounts `${GKPS_FONTS_DIR:-$HOME/.local/share/gkps-fonts}` at
`/usr/share/fonts/operator`, read-only; `docker/entrypoint.sh` runs `fc-cache -f` when that directory
exists. Nothing in Python reads it — fontconfig does, and the identity notices.

## Traceability

| Requirement | Component | Verified by |
| --- | --- | --- |
| FR-001 families resolve proportionally | `docker/slides-fonts.conf`, `Dockerfile` | inspection — `quickstart.md` §1, inside the built image |
| FR-002 LibreOffice 25.2 or newer | `Dockerfile` | inspection — `quickstart.md` §2 |
| FR-003 identity covers version and fonts | `local_media.converter_identity`, `font_inventory` | test — `test_converter_identity_changes_when_the_fonts_change`, `test_converter_version_changes_cache_key` |
| FR-004 operator font directory | `docker-compose.yml`, `docker/entrypoint.sh` | inspection — mount a TTF into the directory, restart, watch the identity change (`quickstart.md` §1 notes) |
| FR-005 build fails on a monospaced fallback | `multimedia/slide_fonts.py`, `Dockerfile` | test — `test_a_monospaced_answer_is_a_violation`, and inspection of a build |
| FR-006 nothing else changes | whole diff | test — `manage.py test multimedia`; manual — the projector's media screens |
| SC-001 words within 1 pt | the image | manual — `quickstart.md` §3 against the preview |
| SC-002 title ink 477 × 199 at (95, 90) | the image | manual — the same |
| SC-003 band holds 5 words, amounts at x 475.45 / 785.56 | the image | manual — the same |
| SC-004 the build refuses a mono mapping | `slide_fonts.violations` | test — the violation case above, plus a built image |
| SC-005 a changed font or version re-renders | `slide_pdf` | test — the two identity cases |
| SC-006 suite green, assertions unchanged | `multimedia/test_local_media.py` | test — the module |
| US1 AC1–AC4 | image + identity | inspection and manual, as SC-001…SC-003 |
| US2 AC1–AC4 | `slide_pdf` | test — the identity cases and the two unchanged cache cases |
| US3 AC1–AC3 | compose + entrypoint | inspection — mount, restart, convert |

Verification split: **6 test · 3 inspection · 3 manual** (SC-001…SC-003 are the manual rows; FR-001,
FR-002 and FR-004 are the inspection rows).
