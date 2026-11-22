# Implementation Plan: the Copy as template confirmation is a layer of the edit modal

**Spec**: `specs/212-copy-confirm-layer/spec.md`
**Branch**: `fix/212-copy-confirm-layer`
**Bump**: `patch` (1.35.2 → 1.35.3)
**Preview**: `static preview at specs/212-copy-confirm-layer/preview/index.html`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | CSS (hand-written, no preprocessor), Python 3.12, Django 4.0 |
| Primary dependencies | none new; Playwright (Python) already in the E2E lane |
| Storage | no schema change, no data touched |
| Testing | `manage.py test tests.e2e.test_tatib_templates` with `DJANGO_DEVELOPMENT_MODE=true` |
| Target platform | server-rendered reading app; the editor `<dialog>` at 480px |
| Project type | Django app, vanilla JS shell, hand-written design sheets |
| Performance goals | none — 15 lines of CSS, no new fetch, no new script |
| Constraints | no markup change; no JS change; no change to the generate page's confirmation; no new token |
| Scale / scope | one block in `components.css`; two E2E tests; one capability requirement |

## Constitution Check

No `CONSTITUTION.md` exists in this repo (SDD-01); the check is recorded as not applicable.

Re-checked after Phase 1: not applicable — no principles to violate.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Six decisions, each with its provenance: where the rules
live (D001), which design's numbers they carry (D002), the scrim's radius (D003), the verification seam
(D004), no motion (D005), and the `[hidden]` restatement (D006).

## Phase 1 — Design

- `data-model.md` — no entity added, changed or removed.
- `contracts/` — **none**: the slice changes no request, no response, no route and no template. The
  form markup `_copy_confirm.html` already emits every element the rules attach to.
- `quickstart.md` — the focused E2E command, the preview probe, and what each prints.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/styles/design/components.css` | `test` → `tests/e2e/test_tatib_templates.py::test_the_copy_confirmation_covers_the_form` | layer rect equals the dialog's rect; dialog height equal before and after |
| FR-002 | `static/styles/design/components.css` | `test` → `tests/e2e/test_tatib_templates.py::test_the_copy_confirmation_covers_the_form` | `elementFromPoint` at the form Save's centre is inside the layer |
| FR-003 | `static/styles/design/components.css` | `test` → `tests/e2e/test_tatib_templates.py::test_the_copy_confirmation_card_matches_the_preview` | 448 × 176.3 ± 1, padding 22px, radius 12px, canvas fill, shadow present |
| FR-004 | `static/styles/design/components.css` | `test` → `tests/e2e/test_tatib_templates.py::test_the_copy_confirmation_card_matches_the_preview` | heading 18px/650, body 13.5px, actions `flex-end` with an 8px gap |
| FR-005 | `static/styles/design/components.css` | `test` → `tests/e2e/test_tatib_templates.py::test_the_copy_confirmation_covers_the_form` | layer radius 14px; `hidden` re-set after Cancel → `display: none` |
| FR-006 | `static/web/editors.js`, `_copy_confirm.html` | `test` → `tests/e2e/test_tatib_templates.py::test_copy_as_template_asks_and_copies` | unchanged: the existing copy test must stay green |
| SC-001 | `static/styles/design/components.css` | `test` → `…::test_the_copy_confirmation_covers_the_form` | `height` before/after equal to a tenth of a pixel |
| SC-002 | `static/styles/design/components.css` | `test` → `…::test_the_copy_confirmation_covers_the_form` | layer box equals dialog box; the hit test names the confirmation |
| SC-003 | `static/styles/design/components.css` | `test` → `…::test_the_copy_confirmation_card_matches_the_preview` | the preview's numbers, asserted against the shipped page |
| SC-004 | `static/styles/design/components.css` | `test` → `…::test_the_copy_confirmation_card_matches_the_preview` | accept button's right edge 22px inside the card's; 8px gap |
| US1/AC1–AC4 | `static/styles/design/components.css` | `test` → the two tests above | the four scenarios are the assertions' Given/When/Then |
| US2/AC1–AC3 | `static/styles/design/components.css` | `test` → `…::test_the_copy_confirmation_card_matches_the_preview` | card box, type scale and actions row |
| US2/AC3 | `static/styles/design/components.css` | `inspection` — the preview's **Dark** toggle: card and scrim take the dark `--canvas` and `--backdrop` because no rule names a colour | tokens only |
| Edge: narrow dialog | `static/styles/design/components.css` | `inspection` — the preview resized to 380px, card capped by `min(468px, 100%)` inside 16px padding | recorded in `## UI/UX` |
| Edge: generate page unchanged | `static/styles/design/generate.css` | `test` → existing `test_a_fill_in_and_a_choice_settle_then_create` | the scoping in D001 is what protects it |

**Verification split**: 13 test · 2 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/212-copy-confirm-layer/spec.md
specs/212-copy-confirm-layer/plan.md
specs/212-copy-confirm-layer/research.md
specs/212-copy-confirm-layer/data-model.md
specs/212-copy-confirm-layer/quickstart.md
specs/212-copy-confirm-layer/tasks.md
specs/212-copy-confirm-layer/analysis.md
specs/212-copy-confirm-layer/converge.md
specs/212-copy-confirm-layer/fold.md
specs/212-copy-confirm-layer/contracts/README.md
specs/212-copy-confirm-layer/checklists/requirements.md
specs/212-copy-confirm-layer/preview/index.html
specs/212-copy-confirm-layer/preview/candidate.css
specs/212-copy-confirm-layer/preview/probe.py
specs/212-copy-confirm-layer/preview/README.md
```

### Source (modified)

```
static/styles/design/components.css   +15 lines, after .editor__confirm
tests/e2e/test_tatib_templates.py     +2 tests, in TataIbadahTemplateE2ETests
docs/spec/reading.md                  +R47 (Fold)
CHANGELOG.md                          one line under ## [Unreleased]
VERSION                               1.35.2 → 1.35.3
backlog/board.md, backlog/items/ITEM-226-copy-confirm-layer.md
```
