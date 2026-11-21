# Implementation Plan: a slot states the kind it resolves to

**Spec**: `specs/213-slot-kind-badge/spec.md`
**Branch**: `feat/213-slot-kind-badge`
**Bump**: `patch`
**Preview**: `specs/213-slot-kind-badge/preview/` — live at `http://127.0.0.1:8777/tatib/151/`, plus the
static A/B/C comparison `preview/compare.html`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 · Django 4.0 templates (DTL) · hand-written CSS |
| Primary dependencies | none added — no JS, no library, no build step |
| Storage | unchanged (reads `ServiceEntry.fill_kind`) |
| Testing | Django test runner; Playwright (Python) E2E for the user-visible behaviour |
| Target platform | server-rendered page, Chromium/Firefox/Safari; both themes |
| Project type | Django web app, server-rendered templates with vanilla JS |
| Performance goals | none measurable: one extra `<span>` and `<svg>` per slot row, no query added |
| Constraints | the badge must not move a row (spec 055/140/143/144 geometry); must be legible at the 400px pane in both themes; must be self-contained (no new asset, no external font) |
| Scale / scope | 2 templates, 1 CSS block, 1 new partial; ~30 lines of markup+CSS; one E2E test, one unit test |

## Constitution Check

`CONSTITUTION.md` does not exist, and SDD-01 makes it optional and never auto-created. The repo's
binding conventions are `docs/PROCESS.md` (checked below) and the geometry contracts recorded in
`docs/spec/reading.md` — those are what this table checks instead.

| Principle | Status | Note |
| --- | --- | --- |
| SDD-06 — the preview is built from the project's own components and `## UI/UX` holds numbers | pass | the live page is the real route with the change applied; `compare.html` is the served markup plus the three real stylesheets, inlined |
| TDD-01 — a failing test comes before the code for every `test` row | pass | tasks T002/T003 are written red-first; the badge did not exist when the assertions were authored |
| TDD-06 — one behaviour per test, named for it | pass | `test_a_slot_row_carries_the_kind_it_resolves_to`, `test_a_slot_with_no_kind_draws_no_badge` |
| Spec 144 FR-008 — the sidebar and the dock keep their own row anatomy | pass | neither carries a mark today; the badge lives inside `_slot_mark.html`, which only the stage includes |
| Spec 055/140/143/144 — the stage's box, rail and text column are fixed | pass | measured: every row's top/height, every title's `x` and the page's scroll height are identical with the badge and with it suppressed |
| No new dependency / self-contained assets | pass | inline SVG on the page's own tokens; nothing fetched |
| BRD-10 — a card past `Speccing` carries one anchor issue | pass | `issue: 562` |

Re-checked after Phase 1: pass, no violations.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

Seven decisions: the badge's home partial (D001), server-rendered from the row's resolved kind (D002),
the four glyphs redrawn on a 12-unit grid (D003), the disc's fill and its behaviour on the row's four
fill states (D004), the frame's `>` selector (D005), the glyph's paint declared on the template (D006),
and the test placement (D007).

## Phase 1 — Design

