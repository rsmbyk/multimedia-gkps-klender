# Implementation Plan: The Transfers scrollbar sits at the dialog's edges

**Spec**: `specs/152-transfer-scrollbar-edge/spec.md` (revision 2)
**Branch**: `feat/152-transfer-scrollbar-edge`
**Bump**: `patch`
**Preview**: `specs/152-transfer-scrollbar-edge/preview/preview.html` (static; measured by `specs/152-transfer-scrollbar-edge/preview/probe.py`)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | CSS only — `static/styles/design/components.css`, the `.media-transfers__list` rule and the `.media-transfers__dialog` rule; no Python, JavaScript, template, or migration change |
| Primary dependencies | none added — the existing dialog's `padding: 22px`, `border: 1px`, `border-radius: 12px`, its flex column (spec 149) and spec 087's scrollbar rules |
| Storage | none |
| Testing | Playwright (Python) E2E through `StaticLiveServerTestCase`: four tests in `tests/e2e/test_media_library.py`, driving its fake companion (`page.route('http://127.0.0.1:63174/**')`), plus `preview/probe.py` for the painted numbers |
| Target platform | every viewport the dialog draws at, light and dark, in the engines this app supports — plain box geometry and `overflow: clip`, so no engine branch is added |
| Project type | server-rendered Django web app, no build step; WhiteNoise serves a collected `static/` |
| Performance goals | no request added; two rules with five declarations between them |
| Constraints | the dialog's `padding`, `border`, `border-radius`, `max-height` and flex column stay; spec 149's 22px end-of-scroll gap stays; spec 087's bar drawing stays |
| Scale / scope | 2 CSS rules, 4 E2E tests, 1 capability requirement |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check is not applicable.
The repo's standing constraints are honoured: design tokens rather than literals, no new dependency,
no inline style, no change to the companion's API, and CSS only where the drawing is decided.

Re-checked after Phase 1: pass. The slice adds no route, stores nothing, and touches no surface other
than the Transfers dialog.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** The four that had to be settled by measurement were the
box arithmetic (D001), the top edge the owner ruled out (D002), the corner the bar spilled over before
the clip (D005), and where spec 149's end-of-scroll gap now lives (D006).

## Phase 1 — Design

- `data-model.md` — the three boxes the slice moves relative to one another (dialog, list, row
  content) and the invariants between them.
- `contracts/` — `none`: the slice exposes no interface. The companion's `/v1/transfers` response and
  the Django routes are unchanged.
