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

## Pass 2 — 2026-10-30, after the rebase onto develop (1.25.0)

The branch was cut at 1.22.11 and replayed onto `develop` at `f36dc2db` (1.25.0) before delivery. The
replay met three facts the base had taken after the spec was accepted:

- **`projector/R3` was claimed.** `R3` now names *the projector's image placeholder appears only when
  the image fails* (spec 157), and the file carries `R1`–`R11`. This slice's requirement is **`R12`**
  in every artifact — spec, plan, research, analysis, checklist, tasks, this file and `fold.md` — and
  it is folded as `R12`. No requirement the owner accepted changed; the identifier did, and the
  rename is stated rather than silent.
- **The sheet gained `Image and PDF`.** Spec 158 added a one-row group to the middle column between
  `Library Detour` and this slice's groups, holding `T` — `Fit Width / Fit Height` — which `Display`
  used to carry. The template and the sheet's test now read the middle column as `Library passage`,
  `Library Detour`, `Image and PDF`, `Audio`, `Video`; the sheet holds **twelve** groups, not the
  eleven the spec's edge case counted, and the two this slice adds are unchanged.
- **The box still holds.** `preview/measure.py` on the rebuilt preview — `today` is the base's own
  sheet, `after` the slice's — reads 1920×1080: 1123.4 × 676.1px → 1094.4 × 676.1px; 1280×720:
  676.1px → 675.8px against a 688px limit, `scrollHeight` 675, nothing scrolls. Pitch 34px, heading
  21.5px, group gap 24px, column gap 32px and sheet padding 20px 24px are unchanged; the middle
  column runs 459.2 → 618.2px, still shorter than the 634.2px the tallest column sets.

| Row | Type | Evidence | Outcome |
| --- | --- | --- | --- |
| FR-001…FR-003 | none | the new case, re-run green on the rebased tree; `Display` holds its three rows | matches |
| FR-004 | none | `Image and PDF` sits between `Library Detour` and `Audio`; the two groups still end the middle column, after every group that was there when the spec was accepted | matches |
| FR-005 | none | the measurements above; the diff names one template (+8/−1), two test modules, the board, the spec index and the pack | matches |
| FR-006, SC-004, US2 AC1–AC4 | **gap closed** | the four E2E cases the plan deferred ran green on the rebased tree (below); the handler is still absent from the diff | verified |

## Accepted gap closed

The four E2E cases the plan deferred to the push step ran on 2026-10-30 and passed:

- `tests/e2e/test_audio_display.py::AudioDisplayE2ETests::test_projector_space_navigation_and_reset`
- `tests/e2e/test_video_display.py::VideoDisplayE2ETests::test_projector_fullscreen_play_pause_and_navigation_guard`
- `tests/e2e/test_projector.py::ProjectorE2ETests::test_the_keyboard_moves_and_turns_the_display_on_and_off`
- `tests/e2e/test_projector.py::ProjectorE2ETests::test_f_and_k_toggle_fullscreen_and_shortcut_sheet`

The module run is green as well: `multimedia.web.tests.ServiceProjectorTests` and
`multimedia.web.test_media`, 61 tests.

## Outcome

**Converged**, the accepted gap closed. Passes used: 2 of 3.

- Folded: FR-001…FR-005 and the sheet's scenarios → `docs/spec/projector.md` R12.
- Nothing about the keys is folded as a change: the sheet's description of them is what R12 states,
  and the behaviour itself is unchanged — the four E2E cases prove it.

## Delivery split

`tasks.md`'s T010 stays open by design: `VERSION` (1.25.0 → 1.25.1) and the `CHANGELOG.md` line are in
the Fold commit with the card `in-progress`; the card's `In review` move, its `pr:` and the board's
`In review` row follow the push, where the PR number exists, and `done`, `closed_at`, `closed_reason`
and the board's `Done` row happen in the closing chore after the merge. A card claiming a merge before
one happened would be the defect BRD-05 names.
