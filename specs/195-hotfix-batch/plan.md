# Implementation Plan: Production hotfixes — 2026-11-15

**Spec**: `specs/195-hotfix-batch/spec.md` (Accepted, Gate 1 2026-11-15)
**Branch**: `fix/195-hotfix-batch`
**Preview**: static at `specs/195-hotfix-batch/preview/index.html`; live click paths in `preview/README.md`
**bump**: `patch` — six user-visible fixes, no new capability, no interface change (declared at gate 2; applied pre-merge per VER-04).

## Technical Context

| Field | Value |
| --- | --- |
| Language / stack | Python 3.12, Django 4.0; server-rendered templates, vanilla JS sheets in `static/web/`, design CSS in `static/styles/design/` |
| Surfaces | `components.css` (US1, US2, US4 styling), `date-picker.js` + `reading.js`'s `shell:page` seam (US3), `entries.js`/`views.py`/`entries.py` (US4), `obs-overlay.js` + `obs-overlay.css` (US5, US6), `obs-dock.js` (US6) |
| Existing patterns | the date-hide-on-reveal rule (spec 190) at `components.css:1425`; spec 167's preview CSS block for the edit-modal header; `gkpsDisplay.subscribe` / BroadcastChannel verbs (specs 119/185); the projector page's screen/entry islands as the one painted truth |
| Testing | Django `manage.py test` (targeted); Playwright (Python) E2E for user-visible acceptance where a test row declares it; heavy runs deferred to the push step |

## Constitution Check

| Constraint | Status | Note |
| --- | --- | --- |
| Verse IDs remain the stored contract (spec 189) | pass | US4 aligns the client to it; nothing writes numbers |
| Empty-verses refusal stays (spec 162/R30) | pass | server-side refusal untouched |
| A lyric that fits paints at the accepted numbers (R2) | pass | fit only runs when the block exceeds two lines |
| The display state never reaches the server | pass | US6 adds no state write, no model change, no new endpoint |
| No framework, no new dependency | pass | all six fixes are hand-written CSS/JS/Django |
| Names in repo artifacts | pass | roles only |

## Research summary (full: `research.md`)

- D001 the lyric fit is a measured JS loop, not CSS (`min()` cannot count visual lines)
- D002 the re-read discovery is a timed re-read of the projector islands — no revision endpoint, no schema change, no write path can be missed
- D003 the verses contract aligns client-side (submit IDs); the server keeps refusing an empty checklist
- D004 US2's CSS is spec 167's accepted preview block ported verbatim; the base title's 34px right pad (spec 006) is superseded inside the head
- D005 the badge hide joins the date-hide rule it mirrors (same media guard, same reveal set)
- D006 `date-picker.js` binds on `shell:page` (the reading shell's own seam) over the whole document; the per-picker ready guard makes rescans cheap

## Data model

No model changes. `ServiceEntry.verses` keeps storing verse IDs; the picker's submitted values align to it. `contracts/` states `none` — every interface touched is the project's own client↔server pair (`entry_song_verses` JSON, the projector islands), consumed only by this repo's scripts.

## Traceability

| Requirement | Component / file | Verified by |
| --- | --- | --- |
| FR-001 (US1 badge hide) | `components.css` 1425–1428 block | `inspection` + preview state |
| FR-002 (US2 header + button) | `components.css` (editor modal block), values from spec 167 preview | `inspection` + computed-style check |
| FR-003 (US3 picker on both paths) | `date-picker.js` (`shell:page`), `reading.js` seam | `test` (new E2E, run at push) + `manual` (both paths) |
| FR-004 (US4 id contract end to end) | `views.py entry_song_verses`, `entries.js renderVerses/verseSummary`, `entries.py` widget | `test` (view + form + widget) + `manual` (save flow) |
| FR-005 (US4 checklist parity) | `components.css` `.editor__verses` block | `inspection` + `manual` |
| FR-006 (US4 preserved states) | `tatib/models.py` clean, spec 162 view path | `test` (existing + one added) |
| FR-007 (US5 two-line fit) | `obs-overlay.js` `fitCaption`, resize refit | `manual` (overlay fixture, measured) |
| FR-008 (US6 re-read everywhere) | `obs-overlay.js`, `obs-dock.js` | `manual` (two-surface live check) + `inspection` |

**Verification split**: `4 test · 2 inspection · 6 manual`. Manual rows give steps in `quickstart.md`; the E2E row (US3) is written here but run at the push step, per standing instruction.

## Quickstart

See `quickstart.md` — commands for the worktree server, the targeted test runs, and the two-surface US6 check.
