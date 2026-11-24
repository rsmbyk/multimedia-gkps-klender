# Implementation Plan: restore the large entry dialog title band

**Spec**: `specs/240-entry-modal-title/spec.md`
**Branch**: `fix/240-entry-modal-title`
**Bump**: `patch` — `origin/develop` is `1.36.25` after spec 239 landed; our target is
`1.36.26`, applied pre-merge and re-checked then
**Preview**: `specs/240-entry-modal-title/preview/README.md` (live worktree page)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 + Django 4.0 server; vanilla CSS, no script or markup change |
| Primary dependencies | none added; Playwright (Python) supplies user-visible E2E |
| Storage | PostgreSQL for fixtures only; no model, migration or endpoint change |
| Testing | Django runner; Playwright E2E through `StaticLiveServerTestCase` with a throwaway DB |
| Target platform | Text Create/Edit and media Create dialogs at 1440×900 and 390×844, light and dark |
| Project type | Server-rendered Django fragments, `static/styles/design/components.css` |
| Performance goals | none; no new work at runtime |
| Constraints | spec 226's head reset and R10's pinned numbers must both hold |
| Scale / scope | three large dialogs; compact forms and record editors are guards only |

## Constitution Check

No `CONSTITUTION.md` exists at the base commit — the constitution is optional and never
auto-created (SDD-01); the table is empty by absence, not by waiver.

Re-checked after Phase 1: pass — one scoped CSS declaration, no new component,
dependency, interface or runtime behaviour.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no persisted entity; documents the title/head/form box relationship.
- `contracts/none.md` — no HTTP, script, model or event interface change.
- `quickstart.md` — live preview, probe and the three targeted E2E commands.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1 | `components.css` headerless-large selector; `tests/e2e/test_entry_modal_title.py` | `test` → `test_large_entry_titles_have_the_band` | text 26/21px, band 72.5px, 1px rule in three dialogs |
| US1/AC2 | same selector; existing `tests/e2e/test_entry_modal_frame.py` | `inspection` — frame stays 840×760, first field y 133.5 → 174.5px, action row unchanged; probe readout | R10's frame numbers |
| US2/AC1 | spec 226 head selectors; `tests/e2e/test_verse_modal_header.py` | `test` → `test_new_verse_header_has_one_rule` | head `20px 26px 14px`, title padding/border `0px`, one rule |
| US2/AC2 | compact form rules; `tests/e2e/test_entry_modal_frame.py` | `inspection` — passage, song, media Edit and old-item dialogs keep the 480px compact frame and their divided title | no selector matches them |
| US3/AC1 | narrow media query; new title module | `test` → `test_narrow_title_keeps_small_gutters` | text 18/17px, band 64.5px, border 1px at 390px |
| US3/AC2 | `preview/probe.py` | `inspection` — frozen before/after at 1440 and 390px, dark theme, no page scrollbar | gate-1 numbers |
| FR-001 | headerless-large selector | `test` → `test_large_entry_titles_have_the_band` | all three large forms |
| FR-002 | narrow media query | `test` → `test_narrow_title_keeps_small_gutters` | `16px 18px`, divider kept |
| FR-003 | head-bearing selectors | `test` → `test_new_verse_header_has_one_rule` + `test_edit_verse_header_has_one_rule` | spec 226 preserved |
| FR-004 | one CSS diff; `tests/e2e/test_entry_modal_frame.py` | `inspection` — no template, script, loading, sr-only or compact-dialog change; existing module stays green | base red run proves the regression |
| SC-001 | new title module | `test` → `test_large_entry_titles_have_the_band` | 26/21px, 72.5px, 1px |
| SC-002 | verse header module | `test` → two header cases + compact-dialog inspection | zero ruled descendants |
| SC-003 | new title module | `test` → `test_narrow_title_keeps_small_gutters` | 18/17px, 64.5px |
| SC-004 | frame + verse + title modules | `test` → all three modules + probe inspection | narrow lanes only; full suite at push |

**Verification split**: 10 test · 4 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

No violations.

## Project Structure

### Documentation

```
specs/240-entry-modal-title/
  spec.md plan.md research.md data-model.md quickstart.md tasks.md analysis.md
  contracts/none.md checklists/requirements.md checklists/checklist.md
  preview/README.md preview/probe.py
```

### Source

```
static/styles/design/components.css       # scoped headerless-large title rule + narrow override
tests/e2e/test_entry_modal_title.py       # new E2E module for text offsets and the band
tests/e2e/test_entry_modal_frame.py       # existing R10 guard (red on base)
tests/e2e/test_verse_modal_header.py      # existing spec 226 guard
docs/spec/reading.md                      # R10 modified at Fold
backlog/board.md, backlog/items/ITEM-255-* # card opened in this PR
VERSION, CHANGELOG.md                     # patch line at delivery
```

### Structure Decision

The declaration belongs beside spec 226's large selectors: both rules decide the same
band, and the `:not(:has(.editor__head))` test is the only difference between the two
markup shapes. A small E2E module measures the text offset with `Range`, which the
existing frame module does not; the existing frame and verse modules stay as guards.
The preview stays live because the title is inside a fetched form, and the probe's
browser-local override supplies the broken readout without changing served code.
