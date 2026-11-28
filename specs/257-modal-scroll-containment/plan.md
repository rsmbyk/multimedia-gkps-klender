# Implementation Plan: An open modal keeps the scroll to itself

**Spec**: `specs/257-modal-scroll-containment/spec.md` — Accepted at gate 1, 2026-11-28.
**Branch**: `fix/257-modal-scroll-containment` (cut from `origin/develop` at `1cd9f081`)
**Bump**: `patch` — declared here, shown at gate 2, applied only in the pre-merge delivery commit.
**Preview**: live and static, measured before gate 1; values frozen in the spec's `## UI/UX`.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0.1; ES5-style vanilla JS |
| Change surface | `static/styles/design/components.css` only (two rules) |
| Existing patterns | `overscroll-behavior: contain` already used on reading/dock/toast scrollports |
| Storage | none — behaviour derives from `dialog[open]` |
| Testing | `tests.e2e.test_modal_scroll_containment`, Playwright Python via `StaticLiveServerTestCase` |
| Constraints | no dependency, route, schema or JS change; no commit before Fold; no push without a separate word |

## Constitution Check (before Phase 0)

No `CONSTITUTION.md` at the repo root — nothing to check. Complexity Tracking: empty.

## Phase 0 — Research

See `research.md`: thirteen scrollports surveyed, eight decisions D001–D008 with rationale,
alternatives and provenance, zero unknowns. Every candidate rule was measured on the two live
servers before gate 1; no question needed the question tool.

## Phase 1 — Design

`data-model.md` (no state), `contracts/none.md`, `quickstart.md` (runnable probe commands; the E2E
command is marked not-yet-runnable until Implement writes the module). The preview components are the
design: the static page uses the real dialog markup and the real stylesheet from both the base commit
and the worktree, and the live 8765 worktree serves the actual change. No new component is invented.

## Constitution Check (after Phase 1)

Unchanged: still no constitution; no Complexity Tracking entry added.

## Traceability

Verification split: **7 test · 6 inspection · 1 manual**.

| Requirement / scenario | Component | Verified by |
| --- | --- | --- |
| US1/AC1 + FR-001 — editor content at end holds the page | `components.css` `.editor__content`, `:root:has(dialog[open])` | `test` — `tests.e2e.test_modal_scroll_containment.ModalScrollContainmentE2ETests.test_wheel_at_the_end_of_editor_content_leaves_the_document_still` |
| US1/AC2 — Preview body at end holds the page | `.preview__body` | `test` — `…test_wheel_at_the_end_of_preview_body_leaves_the_document_still` |
| US1/AC3 + FR-002 — picker options do not move the editor | `.editor__picker-options` | `test` — `…test_picker_options_at_their_end_do_not_scroll_the_editor` |
| US2/AC1 + FR-003 — zero-range editor passes no scroll | `.editor__content` + root hold | `test` — `…test_short_editor_does_not_scroll_the_document` |
| US2/AC2 — wheel over dialog chrome passes no scroll | `:root:has(dialog[open])` | `test` — `…test_wheel_over_the_editor_header_leaves_the_document_still` |
| US2/AC3 + FR-005 + SC-004 — close restores scrolling and offset | root rule without a JS class | `test` — `…test_closing_the_dialog_restores_document_scrolling_at_the_same_offset` |
| US3/AC1 + FR-004 + SC-002 — every named scrollport computes `contain` and root `hidden` | the ten selectors in `research.md` | `inspection` — `preview/probe.py` computed-style block; `getComputedStyle` on each named scrollport with a dialog open |
| US3/AC2 — nested confirmation holds until the last dialog closes | `dialog[open]` selector | `inspection` — open two dialogs, close one, read root `overflow-y` and the remaining `dialog[open]` |
| SC-001 — red on base, green on slice | the E2E module above | `test` — copy the module into the detached base worktree, run with `GKPS_DB=gkps257base`, then run on the slice with `gkps257` |
| SC-003 — no layout shift | root rule | `inspection` — `preview/geometry.py`, both servers: `clientWidth` 1200 and dialog box 480×100 at (360, 300) |
| UI/UX values still match | frozen table | `inspection` — re-run both probes after the final selector edit and compare to `spec.md` |
| Change scope | one stylesheet | `inspection` — `git diff --name-only 1cd9f081` names only `components.css` (plus the spec pack and board when folded) |
| Research coverage | survey table | `inspection` — thirteen rows, each with a selector and a base value |
| Production confirmation | deployed site | `manual` — open an editor on a scrollable page, wheel past its end and confirm the page behind stays put |

## Plan exit gate (seven checks)

1. Requirement coverage — every FR, SC and story scenario has a row: pass.
2. Entity coverage — `n/a`, no stored entities: pass.
3. Interface coverage — `contracts/none.md`: pass.
4. Decision provenance — D001–D008 each name rationale, alternatives and provenance: pass.
5. Constitution conformance — no constitution, no violations: pass.
6. Zero unknowns — research exit: pass.
7. Verification declared — split above, with file/function or explicit steps: pass. `quickstart.md` has
   runnable probe commands; the E2E command is explicitly marked not-yet-runnable until Implement.

No implementation work is done in Plan and `tasks.md` is not created here after the gate; both were
prepared as the gate-2 materials after the accepted gate-1 pack.
