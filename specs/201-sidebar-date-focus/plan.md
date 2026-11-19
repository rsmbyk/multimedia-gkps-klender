# Implementation Plan: a clicked service keeps its date

**Spec**: `specs/201-sidebar-date-focus/spec.md`
**Branch**: `fix/201-sidebar-date-focus`
**Bump**: `patch`
**Preview**: `specs/201-sidebar-date-focus/preview/`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12; CSS (no build step) |
| Primary dependencies | Django 4.0, DRF; Playwright (Python) for E2E |
| Storage | unchanged (no model or migration) |
| Testing | Django runner; `StaticLiveServerTestCase` E2E in `tests/e2e/` |
| Target platform | desktop and touch browsers already supported by the design tokens |
| Project type | server-rendered Django templates + vanilla JS + stylesheet |
| Performance goals | none; selector change only |
| Constraints | keep the `@media (hover: hover)` guard and touch rules; no new DOM state |
| Scale / scope | one rule pair in `components.css`, one E2E module, two capability blocks |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| No `CONSTITUTION.md` in this repo (SDD-01) | pass | nothing to check against |

Re-checked after Phase 1: pass.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entities; invariants recorded.
- `contracts/` — none.
- `quickstart.md` — commands that run in this worktree.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/styles/design/components.css` (date rule, ~1440) | `test` → `tests/e2e/test_sidebar_date_reveal.py::test_a_clicked_row_paints_its_date_again` | rest, hover, clicked, blur |
| FR-001 | `tests/e2e/test_sidebar_date_reveal.py::test_keyboard_focus_on_an_action_hides_the_date_until_it_leaves` | `test` | pencil/trash focus-visible |
| FR-002 | `static/styles/design/components.css` (same rule, Today badge selector) | `test` → `tests/e2e/test_sidebar_date_reveal.py::test_the_today_badge_follows_the_date_reveal` | Today row fixture |
| FR-003 | `static/styles/design/components.css` (~1440-1445) | `inspection` — media guard, touch rules and accessible label unchanged in the diff | structural guard |
| FR-004 | `multimedia/web/templates/reading/_tatib_panel.html:8-10` | `inspection` — no template change; date stays in `aria-label` and DOM | structural guard |
| SC-001 | `tests/e2e/test_sidebar_date_reveal.py` | `test` | computed `display: block` with `:focus-within` true |
| SC-002 | same module | `test` | hover and action focus `none`, blur `block` |
| SC-003 | same module | `test` | box height and `aria-label` read before/after states |
| US1/AC5 | same module | `test` | tab onto the row's link keeps the date painted |
| US2/Edge 3 | same module | `test` | touch context leaves controls drawn and date painted |
| US1/AC3 | `specs/201-sidebar-date-focus/preview/index.html` | `manual` | press Click row (pointer away) in both panels |

**Verification split**: 9 test · 2 inspection · 1 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/201-sidebar-date-focus/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/README.md  checklists/requirements.md  preview/
```

### Source

```
static/styles/design/components.css      # one rule pair
tests/e2e/test_sidebar_date_reveal.py    # new focused E2E module
```

### Structure Decision

The CSS rule stays in `components.css` beside the row-action rules it follows; the E2E gets its
own module so the state matrix is readable on its own and does not enlarge `test_reading.py`.
No template, script, migration or settings change.
