# Implementation Plan: An empty Tata Ibadah is centred, and its five kinds are tiles

**Spec**: `specs/130-empty-service-tiles/spec.md`
**Branch**: `fix/130-empty-service-stage`
**Bump**: `patch`
**Preview**: the running branch — the owner asked for the change in a working session, so the branch itself is
the preview (the same sequencing the previous slice used). Measured numbers are in `spec.md` § UI/UX and in
`quickstart.md`.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django templates; vanilla JS (ES5 style, no build step); CSS |
| Primary dependencies | Django 4.0 templates, WhiteNoise; no new dependency |
| Storage | none — no model, view signature or payload changes |
| Testing | Django's runner; Playwright (Python) E2E through `StaticLiveServerTestCase` |
| Target platform | evergreen Chromium/Firefox/Safari (the app already relies on `:has`, `text-wrap: balance`) |
| Project type | server-rendered web app with a saved-page renderer and an in-place rebuild |
| Performance goals | none; the change is CSS plus five inline SVG templates |
| Constraints | three renderers must agree: `templates/reading/tatib.html`, `static/web/offline-render.js`, `static/web/entries.js` |
| Scale / scope | one block in one pane; five buttons |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| No new dependency | pass | CSS `:has()`/container queries and inline SVG only |
| One behaviour, three renderers | pass | the saved renderer and the delete-rebuild take the same markup |
| Accessible name is never lost with the label | pass | the label moves into `.sr` and the tooltip |
| A pane that holds items is untouched | pass | every rule is scoped to `.entry__empty` |

Re-checked after Phase 1: pass — the container query is the only mechanism new to this stylesheet, and it
degrades to the shrink-only row where it is unsupported.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — n/a: nothing is stored; the block is derived from `items` being empty.
- `contracts/` — `none` (no endpoint, no payload, no fragment signature changes).
- `quickstart.md` — how to open the empty service and the four measurements to take.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/styles/design/components.css` (`.read[data-kind="tatib"]:has(.entry__empty)`) | `test` → `tests/e2e/test_entries.py::EntryModalE2ETests::test_an_empty_service_places_its_tiles_a_quarter_of_the_way_down` | block centre within 12px of the quarter mark at 1440×900 |
| FR-002 | `static/styles/design/components.css` (`.entry__empty-actions`, `.entry__empty-btn`) | `test` → same test | five tiles, one row, square, ≥44px |
| FR-003 | `multimedia/web/templates/reading/tatib.html` | `test` → same test | `title` + `.sr` span per tile |
| FR-004 | `multimedia/web/templates/reading/tatib.html`, `static/web/*.js` | `test` → `tests/e2e/test_saved_render_parity.py` (`icon_count` 5) | media glyph added |
| FR-005 | `static/styles/design/components.css` (`@container (max-width: 300px)`) | `inspection` — open at 1280×800 and 1024×700 | 3+2 at 52px |
| FR-006 | `static/web/offline-render.js`, `static/web/entries.js` | `test` → `tests/e2e/test_saved_render_parity.py` | labels, glyphs and size compared |
| FR-007 | the same stylesheet rules, all scoped | `inspection` — service 144 before/after | header 30px margin and body 8px margin unchanged |
| US1/AC1–2 | measurement | `inspection` — `quickstart.md` probe at four viewports | block centre 26.2% of the reading area at 1440×900, clear of the header at all four |
| SC-003 | `.entry__empty-btn` width fallback | `test` → the 44px floor in the same test at 1440×900 | narrow case inspected |

**Verification split**: 5 test · 4 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| `:has()` and `@container` in a shared stylesheet | the block, the article and the body all have to know the state, and a JS class would add a fourth renderer to keep in step | a body class set by JS desyncs from the server render before scripts run |
| five inline glyphs duplicated in two JS files | the saved renderer and the rebuild have no shared module and the repo has no bundler | a shared module means a new `<script>` on two shells for five paths |

## Project Structure

### Documentation

```
specs/130-empty-service-tiles/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/README.md  checklists/checklist.md
```

### Source

```
multimedia/web/templates/reading/tatib.html   the five tiles + .sr labels
static/web/offline-render.js                  emptyAddButtons() — the saved copy
static/web/entries.js                         emptyAddButton() — the post-delete rebuild
static/styles/design/components.css           the centred block and the tile row
tests/e2e/test_entries.py                     the block's geometry and the tile row
tests/e2e/test_saved_render_parity.py         five glyphs, and tiles compared by content
docs/spec/reading.md                          R6
```

### Structure Decision

The three renderers stay where they are: this slice adds markup to each, not a fourth source of truth. The
stylesheet rule lives beside the block it dresses in `components.css`, not in a new file.
