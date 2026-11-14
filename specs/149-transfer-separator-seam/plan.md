# Implementation Plan: The Transfers list draws each boundary once

**Spec**: `specs/149-transfer-separator-seam/spec.md`
**Branch**: `fix/149-transfer-separator-seam`
**Bump**: `patch`
**Preview**: `specs/149-transfer-separator-seam/preview/preview.html` (static; the same page measured by `specs/149-transfer-separator-seam/preview/probe.py`)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | CSS (`static/styles/design/components.css`) and one class on a `<div>` in `multimedia/web/templates/reading/base.html`; no Python, JavaScript, template-logic or migration change |
| Primary dependencies | none added — the existing `--divider`, `--canvas`, `--ink` and `--head-ink` tokens and the existing `.media-transfers*` class names |
| Storage | none |
| Testing | Playwright (Python) E2E through `StaticLiveServerTestCase`: four tests in `tests/e2e/test_media_library.py`, driving its fake companion (`page.route('http://127.0.0.1:63174/**')`) |
| Target platform | every viewport the dialog draws at, both themes, and every engine this app already supports — `:has()` is the only feature used, and `components.css` already relies on it |
| Project type | server-rendered Django web app, no build step; WhiteNoise serves a collected `static/` |
| Performance goals | no request added; one `:has()` selector evaluated over the dialog's rows only |
| Constraints | the dialog's `max-height: min(86vh, 46rem)` and 22px padding stay; the divider's insertion rule in `media-handoff.js` stays; scrollbars keep spec 087's global styling |
| Scale / scope | 1 template attribute, 3 CSS rules, 4 E2E tests |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check is not applicable.
The repo's standing constraints are honoured: design tokens rather than literals, no new dependency,
no inline style, no change to the companion's API, and CSS only where the drawing is decided.

Re-checked after Phase 1: pass. The slice adds no route, stores nothing, and touches no surface other
than the Transfers dialog.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the two view entities the list renders (`Transfer row`, `Session seam`) and the
  invariants the CSS has to keep.
- `contracts/` — `none`: the slice exposes no interface. The companion's `/v1/transfers` response and
  the Django routes are unchanged.
