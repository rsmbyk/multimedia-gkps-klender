# Converge: Audio and video name their play/pause key

**Pass 1** — 2026-10-29, after Implement's green run.

## What was checked

Every row of `plan.md`'s traceability table against the tree, by the method the row declares. The
code was read after the run rather than trusted from the task ticks (SDD-22).

## Findings

| Row | Type | Evidence | Outcome |
| --- | --- | --- | --- |
| FR-001, FR-002 | none | `test_the_shortcuts_sheet_names_audio_and_video_in_groups_of_their_own` green; the running worktree page at `127.0.0.1:8840/projector` lists `Audio` and `Video` in column 2, each 55.5px tall with one `Play/Pause` row | matches |
| FR-003 | none | the same case asserts `Display`'s three rows and the absence of `Audio/Video Play/Pause`; the page's HTML holds the string zero times | matches |
| FR-004 | none | the same case asserts the columns `[Service, Song, Passage] · [Library passage, Library Detour, Audio, Video] · [Display, Find, While Finding, Fullscreen]` | matches |
| FR-005 | none | `git diff --stat` names one template (+8/−1), two test modules, the board and the specs index; `preview/measure.py` prints 676.1px before and after on the preview and the live page reads 676.5px in both states; column 2 is 380 → 539.3px | matches |
| FR-006 | none | `static/web/projector.js` is absent from `git diff --name-only`; the key handler at `:1254-1260` is the one that shipped | matches |
| US1 AC1–AC2 | none | the new case; live page | matches |
| US1 AC3 | none | live page at 1280×720: sheet 1095 × 676.5px, `scrollHeight` 675, window limit 688 — fits, nothing scrolls | matches |
| US1 AC4 | none | live page at 1920×1080: sheet 1095 × 676.5px, groups 300.5 / 160.5 / 125.5 / 300.5 / 55.5 / 55.5 / 55.5 / 125.5 / 90.5 / 195.5 / 90.5 | matches |
| US2 AC1–AC4 | **accepted gap** | the four E2E cases are declared in the plan and are not run in this slice — the owner's standing rule defers heavy suites to the push step (analysis F3). The handler is not in the diff | deferred, as declared |
| Edge cases | none | a shorter window keeps `max-height` + `overflow: auto` (`projector.css:461-466`); the column stays 379px wide; no CSS is in the diff, so no hover state and no motion changed | matches |
| SC-001, SC-002, SC-003 | none | the new case and the two measurements above | matches |
| SC-004 | **accepted gap** | as US2 — the depending E2E cases run at the push step; the handler is untouched | deferred, as declared |

No `missing`, `partial`, `unrequested` or `contradicts` row was found. The two deferred rows are the
same gap analysis F3 recorded before code, not a new one.

## Outcome

**Converged with accepted gaps.** Passes used: 1 of 3.

- Folded: FR-001…FR-005 and the sheet's scenarios → `docs/spec/projector.md` R3.
- Not folded, accepted: nothing about the keys, because the sheet's description of them is what R3
  states and the behaviour itself is unchanged — the E2E cases prove the behaviour, and they run at
  the push step.

## Delivery split

`tasks.md`'s T010 stays open by design: `VERSION` (1.22.10 → 1.22.11) and the `CHANGELOG.md` line
landed in the Fold commit with the card set `in-progress`, and the card's `In review` move, its
`pr:`, `done`, `closed_at`, `closed_reason` and the board's `Done` row happen at the push and the
closing chore, where the PR number exists and the merge is fact. A card claiming a merge before one
happened would be the defect BRD-05 names.