- `quickstart.md` — the preview's two commands, the dev server, and the targeted E2E run.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/styles/design/components.css` — `.media-transfers__list { margin: 0 -22px -22px; padding: 0 22px 22px; }` | `test` → `tests/e2e/test_media_library.py::MediaLibraryE2ETests::test_the_transfer_list_reaches_the_dialog_edges` | `dialog border-box right − list.right` and `dialog.bottom − list.bottom` are both the 1px border, and `list.left − dialog.left` the same, at 15 rows |
| FR-002 | same rule; the lane is the engine's, spec 087's drawing | `inspection` — `preview/probe.py`, headed Chromium: the thumb's painted column, the first non-canvas column to its right, and the thumb's bottom at the end of the scroll | cannot be a test: headless paints no bar (D007) |
| FR-003 | same rule — the matching `padding` is what restores the content box | `test` → `test_the_transfer_content_keeps_its_insets` | `row.left − dialog.left == 23`; `dialog.right − row.right == 23 + (offsetWidth − clientWidth)`, so it holds with and without a bar |
| FR-004 | the rule leaves the list's top alone; the `padding-bottom` carries the end gap | `test` → `test_the_dialog_frame_and_scroll_end_do_not_move` | title left 23, heading left 23, `list.top − title.bottom == 14`, and at `scrollTop = scrollHeight` the last row is 22px above the dialog's border |
| FR-005 | the same rule (`overflow-y: auto` is not changed) | `test` → `test_a_short_transfer_list_has_no_reserved_gutter` | two rows: `offsetWidth − clientWidth == 0`, `dialog.right − row.right == 23` |
| FR-006 | spec 087's rules in `components.css` (untouched by this slice) | `inspection` — `git diff` on the slice: no `::-webkit-scrollbar*`, `scrollbar-width` or `scrollbar-color` line appears in it | the bar the probe photographs is the app's own 5px `--scroll-thumb` bar |
| FR-007 | `.media-transfers__dialog { overflow: clip; }` | `test` → `test_the_transfer_list_reaches_the_dialog_edges` (the dialog reports `overflow: clip` and no scroll of its own) **and** `inspection` — the probe's corner shots | the test pins the mechanism; the probe shows the corner clean |
| SC-001 | as FR-002 | `inspection` — probe: canvas columns between the bar's right edge and the border, and the lane's bottom against it | 22px → 0px, 23px → 1px, at 1440×760 light and dark and at 420×820 |
| SC-002 | as FR-001 | `test` → `test_the_transfer_list_reaches_the_dialog_edges` | right and bottom 23px → 1px |
| SC-003 | as FR-003 and FR-005 | `test` → `test_the_transfer_content_keeps_its_insets`, `test_a_short_transfer_list_has_no_reserved_gutter` | row left 23 → 23; row right 28 → 28 with the bar, 23 → 23 without |
| SC-004 | as FR-004 | `test` → `test_the_dialog_frame_and_scroll_end_do_not_move` | title, heading, title→list and the end-of-scroll gap identical |
| SC-005 | the rules are engine- and theme-agnostic | `inspection` — probe at 1440×760 light, 1440×760 dark, 420×820 light; live app rail-opened and library-opened | every state in the preview's `README.md` state table |
| SC-006 | as FR-007 | `inspection` — probe's `-end` shots at both resizings | no bar pixel outside the border's curve |
| US1/AC1 | as FR-002 | `inspection` — probe at fifteen rows | the gap is the slice's own number |
| US1/AC2 | as FR-001 | `test` → `test_the_transfer_list_reaches_the_dialog_edges` | |
| US1/AC3 | as FR-002 and FR-007 | `inspection` — probe scrolled to the end, both corners photographed | the tip is cut by the radius, nothing paints outside |
| US1/AC4 | as SC-005 | `inspection` — probe's `--theme dark`, `--width 420`, and the live app's rail origin | |
| US2/AC1 | as FR-003 | `test` → `test_the_transfer_content_keeps_its_insets` | |
| US2/AC2 | as FR-005 | `test` → `test_a_short_transfer_list_has_no_reserved_gutter` | |
| US2/AC3 | as FR-004 | `test` → `test_the_dialog_frame_and_scroll_end_do_not_move` | |
| US2/AC4 | as SC-004 | `inspection` — probe `--theme dark` | same numbers as light |
| Edge — one row | as FR-005 | `inspection` — probe `--rows 2` (the short state; one row takes the same path) | |
| Edge — narrow | as SC-005 | `inspection` — probe `--width 420 --height 820` | dialog 382px wide; 0px gap, 1px bottom |
| Edge — active transfer | the rules are on the elements, not on the view | `inspection` — live app, rail origin (the progress view draws no age headings) | |
| Edge — scrolled | the rule sets no height and no scroll behaviour | `inspection` — probe's `-end` shots | the lane ends at the bottom border |
| Edge — closed | `dialog:not([open]) { display: none }` (UA) | `inspection` — `git diff`; the rules add no display or visibility change | nothing paints either way |
| Edge — keyboard | the slice touches no behaviour | `inspection` — `git diff`: no script file in it; the existing keyboard tests in the module still pass | |

**Verification split**: 12 test · 12 inspection · 0 manual

Outside the table: the scrollbar-hover state and the middle-of-the-scroll thumb are not requirements
of their own and are checked by inspection — spec 087's `:hover` rule is untouched, and the probe
photographs the bar at rest and at the end.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | — | — |

## Project Structure

### Documentation

- `specs/152-transfer-scrollbar-edge/spec.md` — the requirements
- `specs/152-transfer-scrollbar-edge/plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `tasks.md`, `analysis.md`
- `specs/152-transfer-scrollbar-edge/contracts/none.md` — the explicit "no interface"
- `specs/152-transfer-scrollbar-edge/checklists/requirements.md` — reviewer-owned
- `specs/152-transfer-scrollbar-edge/preview/preview.html` — the static preview, with `README.md`, `build_preview.py`, `probe.py`, `assets/` and `shots/` beside it

### Source

```
static/styles/design/components.css   .media-transfers__list gains its margins and padding;
                                      .media-transfers__dialog gains overflow: clip
tests/e2e/test_media_library.py       four tests in the existing class
```

### Structure Decision

The rules join the lines they correct — the list's own rule and the dialog's own rule — because a
separate block would split one surface's drawing across two places and the next reader would find only
half of it. No template change: spec 149 already put the class on `#mediaTransfersList`, and this
slice needs nothing new from the markup. The tests join `tests/e2e/test_media_library.py`, where the
fake companion and the `transfer_list_page` helper already exist; a new module would duplicate that
harness.
