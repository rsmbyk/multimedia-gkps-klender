# Implementation Plan: song-row focus ring is clipped at the list top

**Spec**: `specs/223-songrow-focus-ring-clip/spec.md`
**Branch**: `fix/223-songrow-focus-ring-clip`
**Bump**: `patch` — 1.36.8 → 1.36.9 (re-check `VERSION` on `origin/develop` before delivery)
**Preview**: `static preview at specs/223-songrow-focus-ring-clip/preview/index.html` (candidate A adopted)
**Gate 1**: accepted 2026-11-22; candidate A recorded from the skipped Clarify question.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | CSS in `static/styles/design/components.css`; Python 3.12 / Django 4.0 for the new E2E module; no JS change |
| Primary dependencies | none added — Playwright is already installed in the repo's virtualenv |
| Storage | none; the reserved space is a CSS box property, nothing is persisted |
| Testing | `tests/e2e/test_songrow_focus_ring.py` (new, three cases) on `StaticLiveServerTestCase` |
| Target platform | the browsers the app already supports; the mechanism is `:focus-visible` + a UA outline |
| Project type | server-rendered Django app, vanilla JS, no build step |
| Performance goals | none; one declaration, no script |
| Constraints | the row box, text, 1px pitch, hover and selected fills stay byte-identical; the first sidebar and other pages are untouched |
| Scale / scope | 1 CSS declaration, 1 new E2E module, spec pack, card and board row |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check does not apply. The
constraint row above stands in its place.

Re-checked after Phase 1: **pass** — no new file in the product, no request, no stored value, no
template or script hook.

## Phase 0 — Research

See `research.md`. Six decisions, each from a code read or a browser measurement: the UA outline is
the painter (D001), candidate A is in scope (D002), the space belongs on `.ch__body` (D003), the E2E
asserts the geometric relationship rather than screenshot pixels (D004), the test fixture owns its
own book and songs (D005), and the bump is `patch` (D006). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the row's three focus states and the geometry invariant.
- `contracts/` — `none` (`contracts/none.md`): no interface changes.
- `quickstart.md` — the DB-isolated commands and the three cases.

### The design

`static/styles/design/components.css`, at the `.ch__body` rule (currently `padding: 0 0 8px` at
line 1669):

```css
  padding: 3px 0 8px;
```

That gives the scrollport 3px of clearance above the first row. A 1px outline at a 1px offset needs
2px, so the ring's top edge lands inside the scrollport with 1px to spare. The rows, their 1px
pitch, their side padding and the bottom padding are untouched; the browser's outline rule is not
added, changed or suppressed.

`tests/e2e/test_songrow_focus_ring.py` — three cases on its own Book/Song fixtures, opening
`reverse('web-song', args=[song.pk])`:

1. `test_the_first_rows_ring_fits_inside_the_scrollport` — pointer-click the first row, press `a`;
   assert `:focus-visible`, `scrollTop == 0`, and `row.top - host.top >= outlineWidth + outlineOffset`.
2. `test_a_tabbed_first_row_gets_the_same_complete_ring` — Tab from the page until the row is
   active, then the same clearance assertion.
3. `test_focus_does_not_change_the_row_box_or_its_states` — before/after focus the row heights,
   pitch, `aria-current` and hover fill are identical, and an unfocused row has `outlineStyle none`.

**Deliberately not done.** No `:focus-visible` rule is added; no inset ring, no `--focus` colour, no
script, no template, no scroll manipulation, no change to the first sidebar, the song detail page or
other focusable controls. Candidate B stays in the preview as a comparison only.

## Traceability

