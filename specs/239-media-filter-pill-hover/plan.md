# Implementation Plan: Media Library filter-pill hover

**Spec**: `specs/239-media-filter-pill-hover/spec.md`
**Branch**: `feat/239-media-filter-pill-hover`
**Bump**: `patch` — `origin/develop` is `1.36.23` at Plan; re-checked before the pre-merge delivery commit
**Preview**: `specs/239-media-filter-pill-hover/preview/README.md` (live worktree page, gate 1 accepted)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 + Django 4.0 server; vanilla CSS/HTML, no JavaScript change |
| Primary dependencies | none added; Playwright (Python) supplies user-visible E2E |
| Storage | SQLite for the local dev preview; no model, migration or endpoint change |
| Testing | Django test runner; Playwright E2E through `StaticLiveServerTestCase`; heavy suite at push only |
| Target platform | The Media Library filter row in light and dark themes at desktop and narrow widths |
| Project type | Server-rendered Django template; single rule in `static/styles/design/components.css` |
| Performance goals | none; no new work at runtime |
| Constraints | One CSS rule; no template, script, token or endpoint edit; no `@media (hover: hover)` wrapper |
| Scale / scope | Six buttons in `.media-library__chips`; untouched elsewhere |

## Constitution Check

No `CONSTITUTION.md` exists at the base commit — the constitution is optional and never
auto-created (SDD-01), so the table is empty by absence, not by waiver.

Re-checked after Phase 1: pass — no new component, dependency, interface or runtime behaviour.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no persisted entity; documents the filter-row boxes and the two theme tokens.
- `contracts/README.md` — `none`: no HTTP, script, model or event interface changes.
- `quickstart.md` — live preview, probe and targeted E2E path.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1 | `.media-library__chips button:not([aria-pressed="true"]):hover` in `static/styles/design/components.css`; `tests/e2e/test_media_filter_pill_hover.py` | `test` → `test_all_unpressed_pills_take_the_hover_pair` | six pills, both themes, real mouse hover |
| US1/AC2 | same selector and module | `test` → `test_pointer_leave_restores_rest_colours` | transparent + `--divider` after moving away |
| US1/AC3 | same selector and module | `test` → `test_hover_keeps_box_and_label` | 63.36 × 30 px, label colour unchanged |
| US2/AC1 | pressed rule and same module | `test` → `test_pressed_pill_keeps_its_accent_fill` | fill/border/text identical under pointer |
| US2/AC2 | existing global focus-visible rule; same module | `test` → `test_keyboard_focus_keeps_its_outline` | 2px `--focus` outline, 2px offset |
| US2/AC3 | `.media-library__chips` box geometry | `inspection` — frozen gate-1 readouts: 63.36 × 30 px across rest, hover and pressed; row gaps unchanged | no geometry declaration in the new rule |
| FR-001 | new hover selector in `components.css` | `test` → `test_all_unpressed_pills_take_the_hover_pair` | border and background only |
| FR-002 | existing `[aria-pressed="true"]` rule | `test` → `test_pressed_pill_keeps_its_accent_fill` | hover selector excludes pressed pills |
| FR-003 | single-rule diff | `inspection` — diff shows two declarations and no label, dot, filter or focus change | `media-library.js` and the template untouched |
| FR-004 | single-file diff | `inspection` — only `components.css` changes; no other pill or control selector touched | dock chips keep their own rules |
| SC-001 | new E2E module | `test` → `test_all_unpressed_pills_take_the_hover_pair` | base has no hover rule and fails |
| SC-002 | new E2E module | `test` → `test_pressed_pill_keeps_its_accent_fill` | pressed values frozen from gate 1 |
| SC-003 | gate-1 probe | `inspection` — widths/heights 63.36 × 30 px and label colour identical in all three states | no new box metrics |
| SC-004 | gate-1 probe | `inspection` — light/dark readouts in `spec.md §UI/UX` agree after the rule | same rule reads both theme tokens |

**Verification split**: 9 test · 5 inspection · 0 manual

## Plan exit gate (SDD-14)

| Check | Result |
| --- | --- |
| Requirement coverage — every FR/SC/story scenario traced | pass — 14 rows above |
| Entity coverage — boxes and tokens named | pass — `data-model.md` |
| Interface coverage — explicit `none` | pass — `contracts/README.md` |
| Decision provenance — every D has rationale, alternatives, provenance | pass — `research.md` |
| Constitution conformance — no constitution, no violations | pass — both checks above |
| Zero unknowns | pass — `research.md` ends at 0 |
| Verification declared — every row has a method and runnable path | pass — split 9/5/0; `quickstart.md` |

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

No violations.

## Project Structure

### Documentation

```
specs/239-media-filter-pill-hover/
  spec.md plan.md research.md data-model.md quickstart.md
  contracts/README.md checklists/requirements.md checklists/checklist.md
  preview/README.md preview/probe.py
```

### Source

```
static/styles/design/components.css                  # one hover rule in the chips row
tests/e2e/test_media_filter_pill_hover.py             # new E2E module (written at Implement)
docs/spec/media-library.md                            # R6 added at Fold
backlog/board.md, backlog/items/ITEM-254-*            # card opened in this PR
VERSION, CHANGELOG.md                                 # patch line at delivery
```

### Structure Decision

The rule sits beside the existing base and pressed pill rules in `components.css`:
that keeps the rest, hover and pressed states in one cascade, with the `:not([aria-pressed])`
guard making the selected state immune at equal specificity. A new E2E module keeps
the colour and box evidence together; existing media-library tests cover filtering, not
hover painting. The preview stays live because the page and its theme tokens are
server-rendered, and `probe.py` freezes the before/after numbers from that same page.