- `data-model.md` — n/a, no stored state changes; it records which existing field is read
- `contracts/stage-markup.md` — the markup seam three suites read, and what must not change
- `quickstart.md` — run, look, verify, test, rebuild the previews

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 a slot row carries a badge naming its kind | `_slot_mark.html`, `_slot_kind_badge.html`, `tatib.html` | `test` → `tests/e2e/test_tatib_templates.py::test_a_slot_row_carries_the_kind_it_resolves_to` | six slots on the fixture, one badge each |
| FR-002 the badge differs per kind | `_slot_kind_badge.html` | `test` → same test | the four `data-kind-badge` values and their path data are pairwise different; `preview/probe_glyphs.py` prints the pixel-map difference (closest pair 0.141) |
| FR-003 the mark keeps its own identity | `_slot_mark.html`, `generate.css` | `test` → same test | the frame's `stroke-dasharray` and the `+`/`◎` path are unchanged |
| FR-004 the badge is `aria-hidden` and the row's name is unchanged | `_slot_kind_badge.html` | `test` → same test | compares the row's accessible name with the badge and with it suppressed |
| FR-005 no height, no title moved | `generate.css` | `test` → same test | every slot row's `y`/`height`, every title's `x`, the page's scroll height, badge vs suppressed |
| FR-006 legible on the canvas and on the fill, both themes | `generate.css` | `test` → same test | glyph colour and disc fill per theme; the fill states' `background-image` |
| FR-007 an unreadable kind draws no badge | `_slot_mark.html` (`{% if fill_kind %}`) | `test` → `multimedia/web/tests.py::test_a_slot_with_no_kind_draws_no_badge` | the local data cannot produce such a row, so it is a unit test |
| SC-001 every slot row badged, a service carries none | `tatib.html` | `test` → the E2E above | counts the badges against the fixture's slots; the dated service's page carries none |
| SC-002 the four kinds are told apart | `_slot_kind_badge.html` | `test` → the E2E above + `preview/probe_glyphs.py` | path data differ; pixel maps differ by ≥ 0.141 normalised |
| SC-003 the mark keeps its identity | `_slot_mark.html` | `test` → the E2E above | |
| SC-004 nothing moves | `generate.css` | `test` → the E2E above | |
| SC-005 reachable-free | `_slot_kind_badge.html` | `test` → the E2E above | `aria-hidden` + accessible-name equality |
| US1/AC1–4 | the page | `test` → the E2E above | four scenarios, one test |
| US2/AC1 the badge and the entry's mark share one glyph | `_slot_kind_badge.html` | `inspection` — open `/tatib/151/`: the song slot's badge and the song entry's 20px mark are the same note | the entry's mark is spec 144's, untouched |
| US2/AC2 legible on the hover fill | `generate.css` | `test` → the E2E above | the disc repaints the row's own tint; assert `background-image` is set in each fill state |
| US2/AC3 both themes | `generate.css` | `test` → the E2E above | contrast 5.57 light / 6.59 dark, read off computed colours |
| US3/AC1–3 no height, no wrap, no motion | `generate.css` | `test` → SC-004's assertions | |
| Edge: a choice with no options still badged | `_slot_kind_badge.html` | `test` → the E2E above | the fixture carries a fifth slot, a choice with no options; its badge is drawn and its row still reads `No options yet` |
| Edge: the Use template dialog carries no badge | `_generate_modal.html` | `inspection` — the dialog's slot rows are `.g-row--slot` and carry no `.slot__mark` | already true; nothing to change |

**Verification split**: 13 test · 2 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

No violation: the slice adds one partial, one CSS block and one include argument.

## Project Structure

### Documentation

```
specs/213-slot-kind-badge/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md  converge.md
  contracts/stage-markup.md  checklists/requirements.md
  preview/  index.html  compare.html  README.md  build_preview.py  build_compare.py
            probe.py  probe_candidates.py  probe_adopted.py  probe_glyphs.py  shots/
```

### Source

```
multimedia/web/templates/reading/
  _slot_kind_badge.html      new — the badge and its four glyphs
  _slot_mark.html            + one include, one argument
  tatib.html                 + fill_kind=item.slot_kind on the mark's include
static/styles/design/
  generate.css               + the badge's box, disc, fill-state rule and glyph size;
                             .slot__mark svg -> .slot__mark > svg
tests/e2e/test_tatib_templates.py   + one test
multimedia/web/tests.py             + one unit test
```

### Structure Decision

The badge is a partial rather than inline markup because `_slot_mark.html` is already the single place
a slot's mark is drawn and already branches on the row's kind. The styles go in `generate.css`'s
existing `#read` block — the same block that seats `.slot__mark`, `.slot__tile` and the choice's
options — because the badge is part of that block's geometry and splitting it across two sheets is how
the two drift. No new stylesheet, no new script.
