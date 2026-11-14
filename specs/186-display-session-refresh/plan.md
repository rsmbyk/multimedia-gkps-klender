# Implementation Plan: a surface re-reads the session it is showing

**Spec**: `specs/186-display-session-refresh/spec.md`
**Branch**: `fix/186-display-session-refresh` (stacked on `feat/185-dock-goto`)
**Bump**: `patch` — 1.26.3 → 1.26.4, applied on top of spec 185's 1.26.2 → 1.26.3. Two slices,
one chain: 186 lands second and takes the next patch (C-SDD-VER's "each landing takes the next value").
**Preview**: `n/a — nothing visible changes` (the spec's `## UI/UX`), and the evidence is the E2E
readouts in `converge.md`.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | JavaScript, ES5-era IIFEs in `static/web/` (no build step). No Python changes. |
| Primary dependencies | none new; `static/web/display-session.js` (spec 184) and the display module it gates. |
| Storage | none added: the re-read calls `read()`, which reads the existing key. |
| Testing | Playwright E2E under `tests/e2e/`, in a new module `test_display_session_refresh.py`. |
| Target platform | OBS's Chromium (CEF) dock panel, the projector window, and the overlay source. |
| Project type | Django app, server-rendered templates plus vanilla JS modules. |
| Performance goals | A focus costs one `read()` and a compare; a focus with no change mutates nothing (SC-003). |
| Constraints | No new key, message, verb or timer (FR-004); the overlay's own re-reads stay (FR-006); "in the same turn" — the repaint starts inside the handler. |
| Scale / scope | 6 requirements, 2 stories, 4 success criteria, 2 JS modules, 1 new E2E module. |

## Constitution Check

No `CONSTITUTION.md`; the standing principles are the repo's own.

| Principle | Status | Note |
| --- | --- | --- |
| The display state is browser-local; its life is the browser session (spec 184) | pass | this makes the *paint* obey the rule the read already enforces |
| One state module, one channel (`display-state`) | pass | the dock gets the re-read through `display.js`'s existing subscribers; nothing is duplicated |
| No new endpoint, storage key or server state | pass | FR-004 |
| Behaviour recorded at Fold | pass | `display-state/R3` |
| Previews from the product's materials, or `n/a` for an invisible change | pass | `n/a` recorded, with the E2E as the evidence |
| No personal names in repo artifacts | pass | roles only |

Re-checked after Phase 1: **pass**.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Two decisions: D001 (the module owns the compare and
the notify) and D002 (the projector gets its own re-read because it does not load `display.js`).

## Phase 1 — Design

- `data-model.md` — `n/a`: the stored shape is untouched; the spec adds no entity.
- `contracts/` — `none`: no interface is added; the module gains one exported function and the
  channel is unchanged (the file says so explicitly).
- `quickstart.md` — the stack, the new module's targeted run, and the manual gesture that shows it.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/display.js` (`reread`), `static/web/projector.js` (`rereadSession`) | `test` → `tests/e2e/test_display_session_refresh.py::test_a_focused_dock_stops_painting_a_refused_state` and `::test_the_projector_stops_painting_a_refused_state` | |
| FR-002 | `static/web/display.js` (`reread`, exported) | `test` → `::test_a_focus_with_the_state_unchanged_repaints_nothing` | the subscriber-notify path |
| FR-003 | `static/web/display.js`, `static/web/obs-dock.js` (`sync`), `static/web/projector.js` (`render`) | `test` → `::test_a_refused_state_leaves_every_control_idle` | live row, block, eye label, transport |
| FR-004 | `static/web/display.js` | `inspection` — the diff adds no `localStorage.setItem`, no `post(` and no message type | |
| FR-005 | `static/web/display.js` (`reread`'s compare) | `test` → `::test_a_focus_with_the_state_unchanged_repaints_nothing` | a `MutationObserver` counts 0 |
| FR-006 | `static/web/obs-overlay.js` | `inspection` — `obs-overlay.js` is unmodified by the branch (`git diff --stat`) | |
| SC-001 | `tests/e2e/test_display_session_refresh.py` | `test` — the dock walk | |
| SC-002 | `tests/e2e/test_display_session_refresh.py` | `test` — the projector walk | |
| SC-003 | `tests/e2e/test_display_session_refresh.py` | `test` — 0 mutations across a focus | |
| SC-004 | `static/web/display.js` | `test` → `::test_the_stored_shape_and_the_messages_are_unchanged` | keys and message types |
| US1/AC1 | `static/web/display.js` (`reread`) | `test` → `::test_a_focused_dock_stops_painting_a_refused_state` | |
| US1/AC2 | `static/web/display.js` (`visibilitychange`) | `test` → `::test_a_visibility_change_stops_painting_a_refused_state` | |
| US1/AC3 | `static/web/display.js` (`reread`'s compare) | `test` → `::test_a_focus_with_the_state_unchanged_repaints_nothing` | |
| US1/AC4 | `static/web/projector.js` (`rereadSession`) | `test` → `::test_the_projector_stops_painting_a_refused_state` | |
| US2/AC1 | `static/web/display.js` (`reread`) | `test` → `::test_a_focus_with_the_state_unchanged_repaints_nothing` | |
| US2/AC2 | `static/web/display.js` (`notify`) | `test` → `::test_a_changed_reread_notifies_a_subscriber_once` | |
| US2/AC3 | `static/web/obs-overlay.js` | `inspection` — unmodified, and its own re-reads still listen | |

**Verification split**: 14 test · 3 inspection · 0 manual.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| No violation | — | — |

## Project Structure

### Documentation

```
specs/186-display-session-refresh/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/  checklists/
```

### Source

```
static/web/display.js      the re-read: compare, then notify; wired to focus, visibility, pageshow
static/web/projector.js    its own re-read, since the page does not load display.js
tests/e2e/test_display_session_refresh.py   the five tests above
```

### Structure Decision

The re-read belongs in the module that owns the state, so the dock (and any future reader that
renders on notification) gets it without a listener of its own. The projector keeps its own copy of
the state module — the page loads `display-session.js` and `projector.js`, not `display.js` — so its
re-read is written there, and the plan says so rather than pretending one module covers both.
