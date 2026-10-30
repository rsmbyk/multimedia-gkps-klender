# Implementation Plan: the dock fills whatever panel it is given

**Spec**: `specs/164-dock-fluid-width/spec.md`
**Branch**: `fix/164-dock-fluid-width`
**Bump**: `patch` — 1.23.1 → 1.23.2 (the level is declared here; the number is stamped against
`develop` in the pre-merge commit, after the sibling slices in flight)
**Preview**: `live preview at http://127.0.0.1:8799/obs/dock` — `manage.py runserver` from this
slice's worktree against the compose database

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | CSS in `static/styles/design/obs-dock.css`; Playwright (Python) for the acceptance tests |
| Primary dependencies | none added |
| Storage | none — the page renders per request; the display state stays browser-local and untouched |
| Testing | `tests/e2e/test_obs_dock.py`: two new cases and one helper; the module's five existing cases unchanged |
| Target platform | every browser the app supports; the change is plain CSS with no query and no new property |
| Project type | server-rendered Django app, vanilla JS, no build step |
| Performance goals | none; two declarations removed |
| Constraints | no template, model, payload or endpoint change; every box at 560px and below keeps its 1.23.1 value; the picker never fans into columns |
| Scale / scope | one rule in one stylesheet, one test file, one board card |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check does not apply. The
constraint row above stands in its place.

Re-checked after Phase 1: pass — no new file in the product, no new state, no new dependency.

## Phase 0 — Research

See `research.md`. Six decisions, each with its measurement or code read: remove the cap rather than
raise it (D001), keep no container query once the grid is gone (D002), one column recorded as a
requirement (D003), a fill and not a text measure (D004), two E2E cases at fixed viewports (D005), and
the runner out of scope (D006). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the dock's box tree and the three invariants this slice creates.
- `contracts/` — `none` (`contracts/none.md`): no interface changes.
- `quickstart.md` — the DB-isolated module command, the committed probe, the live check, and the
  post-merge check.
- `probe/probe.py` — the measurement the spec's table comes from, runnable as committed.

### The design

**Stylesheet** — `static/styles/design/obs-dock.css`: the `.dock` rule loses `max-width: 560px` and
`margin: 0 auto` and takes `margin: 0`; the comment above it says why the panel is never capped. No
other rule in the sheet carries a width, so nothing else needs a companion change: the head is a flex
row, the body is a block scroller with 8px side padding, and the rows are already `width: 100%`.

**Picker** — nothing to write. `#pickBody` stays `display: block`; its sections are the buckets in
normal flow, so they share one x and one sticky-head line at every width. The slice records that as
FR-003 so a later pass cannot "use" the new width by fanning the list out.

**Runner** — nothing to write; it already filled the panel and its rows are a sequence (D006).

**Tests** — `tests/e2e/test_obs_dock.py` gains `_panel()` (the dock's box at a list of widths) and two
cases: the panel fills at 320/420/560/720/900/1440/1920/2560 with no horizontal overflow, and the
picker stays one column with rows spanning the body's content width at 560/900/1440/1920 and the
bucket head still sticky.

**No template, no JS, no model** — the dock's markup and scripts are untouched.

## Traceability

| Requirement / scenario | Component | Verified by | Evidence |
| --- | --- | --- | --- |
| US1 AC1 — the panel's width is the viewport's | `.dock` | `test` → `test_the_dock_fills_whatever_width_it_is_given` | eight widths |
| US1 AC2 — no strip beside the panel | `.dock` | `test` → the same case | panel x = 0 at each width |
| US1 AC3 — no horizontal scrollbar from the fill | `.dock` | `test` → the same case | `overflow == 0` at each width |
| US2 AC1 — the buckets are stacked, one column | `#pickBody` | `test` → `test_a_wide_dock_keeps_the_picker_in_one_column` | `display: block`, one x |
| US2 AC2 — the name at the left padding, the date at the right | `.servicerow` | `inspection` — row width equals the body's content width and, at 1440, 1424px; the date is the row's last item | `probe/probe.py` |
| US2 AC3 — the bucket head sticks | `.group__head` | `test` → the one-column case | `position: sticky` at each width |
| US3 AC1 — a 420px dock is unchanged | no rule below 560 | `manual` — the probe at 420 (panel 420, row 404) against the spec's 1.23.1 column | `probe/probe.py` |
| US3 AC2 — a 320px dock is unchanged | the same | `manual` — the probe at 320 (panel 320, row 304) | `probe/probe.py` |
| FR-001 — full width and height, no cap, no centring | `.dock` | `test` → the fill case | |
| FR-002 — no horizontal overflow at any width | `.dock` | `test` → the fill case | |
| FR-003 — one column at every width | `#pickBody` | `test` → the one-column case | |
| FR-004 — a row spans the body's content width | `.servicerow` | `test` → the one-column case | row = content width, and viewport − 16 |
| FR-005 — the head keeps sticking | `.group__head` | `test` → the one-column case | |
| FR-006 — nothing else moves | every other rule | `inspection` — the diff is two declarations and one comment in `obs-dock.css`; the module's five existing cases stay green | 18/18 |
| SC-001 — panel = viewport at 320…2560, x = 0 | `.dock` | `test` → the fill case | |
| SC-002 — overflow 0 at those widths | `.dock` | `test` → the fill case | |
| SC-003 — rows 544 / 1424 / 1904 at 560 / 1440 / 1920 | `.servicerow` | `test` → the one-column case | |
| SC-004 — `display: block` and one x at every width | `#pickBody` | `test` → the one-column case | |
| SC-005 — both cases fail on 1.23.1 for the width reason | the suite | `inspection` — the red run recorded in `converge.md` | `panel starts at 170 at 900px`; `row is 544 of 1424px` |

**Verification split: 14 test · 3 inspection · 2 manual.**

## Plan exit gate

| Check | Result |
| --- | --- |
| Requirement coverage | FR-001…FR-006 each carry a row; every SC and every story scenario is mapped |
| Entity coverage | the dock's box tree and its three invariants are in `data-model.md`; no entity added |
| Interface coverage | `contracts/none.md` states `none` and why |
| Decision provenance | D001–D006 in `research.md`, each with its measurement or code read |
| Constitution conformance | no constitution exists (SDD-01); the constraint row is honoured |
| Zero unknowns | 0 |
| Verification declared | 14 `test` · 3 `inspection` · 2 `manual` |
| `quickstart.md` runnable | yes — the module runs on this worktree against a throwaway database, the probe runs as committed, and the post-merge row names its command |

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/164-dock-fluid-width/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md  converge.md  fold.md
  contracts/none.md  checklists/requirements.md  probe/probe.py
```

### Source

```
static/styles/design/obs-dock.css     the .dock rule: no cap, no centring
tests/e2e/test_obs_dock.py            two cases and one helper
docs/spec/reading.md                  the new requirement, at Fold
backlog/items/ITEM-177-dock-fluid-width.md   card
backlog/board.md                      the card's row
specs/README.md                       the spec's index row, at delivery
VERSION, CHANGELOG.md                 patch bump and one line, at delivery
```

### Structure Decision

No new file in the product: the panel already owns the rule that capped it, and the test module that
opens the dock already holds the two cases.
