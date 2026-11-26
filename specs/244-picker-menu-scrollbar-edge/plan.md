# Implementation Plan: picker popout scrollbar edge

**Spec**: `specs/244-picker-menu-scrollbar-edge/spec.md`
**Branch**: `fix/244-picker-menu-scrollbar-edge`
**Bump**: `patch`
**Preview**: `specs/244-picker-menu-scrollbar-edge/preview/` (live at `http://127.0.0.1:8778/`)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12; vanilla CSS/JS (no build step for styles) |
| Primary dependencies | Django 4.0, Django REST Framework; Playwright (Python) for E2E |
| Storage | none — no model or migration; PostgreSQL only as the E2E fixture database |
| Testing | Django test runner; user-visible acceptance in Playwright E2E |
| Target platform | modern Blink/WebKit browsers already covered by spec 087's bare 5px scrollbar |
| Project type | server-rendered Django web app with fixed-position picker popouts |
| Performance goals | no new layout work: two CSS declarations and one clipping keyword |
| Constraints | preserve `reading/R59` filtering, highlight, Tab commit and scroll-follow; preserve spec 087's bar drawing and spec 040's viewport-capped positioning; leave the mini-sidebar/rail scrollbar exceptions alone |
| Scale / scope | one stylesheet rule set, one focused E2E module, one capability modification at Fold |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| `CONSTITUTION.md` | n/a | No constitution file exists in this repo; repo `docs/PROCESS.md`, spec 087/152 precedents and `reading/R59` are the applicable rules. |

Re-checked after Phase 1: pass — no new principle, dependency or interface; the only changed file in
production code is a CSS rule set, and every requirement is traceable below.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the three CSS boxes (menu, scrollport, option content); no persisted entity.
- `contracts/` — `none` — CSS-only change, no exposed interface.
- `quickstart.md` — how to serve the slice and run the focused probe and browser modules.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/styles/design/components.css` `.editor__picker-options` | `test` → `tests/e2e/test_picker_menu_scrollbar_edge.py::test_scrollport_reaches_menu_edges` | `menu.right - options.right == 1`, bottom likewise |
| FR-002 | `static/styles/design/components.css` spec 087 pseudo-element rules | `inspection` — computed 5px bar rules unchanged; lane at the scrollport's outer columns in the live preview | painted pixels, no DOM node |
| FR-003 | `static/styles/design/components.css` `.editor__picker-options` | `test` → `…::test_option_and_filter_boxes_are_unchanged` | first option and chapter filter boxes equal the frozen numbers |
| FR-004 | `static/styles/design/components.css` `.editor__picker-menu` | `inspection` — computed `overflow: clip`, 10px radius; corner in the live preview | clip must not create a scroll container |
| FR-005 | `static/web/entries.js` (unchanged) | `test` → `tests/e2e/test_passage_search_pickers.py`, `tests/e2e/test_song_entry_pickers.py` | existing accepted modules, run at push |
| FR-006 | `static/styles/design/components.css` `.editor__picker-options` | `test` → `…::test_one_option_menu_has_no_scrollbar_lane` | Obaja's one-chapter menu |
| FR-007 | `static/styles/design/components.css` spec 087 block (unchanged) | `inspection` — `--scroll-thumb`, 5px, no steppers, transparent track | no token drift |
| SC-001 | live geometry probe | `test` → `…::test_scrollport_reaches_menu_edges` | 0px canvas between bar and border |
| SC-002 | live geometry probe | `test` → `…::test_option_and_filter_boxes_are_unchanged` | 0px box delta |
| SC-003 | live geometry probe | `test` → `…::test_one_option_menu_has_no_scrollbar_lane` | 0px lane reserved |
| SC-004 | accepted spec 238 modules | `test` → same two modules as FR-005 | push-step run |
| US1/AC1 | Book menu | `test` → `…::test_scrollport_reaches_menu_edges` | 938/892 vs 937/891 |
| US1/AC2 | Chapter and verse menus | `test` → `…::test_scrollport_reaches_menu_edges_for_all_pickers` | 938/892 and 715/892 |
| US1/AC3 | corner clip | `inspection` — scrolled-to-end bar tip follows the 10px radius in the live preview | manual visual only, not asserted in E2E |
| US1/AC4 | dark / flipped / narrow | `inspection` — same box rule holds in the theme and placement states in the live preview | state reachable by the preview steps |
| US2/AC1 | first book option | `test` → `…::test_option_and_filter_boxes_are_unchanged` | 511,464.1 → 929,503.1 |
| US2/AC2 | chapter filter | `test` → `…::test_option_and_filter_boxes_are_unchanged` | 511,510.1 → 929,548.1 |
| US2/AC3 | one-option menu | `test` → `…::test_one_option_menu_has_no_scrollbar_lane` | no bar, no lane |
| US2/AC4 | interactions | `test` → accepted spec 238 modules | push-step run |

**Verification split**: 14 test · 5 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/244-picker-menu-scrollbar-edge/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/README.md  checklists/requirements.md  checklists/checklist.md
  preview/README.md  analysis.md  converge.md  fold.md
```

### Source

```
static/styles/design/components.css   (picker menu + options rules)
tests/e2e/test_picker_menu_scrollbar_edge.py   (new focused module)
docs/spec/reading.md   (R59 modification at Fold)
backlog/board.md, backlog/items/ITEM-259-*.md   (card and board at Fold)
CHANGELOG.md, VERSION   (delivery commit, after PR number exists)
```

### Structure Decision

The product already owns the popout style in `components.css` and its acceptance tests in
`tests/e2e/`; no new directory or dependency is introduced. The card ID `ITEM-259`, spec number
`244` and patch level `1.37.2` were checked against `origin/develop` and the unmerged local
worktrees before this plan, and are re-checked before merge.