- `quickstart.md` — the preview's two commands, the targeted E2E run, and the dev-server route.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/styles/design/components.css` — `.media-transfers__row:has(+ .media-transfers__divider)` | `test` → `tests/e2e/test_media_library.py::MediaLibraryE2ETests::test_the_session_seam_draws_one_line` | the row above the seam reports `border-bottom-width: 0px`, the divider `border-top-width: 2px`, and one painted boundary sits within 20px above the divider |
| FR-002 | same rule, plus `.media-transfers__divider`'s `margin: 9px 0` | `test` → `tests/e2e/test_media_library.py::MediaLibraryE2ETests::test_the_seam_keeps_equal_space_either_side` | the painted line's centre is 9px from the row above's padding box and 9px from the row below's |
| FR-003 | `.media-transfers__row`'s existing `border-bottom: 1px` | `test` → `tests/e2e/test_media_library.py::MediaLibraryE2ETests::test_the_session_seam_draws_one_line` | every other row still reports `1px` and its 72px pitch |
| FR-004 | `multimedia/web/templates/reading/base.html` (`media-transfers__list`) + `.media-transfers__dialog` / `.media-transfers__list` rules | `test` → `tests/e2e/test_media_library.py::MediaLibraryE2ETests::test_a_long_transfer_list_scrolls_inside_the_dialog` | the list reports `scrollHeight > clientHeight`, the dialog reports no scroll of its own, and the title's box is unchanged before and after scrolling the list |
| FR-005 | `.media-transfers__list` + the dialog's `padding: 22px` | `test` → `tests/e2e/test_media_library.py::MediaLibraryE2ETests::test_a_long_transfer_list_scrolls_inside_the_dialog` | the list's box ends at the dialog's inner bottom edge (0px past); scrolled to the end, the last row's border is 22px above the dialog's border |
| FR-006 | `.media-transfers__list` (`overflow-y: auto`) | `test` → `tests/e2e/test_media_library.py::MediaLibraryE2ETests::test_a_short_transfer_list_keeps_its_natural_height` | two rows: no divider, dialog shorter than `max-height`, `scrollHeight == clientHeight` |
| SC-001 | as FR-001 | `test` → `test_the_session_seam_draws_one_line` | one painted boundary within 20px of the seam, against the two the report showed |
| SC-002 | as FR-005 | `test` → `test_a_long_transfer_list_scrolls_inside_the_dialog` | the lowest visible boundary is at least 22px above the dialog's bottom border |
| SC-003 | as FR-004 and FR-005 | `test` → `test_a_long_transfer_list_scrolls_inside_the_dialog` | the list's box past the dialog's inner bottom edge is 0px at nine and at fifteen rows |
| SC-004 | as FR-003 and FR-006 | `test` → `test_a_short_transfer_list_keeps_its_natural_height` | row count, 72px pitch and 1px borders identical to develop |
| US1/AC1 | `specs/149-transfer-separator-seam/preview/preview.html` | `inspection` — open the preview, press `9 rows`, and count the lines between the elephant row and `random.jpg` | the report's own nine rows and its own seam |
| US1/AC2 | as FR-002 | `test` → `test_the_seam_keeps_equal_space_either_side` | equal 9px either side |
| US1/AC3 | `static/web/media-handoff.js`'s `separated` branch | `inspection` — a list whose only unseen row is the first | the divider is the list's first child and the row below it keeps its 1px border |
| US1/AC4 | `media-handoff.js`'s `source` guard | `test` → `test_the_session_seam_draws_one_line` and the existing `test_sidebar_transfer_session_shows_active_then_finished` | opened from `#mediaTransfersButton` and while a transfer is active: no `.media-transfers__divider` at all |
| US2/AC1 | as FR-004 | `test` → `test_a_long_transfer_list_scrolls_inside_the_dialog` | fifteen rows, nothing painted outside the dialog |
| US2/AC2 | as FR-005 | `test` → `test_a_long_transfer_list_scrolls_inside_the_dialog` | scrolled to the end: 22px |
| US2/AC3 | `.media-transfers__dialog` flex column | `test` → `test_a_long_transfer_list_scrolls_inside_the_dialog` | the `h2`'s rect is identical before and after `list.scrollTop` changes |
| US2/AC4 | as FR-006 | `test` → `test_a_short_transfer_list_keeps_its_natural_height` | no scrollbar, natural height |
| Edge — one row | as FR-006 | `test` → `test_a_short_transfer_list_keeps_its_natural_height` | one row, one border, no divider |
| Edge — divider first | as US1/AC3 | `inspection` — the same first-child case in the preview | one line, no stray 9px band above the title |
| Edge — failed / cancelled rows | `.media-transfers__main span` | `inspection` — the status text of a failed row in the preview | text and border unchanged; no rule in this slice reaches them |
**Verification split**: 17 test · 4 inspection · 0 manual

Outside the table: the dark theme is not a requirement of its own, and is checked by inspection —
press `Dark` in the preview and re-read the metrics table (the same counts and distances, with
`--divider` at `#3A362F`).

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | — | — |

## Project Structure

### Documentation

- `specs/149-transfer-separator-seam/spec.md` — the requirements
- `specs/149-transfer-separator-seam/plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `tasks.md`, `analysis.md`
- `specs/149-transfer-separator-seam/contracts/none.md` — the explicit “no interface”
- `specs/149-transfer-separator-seam/checklists/requirements.md` — reviewer-owned
- `specs/149-transfer-separator-seam/preview/preview.html` — the static preview, with `README.md`, `build_preview.py`, `probe.py`, `assets/` and `shots/` beside it

### Source

```
static/styles/design/components.css          three rules beside the existing .media-transfers block
multimedia/web/templates/reading/base.html   one class on #mediaTransfersList
tests/e2e/test_media_library.py              four tests in the existing class
```

### Structure Decision

The three rules live in the same block as the rules they correct (`components.css`, beside
`.media-transfers__row` and `.media-transfers__divider`), because a separate block would split one
surface's drawing across two places and the next reader would find only half of it. The class goes on
the element the script already owns rather than replacing the id. The tests join
`tests/e2e/test_media_library.py`, where the fake companion and the rail button already exist; a new
module would duplicate that harness.
