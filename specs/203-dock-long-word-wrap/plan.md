# Implementation Plan: A long word wraps in the dock runner

**Spec**: `specs/203-dock-long-word-wrap/spec.md`
**Branch**: `fix/203-dock-long-word-wrap`
**Bump**: `patch`
**Preview**: live at `http://127.0.0.1:8767/obs/dock` (worktree `~/Projects/multimedia-gkps-klender-203`);
`specs/203-dock-long-word-wrap/preview/README.md` names every state and the probe that reads them.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | CSS only — `static/styles/design/obs-dock.css` (no Python, no JS, no template) |
| Primary dependencies | none added; the dock's stylesheet loads `tokens.css` as it already did |
| Storage | none — no model, no migration, no data touched |
| Testing | Playwright (Python) E2E through Django's `StaticLiveServerTestCase`, the repo's user-visible acceptance harness |
| Target platform | Chromium at 320–900px panels, light and dark; the same page in OBS's own browser |
| Project type | Server-rendered Django page with a stylesheet and one script; the slice touches the stylesheet alone |
| Performance goals | none — `overflow-wrap` is a layout-time text property; no new layer, no script on any path |
| Constraints | the number column (33.6px at left 18), every chevron (10px off the row's right, 0px off centre), the date box, and every box whose text already fits must not move; the two `nowrap` labels keep their cut |
| Scale / scope | 3 declarations in one file; 10 E2E tests in one new module |

## Constitution Check

No `CONSTITUTION.md` exists at the repo root (SDD-01: the constitution is optional and never auto-created),
so this table has no principles to check against. The repo's standing constraints still apply and are met:
no person's name in the artifacts, no secret (the quickstart reads the database password from the container
rather than writing it), no new dependency.

Re-checked after Phase 1: pass — the design adds no dependency, no script and no data, and the preview is
the product's own route running.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Seven decisions, each with its measurement or its failing run
as provenance; D007 records the sequence deviation rather than backdating it.

## Phase 1 — Design

- `data-model.md` — no entities: three declarations in a stylesheet, nothing stored.
- `contracts/` — `none`: no endpoint, event, storage key or cross-surface message changes.
- `quickstart.md` — how to serve the page, the numbers to read, and the two suite commands.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/styles/design/obs-dock.css` (`.serviceline`) | `test` → `tests/e2e/test_dock_text_wrap.py::test_an_unbroken_service_name_wraps_inside_its_column` | range-rect spill ≤ 1px at 320/456/900; more than one line at 456 |
| FR-002 | same (`.entryrow__t`) | `test` → `::test_an_unbroken_entry_header_wraps_inside_its_row` | every header's spill ≤ 1px at 320/456, covering the URL, the 200-char filename, the hyphenated name and the ordinary-songbook title |
| FR-003 | same (`.screenerow`) | `test` → `::test_a_screen_row_wraps_inside_the_open_block` | the open block's screen lines, spill ≤ 1px at 320/456 |
| FR-004 | same (all three) | `test` → `::test_the_runner_body_does_not_scroll_sideways` | `#runBody.scrollWidth - clientWidth == 0` and document overflow 0 at 320/456/900 |
| FR-005 | same | `test` → `::test_text_that_fits_is_unchanged`, `::test_a_short_service_is_unchanged`, `::test_a_wide_panel_renders_as_it_does_today` | the page read twice, rule shipped vs value restored to `normal`: height, width and line count equal for every fitting box |
| FR-005 (geometry) | same | `test` → `::test_the_row_keeps_its_number_and_chevron` | number widths and every visible chevron's offRight/offCentre equal in both reads |
| FR-006 | `.nextband__label`, `.offstrip__label` (unchanged) | `test` → `::test_a_truncating_label_still_truncates` | `nowrap`, `ellipsis`, one line, still clipped, on a live block tall enough to draw the band |
| FR-007 | `.servicerow__n` (unchanged) | `test` → `::test_the_picker_name_still_wraps` | computes `anywhere`, spill ≤ 1, more than one line |
| US1/AC1 | `.serviceline` | `test` → `::test_an_unbroken_service_name_wraps_inside_its_column` | |
| US1/AC2–3 | `.entryrow__t`, `.screenerow` | `test` → the header and screen-row tests | |
| US1/AC4 | `#runBody` | `test` → `::test_the_runner_body_does_not_scroll_sideways` | |
| US2/AC1–2 | fitting rows | `test` → `::test_text_that_fits_is_unchanged` | `random.jpg`, `images (1).jpeg`, the hyphenated filename |
| US2/AC3 | number column, chevron | `test` → `::test_the_row_keeps_its_number_and_chevron` | |
| US2/AC4 | wide panel | `test` → `::test_a_wide_panel_renders_as_it_does_today` | the name fits at 900px and is unchanged; a run wider than the panel still wraps |
| US3/AC1 | `.nextband__label` | `test` → `::test_a_truncating_label_still_truncates` | |
| US3/AC2 | `.servicerow__n` | `test` → `::test_the_picker_name_still_wraps` | |
| SC-001 | spill | `test` → the three wrap tests | |
| SC-002 | body overflow | `test` → `::test_the_runner_body_does_not_scroll_sideways` | |
| SC-003 | fitting boxes | `test` → the three no-change tests | |
| SC-004 | row geometry | `test` → `::test_the_row_keeps_its_number_and_chevron` | |
| SC-005 | truncators | `test` → `::test_a_truncating_label_still_truncates` | |
| — | the diff itself | `inspection` — `git diff origin/develop -- static/styles/design/obs-dock.css` reads three `overflow-wrap: anywhere` declarations and their comments, all inside the runner's rules; no picker, transport or find-band rule is touched | |
| — | the live page | `manual` — open `http://127.0.0.1:8767/obs/dock`, hard-reload, click the `hhhh…` service: the title takes three lines inside its own column, the URL two inside its header, and the body has no horizontal scrollbar | the owner's own click-through; the probe's numbers are the recorded evidence |

**Verification split**: 21 test · 1 inspection · 1 manual

## Risks and their handling

- **A taller header moves the sticky pin's geometry.** The live row pins at `top: -4px` against its own
  height, so a wrapped header simply pins taller; the block's 230ms morph takes the taller end value. Covered
  by the screen-row test, which projects the first entry and measures with the row pinned.
- **A future flex item without `min-width: 0`** added under `.entryrow__t` or `.screenerow` would let
  `anywhere` collapse its min-content size — the trap spec 137 recorded. The stylesheet's comment names the
  reason `anywhere` is safe here, so the next editor sees the condition rather than only the declaration.
- **The 200-character filename fixture is taller than any real header today.** It is inside the column's own
  255-character limit, so it is a value the product can hold, not an invented stress case.
