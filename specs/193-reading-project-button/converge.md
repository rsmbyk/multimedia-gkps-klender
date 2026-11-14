# Converge — Project button on the song and Bible pages

## Pass 1 — 2026-11-14

**Scope**: `plan.md`'s traceability table (FR-001…FR-008, US1/US2 ACs, SC-001…SC-006).
**Method**: every row checked by its declared method — tests run, inspection rows read off the
running pages, the manual row left for the owner's live review.

### What was checked

| Traceability row | Result |
| --- | --- |
| FR-001 song page control | `test` — `ReadingViewTests::test_song_page_draws_project_control` green; E2E clicks it |
| FR-002 chapter control, right of the switch | `test` — `test_bible_chapter_draws_project_control_beside_the_switch` green (order asserted); E2E writes the chapter pointer |
| FR-003 song pointer, no reset | `test` — E2E `test_clicking_project_writes_the_song_pointer`, `test_repeat_click_keeps_the_detours_place` green |
| FR-004 chapter pointer, verse 1, edition | `test` — E2E `test_clicking_project_writes_the_chapter_pointer`, `test_sim_page_projects_sim` green |
| FR-005 window act, never Stop | `test` — E2E `test_one_click_opens_the_projector_window_once` green; popup-blocked `checked by inspection` (the Go To write precedes the window act, which returns on a falsy handle) |
| FR-006 composes with dock/R1 | `test` — E2E `test_back_returns_to_the_service` green (service adopted, Back restores, detour gone); picker-alone semantics untouched (`test_goto_shared_state` 10/10) |
| FR-007 not drawn where it has nothing to say | `test` — `test_project_control_is_absent_where_it_has_nothing_to_say` green (verse-less song, book landing, Bible landing); ≤720px `checked by inspection` (the rule joins `components.css:3202`'s existing hide) |
| FR-008 fetches only a different Go To | `test` — E2E `test_repeat_click_makes_no_second_fetch` green (route count = 1); a genuinely different pointer still fetches (the boot ride in T017 applies it) |
| SC-001…SC-006 | covered by the rows above; SC-005 `checked by inspection` against `dock/R1` scenarios |
| US1/AC5, US2/AC4 (survives the stage swap) | `test` — E2E `test_the_control_survives_in_page_navigation` green (same document asserted) |
| Owner's live review | `manual` — pending, offered with the closing report |

### Findings

| # | Type | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | partial (made whole) | FR-005/FR-006 were only partial on a **cold open**: the projector's boot adopted a service from the stored state asynchronously and the adoption's fetch wiped the detour the boot's own `applyGoto()` had painted while in flight, so with a service on air the freshly opened window could land on the service instead of the detour. The accepted spec requires the cold open to show the detour with the service preserved underneath (US1/AC2, FR-006). Code was at fault → the boot now re-applies the stored Go To after the adoption settles (`bootRidesGoto`, T017). Reproduced by the failing E2E, then green. | task appended (T017), done |
| 2 | stale path | The plan named `tests.e2e.test_saved_render_parity`, which no longer exists — spec 136 removed the offline library and the parity surface with it. The parity concern is moot for this slice: the offline renderer draws no project controls and the spec forbids adding any. | task T013 text corrected; nothing to run |
| 3 | unrequested (evidence note) | The combined projector suite run shows 14 non-green tests (`test_projector`, `test_goto_shared_state`). Re-run against unmodified `develop` at `9a556a99` (`gkps-check190`, throwaway DB `gkps190`): **13 of 14 byte-identical failures, pre-existing**; the 14th (`test_the_dock_follows_a_goto_started_on_the_projector`) passed alone and with its whole module (10/10) on this branch — a load flake from two suites sharing one machine. Zero regressions introduced. | documented, no action |
| 4 | partial (made whole) | T007/T009's render pins were written after the templates rather than strictly before the code for those two tasks (the E2E reds T002–T004/T010 preceded everything; the pins followed). Noted here rather than hidden: the behaviour-level red/green cycle held for every acceptance row; the pin tasks were verification of already-tested markup. | documented |

### Outcome

**Converged** — every traceability row holds by its declared method; both `partial` findings were
made whole in this pass; the `stale path` was corrected; the `unrequested` row is an evidence note.
Pass 2 was not needed. Fold follows.
