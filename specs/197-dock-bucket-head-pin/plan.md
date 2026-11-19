# Implementation Plan: The dock's bucket head owns the strip above its label

**Spec**: `specs/197-dock-bucket-head-pin/spec.md`
**Branch**: `fix/197-dock-bucket-head-pin`
**Bump**: `patch`
**Preview**: `specs/197-dock-bucket-head-pin/preview/` (static, plus the live route named below)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | CSS only — `static/styles/design/obs-dock.css` (Django 4.0 templates unchanged, no Python, no JS) |
| Primary dependencies | none added; the dock's stylesheet loads `tokens.css` as it already did |
| Storage | none — no model, no migration, no data touched |
| Testing | Playwright (Python) E2E through Django's `StaticLiveServerTestCase`, the repo's user-visible acceptance harness |
| Target platform | Chromium at 320–2560px wide, light and dark; the same page in OBS's own browser |
| Project type | Server-rendered Django page with a stylesheet and one script; the slice touches the stylesheet alone |
| Performance goals | none — sticky positioning is already in use; no new layer, no script on the scroll path |
| Constraints | the head's foot (100.52px) and the reserve (37px) must not move; the runner's pins and the dock's other scrollers must be untouched |
| Scale / scope | 3 declarations in one file; 5 E2E tests in one new module |

## Constitution Check

No `CONSTITUTION.md` exists at the repo root (SDD-01: the constitution is optional and never auto-created), so
this table has no principles to check against. The repo's standing constraints still apply and are met: no
person's name in the artifacts, no secret, no new dependency.

Re-checked after Phase 1: pass — the design adds no dependency, no script and no data, and the preview is
built from the product's own markup and stylesheet.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entities: the slice changes where a sticky box starts, nothing is stored.
- `contracts/` — `none`: the dock page exposes no interface of its own; the geometry is internal CSS.
- `quickstart.md` — how to run the page and the E2E module, and the numbers to read.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/styles/design/obs-dock.css` (`#pickBody`, `.group__head`) | `test` → `tests/e2e/test_dock_bucket_head.py::test_a_pinned_bucket_head_leaves_no_row_above_it` | hit test at scroller top + 2px must be the head, and head top − scroller top = 0 |
| FR-002 | same | `test` → `::test_the_label_holds_its_place_between_rest_and_pinned` | the label's offset is one number at `scrollTop` 0 and pinned |
| FR-003 | `static/styles/design/obs-dock.css` (`scroll-padding-top`) | `inspection` — the declaration reads 37px and the head's foot reads 100.52px, so the reserve still covers the pinned head | the cursor test below proves the consequence |
| FR-004 | same | `test` → `::test_nothing_below_the_head_moves` | first row's top equals the head's foot at rest and pinned; the runner's rules are absent from the diff |
| FR-005 | same (`#pickBody section + section`) | `test` → `::test_consecutive_buckets_keep_their_air` | the air equals the first label's offset + 12px |
| US1/AC2 | the same page, scrolled by hand | `manual` — scroll the picker past a bucket with a row half out; nothing paints above the label | the pixel scan that backed the preview is not part of the suite |
| US2/AC1 | `static/web/obs-dock.js` (`setPickCursor`) | `test` → `::test_the_cursor_still_parks_below_the_head` | walks the cursor up through a boundary and reads every parked row |
| SC-001 | strip pixels | `test` → `::test_a_pinned_bucket_head_leaves_no_row_above_it` (hit test stands in for the pixel count; the count itself was the preview's evidence) | |
| SC-002 | hit test | `test` → same test | |
| SC-003 | label offsets | `test` → `::test_the_label_holds_its_place_between_rest_and_pinned` | |
| SC-004 | head foot + cursor clearance | `test` → `::test_nothing_below_the_head_moves`, `::test_the_cursor_still_parks_below_the_head` | |
| SC-005 | first row's top | `test` → `::test_nothing_below_the_head_moves` | |
| SC-006 | boundary air | `test` → `::test_consecutive_buckets_keep_their_air` | |
| — | the preview page | `inspection` — `preview/index.html` opens at the pinned offset and prints 4.0/`span.servicerow__n`/10.0 against 0.0/`h3.group__head`/26.0 | the same numbers the tests assert |

**Verification split**: 5 test · 2 inspection · 1 manual

## Risks and their handling

- **A second sticky element in the picker later** would inherit `#pickBody`'s zero top padding and need its own
  compensation. Recorded in the stylesheet's comment; the runner's pattern (`top: -4px`) is the precedent.
- **The air number is a look dial**: 8px is the accepted value; changing it changes only the boundary and one
  assertion in `::test_consecutive_buckets_keep_their_air`.