# Implementation Plan: a media size reads in the unit that still shows its number

**Spec**: `specs/145-media-size-precision/spec.md`
**Branch**: `feat/145-media-size-precision`
**Bump**: `patch`
**Preview**: `specs/145-media-size-precision/preview/` — live, the slice's own server

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | JavaScript, ES5 style in `media-entry.js` and `media-library.js`, ES2015 in `media-handoff.js` |
| Primary dependencies | none — one new file, loaded by `reading/base.html` |
| Storage | none; sizes arrive as `byte_count` / `size` in existing payloads |
| Testing | Django test runner; Playwright (Python) E2E through `StaticLiveServerTestCase` |
| Target platform | Chrome and Safari on macOS, 1440×900 and 720px |
| Project type | Django 4.0 server-rendered pages with vanilla JS |
| Performance goals | O(1) per label; no measurable change to a library render |
| Constraints | no framework, no build step, self-hosted assets only, WhiteNoise manifest hashing |
| Scale / scope | ≤ 200 MB per file, a few hundred files per library |

## Constitution Check

`CONSTITUTION.md` does not exist in this repository (`ls CONSTITUTION.md` → absent), so there are no
project principles to check against; the repo conventions in `AGENTS.md` and `docs/PROCESS.md` apply.

Re-checked after Phase 1: pass.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entity changes; the label is derived.
- `contracts/` — none: the slice exposes no interface outside the page.
- `quickstart.md` — how to run the branch server and read the label on each surface.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/media-size.js` | `test` → `tests/e2e/test_media_library.py::MediaLibraryE2ETests::test_media_size_reads_in_the_smallest_unit_that_shows_a_number` | no label reads zero |
| FR-002 | `static/web/media-size.js` | `test` → same test | `2 KB`, not `2.0 KB`; `999,999 B → 1 MB` |
| FR-003 | `multimedia/web/templates/reading/base.html`, `media-entry.js`, `media-library.js` | `test` → same test | card + library agree |
| FR-004 | `static/web/media-size.js` | `test` → same test | `512 B` |
| SC-001 | `static/web/media-size.js` | `test` → same test | table of byte counts |
| SC-002 | `static/web/media-size.js` | `test` → same test | exact strings |
| SC-003 | three surfaces | `inspection` — open the live preview, choose one file, compare the card and the library row | |
| SC-004 | `static/web/media-entry.js` (no CSS change) | `manual` — read the line's computed `font-size`, `line-height`, `color` in DevTools | |
| US1/AC1–3 | `media-entry.js:39,87` | `test` → same test | |
| US2/AC2 | `static/web/media-handoff.js` | `inspection` — `grep -n '\bfmt\b' static/web/media-handoff.js` returns nothing | |

**Verification split**: 3 test · 1 inspection · 1 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/145-media-size-precision/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/  checklists/  preview/
```

### Source

```
static/web/media-size.js          new — window.gkpsFormatSize
static/web/media-entry.js         formatSize delegates
static/web/media-library.js       fmtSize delegates
static/web/media-handoff.js       unused fmt removed
multimedia/web/templates/reading/base.html   loads media-size.js before media-entry.js
tests/e2e/test_media_library.py   one new acceptance test
```

### Structure Decision

`static/web/` already holds one behaviour per file (`media-stage.js` for icons, `media-image.js` for the
image stage), and `base.html` loads them in dependency order; the size label follows the same shape. No
template or stylesheet changes.