| Requirement / scenario | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 full ring inside scrollport | `components.css` `.ch__body` padding | `test` → `test_songrow_focus_ring::test_the_first_rows_ring_fits_inside_the_scrollport` | clearance ≥ 2px |
| FR-002 row box, pitch, text, fills unchanged | untouched `.songrow` rules | `test` → `::test_focus_does_not_change_the_row_box_or_its_states` | heights 38 / 57.5px in the preview |
| FR-003 unfocused outline stays none | untouched CSS | `test` → `::test_focus_does_not_change_the_row_box_or_its_states` | `outlineStyle === 'none'` |
| FR-004 both themes and three viewports, last row | `.ch__body` padding; existing 8px bottom padding | `manual` — preview states at 1440×900, 900×700, 390×844 in dark and light, scroll to bottom and focus last row | relationship asserted in the test; theme checks are manual |
| FR-005 first sidebar and other pages unchanged | the diff | `inspection` — only `.ch__body`'s padding declaration changes; `test` → `tests.e2e.test_reading` module re-run | |
| FR-006 candidate A only, 3px, no ring restyle | `components.css` | `inspection` — no `:focus-visible` selector appears in the diff | skipped Clarify recorded in spec |
| US1 AC1 first row at scrollTop 0, Tab focus | as FR-001 | `test` → `::test_a_tabbed_first_row_gets_the_same_complete_ring` | |
| US1 AC2 key after pointer focus | as FR-001 | `test` → `::test_the_first_rows_ring_fits_inside_the_scrollport` | |
| US1 AC3 unfocused, hover and selected states | as FR-002/FR-003 | `test` → `::test_focus_does_not_change_the_row_box_or_its_states` | |
| US1 AC4 bottom row not clipped | existing bottom padding | `manual` — the last-row state in the preview | |
| US1 AC5 themes and viewports | as FR-004 | `manual` — the preview's responsive and theme states | |
| US1 AC6 other surfaces unchanged | as FR-005 | `inspection`; `test` → `tests.e2e.test_reading` | |
| Edge: not a scroll defect | scrollTop / scrollHeight | `test` → `::test_the_first_rows_ring_fits_inside_the_scrollport` | `scrollHeight === clientHeight` before focus |
| Edge: three-line row 57.5px | `.songrow` clamp | `manual` — preview's three-line song row | |
| Edge: side padding already sufficient | `.ch__body ul` padding 0 10px | `inspection` — that declaration is unchanged | |
| SC-001 complete ring | as FR-001 | `test` → `::test_the_first_rows_ring_fits_inside_the_scrollport` | pixel diff in the preview, geometry in the test |
| SC-002 not a scrolled list | `scrollTop`, `scrollHeight` | `test` → `::test_the_first_rows_ring_fits_inside_the_scrollport` | |
| SC-003 geometry and states unchanged | as FR-002 | `test` → `::test_focus_does_not_change_the_row_box_or_its_states` | |
| SC-004 Tab and key-after-pointer | two focus paths | `test` → the first two cases | |
| SC-005 no ring unfocused | as FR-003 | `test` → `::test_focus_does_not_change_the_row_box_or_its_states` | |

**Verification split: 14 test · 4 inspection · 3 manual** across 21 rows (rows naming two methods
are counted in both).

## Plan exit gate

| Check | Result |
| --- | --- |
| Requirement coverage | FR-001…FR-006, US1 AC1–AC6 and SC-001…SC-005 each carry a row |
| Entity coverage | the three focus states and the geometry invariant are in `data-model.md`; nothing stored |
| Interface coverage | `contracts/none.md` states `none` and why |
| Decision provenance | D001–D006 in `research.md`, each with a code read or measurement |
| Constitution conformance | no constitution exists; the constraint row is honoured |
| Zero unknowns | 0 |
| Verification declared | 14 `test` · 4 `inspection` · 3 `manual`; every `test` row names a module and case |
| `quickstart.md` runnable | yes — the test command runs on this worktree against `gkps223`; manual states are reachable in the preview today |

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/223-songrow-focus-ring-clip/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/none.md  checklists/requirements.md
  preview/{index.html,README.md,build_preview.py,assets/}
```

### Source

```
static/styles/design/components.css        `.ch__body` padding-top 0 → 3px
tests/e2e/test_songrow_focus_ring.py        three cases
docs/spec/reading.md                        R52 at Fold
backlog/items/ITEM-238-songrow-focus-ring-clip.md
backlog/board.md                            card row
specs/README.md                             index row
VERSION, CHANGELOG.md                       patch bump and one line, at delivery
```

### Structure Decision

No new product module. The rule sits on the scrollport that clips; the regression cases live in a
module of their own because no existing E2E module owns the song-list focus geometry.
