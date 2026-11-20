# Tasks: opening a service starts its entry blocks shut

**Spec**: `specs/204-dock-entry-open-reset/spec.md`
**Plan**: `specs/204-dock-entry-open-reset/plan.md`
**Verification split**: 30 test · 1 inspection · 0 manual (the plan's traceability table is the
row-level source; this file carries one task per row it can act on)

Ordered by user story. `[P]` means order-independent, not concurrent — one agent, one thread; the
run states the order it used.

**Red-first applies to US1 only, and that is declared, not assumed.** US1's six tests assert the
new reset, so each is run against the base `ab46f384` (the slice's changes stashed) and must fail
because a non-live block stands open after an open — not on an import, a selector or a fixture.
US2's and US3's rows pin behaviour that is **unchanged** by this slice (a crossing keeps a
hand-opened block, a re-read keeps it, an open writes nothing and paints no morph): those tests are
green on the base and must stay green on the slice, so they are regression pins, not red-first
rows. One statement serves every story, so US1's green task is the single implementation task; the
later phases add pins and re-runs, not more code.

## Phase 1 — Setup

- [x] T001 `tests/e2e/test_dock_open_reset.py` — the module and its fixtures, in
  `test_obs_dock_follow.py`'s shape: `StaticLiveServerTestCase`, `@tag('e2e')`,
  `skipUnless(HAS_PLAYWRIGHT)`, `@override_settings(STATICFILES_STORAGE=…StaticFilesStorage)`;
  two services built in `setUp` before the browser starts — `Ibadah Panjang` with 12 entries
  (a passage with verses, a song with baits, a media entry, a `SECTION_BREAK`, text entries) and
  `Ibadah Pendek` with 5 — plus the helpers `_dock`, `_open_service`, `_block`, `_raw`,
  `_wait_state`, `_opens` (the painted open/non-live/live index lists).

## Phase 2 — Foundational

- [x] T002 the red-first lane: run `tests.e2e.test_dock_open_reset` against the base with the
  slice's tree stashed, and record each failure's reason in `converge.md`'s first pass — the
  assertion must be the open block, never an import or a missing selector (SC-007).

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: an explicit open of a service starts every block shut but the live entry's.
**Independent test**: expand position 4 in the long service, open the short one — nothing open;
re-open the long one — nothing open; put position 4 on air and return — only that block open.

- [x] T003 [P] [US1] red test `test_an_open_starts_every_block_shut_in_another_service`
  (US1/AC1, FR-001, FR-003 click, SC-001) in `tests/e2e/test_dock_open_reset.py`.
- [x] T004 [P] [US1] red test `test_reopening_the_same_service_starts_every_block_shut`
  (US1/AC2, SC-002) in the same module.
- [x] T005 [P] [US1] red test `test_several_hand_opened_blocks_leak_nothing_into_a_shorter_service`
  (US1/AC3, SC-003) — three hand-opens at indices 1, 3, 8, then the 5-entry service.
- [x] T006 [P] [US1] red test `test_the_live_entrys_block_stays_open_when_its_service_is_opened`
  (US1/AC4, FR-002, SC-004) — project index 3, open the other service, return; assert open,
  `aria-current="true"`, chevron count 0, and every other block shut.
- [x] T007 [P] [US1] red test `test_a_browsed_service_has_no_open_block_while_another_is_on_air`
  (US1/AC5) — with the long service on air, open the short one: nothing live there, nothing open.
- [x] T008 [P] [US1] red tests `test_the_keyboard_open_resets_like_a_click` (picker `Enter`,
  FR-003) and `test_the_on_load_open_keeps_only_the_live_block` (reload with a service on air,
  FR-003, US1/AC6) in the same module.
- [x] T009 [US1] **green**: `static/web/obs-dock.js` `openService()` L418 — one
  `entryOverrides.clear();` before the service's data is reassigned, with a comment naming the
  rule and the two events that must NOT clear it (research D001/D002/D003). No other line changes.
- [x] T010 [US1] re-run the module: all six US1 tests green; record the output.

## Phase 4 — US2 (P1)

**Goal**: the reset does not reach a crossing, a re-read or a reload's existing rule.
**Independent test**: with a block open by hand, project another entry and trigger a re-read — the
block stands open through both; reload — every override is gone.

- [x] T011 [P] [US2] pin `test_a_reread_keeps_a_hand_opened_block_open` (US2/AC2, FR-003, SC-005)
  in `tests/e2e/test_dock_open_reset.py`: hand-open a block, post `{type:'update'}` on
  `gkps-service-display`, wait for the re-read, assert the same open indices and the same
  `scrollTop`. Green on the base and on the slice.
- [x] T012 [US2] re-run unchanged
  `tests/e2e/test_obs_dock.py::ObsDockE2ETests::test_open_blocks_survive_crossings_and_forget_on_reload`
  (US2/AC1, US2/AC3, FR-004, FR-006, SC-005) — spec 198's pin, not edited.

## Phase 5 — US3 (P2)

**Goal**: the reset is silent — no write, no broadcast, no morph, and the on-air open still centres.
**Independent test**: open a service with the state watched byte-for-byte and the channel listened
to — nothing changes; sample the new list's frames — no `.is-morph`, no scroll movement.

- [x] T013 [P] [US3] pin `test_an_open_writes_no_display_state_and_broadcasts_nothing`
  (US3/AC2, FR-005, SC-006) in `tests/e2e/test_dock_open_reset.py`: raw `gkps-display` bytes before
  and after an open, with a `BroadcastChannel` listener counting messages.
- [x] T014 [P] [US3] pin `test_an_open_paints_no_morph_in_the_new_list` (US3/AC1, FR-005, SC-006):
  a `requestAnimationFrame` sample across the open counting `.entryinner.is-morph` and reading
  `runBody.scrollTop` — zero morph frames, no scroll jump.
- [x] T015 [US3] re-run unchanged
  `tests/e2e/test_obs_dock_follow.py::ObsDockFollowE2ETests::test_opening_the_service_on_air_enters_following`
  (US3/AC3) — spec 200's pin, not edited.

## Phase 6 — Polish

- [x] T016 [P] the inspection row (FR-006, no new storage): grep the slice's diff for
  `localStorage`, `sessionStorage`, `document.cookie`, `fetch(` and any endpoint path — the only
  added statement is the `Map.clear()`; record the grep and its result in `converge.md`.
- [x] T017 [P] the preview parity pass: `diff static/web/obs-dock.js
  specs/204-dock-entry-open-reset/preview/assets/obs-dock.js` must show only the preview's gate
  wrapper around the same clear; re-run `preview/probe.py`, `probe_open_write.py` and
  `probe_enter_path.py` and confirm the drafted numbers are unchanged (64 states, 0 errors,
  10 opens byte-identical, `Enter` path `[]`).
- [x] T019 [P] the empty-service edge test
  `test_an_empty_service_opens_without_a_block_or_an_error` in `tests/e2e/test_dock_open_reset.py`
  — an open of a service with no entries draws no rows, raises no page error and resets nothing.
  Green on the base and on the slice (a pin, not a red-first row); the plan carries its row.
- [x] T018 the targeted suite lane: `manage.py test tests.e2e.test_dock_open_reset
  tests.e2e.test_obs_dock tests.e2e.test_obs_dock_follow tests.e2e.test_dock_keys
  tests.e2e.test_dock_goto tests.e2e.test_dock_bucket_head multimedia.web.test_obs_dock --keepdb`
  on a throwaway database (SC-007). A red identical on the base is proven there under the same
  command and carded, never silently accepted. The full browser matrix stays at the push step.

## Phase 7 — Convergence

Converge pass 1 (`converge.md`): 30 test rows run, 1 inspection row clean, preview parity
confirmed. **Converged** — no `missing`/`partial`/`contradicts`/`unrequested` finding, one pass, no
cap. The lane's two reds were proven identical on the base with the change stashed and are carded
as `ITEM-215`; C1 and C2 were fixed mechanically and are recorded there.

## Phase 8 — Fold and delivery

- [x] T020 `docs/spec/dock.md` — Fold the typed delta into R14 (the override's lifetime: an explicit
  open ends it; the crossing and re-read rules stand), move `last folded` and prepend the slice id;
  write `fold.md` with the operations and the before/after counts.
- [x] T021 `converge.md` — the passes, their evidence and the outcome; `analysis.md` re-run after
  any mechanical fix.
- [X] T022 the delivery commit (pre-merge, VER-04): `VERSION` to the base's next patch,
  `CHANGELOG.md` `[Unreleased]` line, `backlog/items/ITEM-216-…md` (`bump: patch`, `branch`, `pr`
  when it exists) and the `backlog/board.md` row — all in one commit, with the suite green.
- [X] T023 the closing report: what shipped, the verification split, convergence and any accepted
  gap, the folded capability, the branch and commit count, the version and changelog line, the PR
  title and body, that nothing is pushed — then ask about pushing.

## Notes on order

The run uses T001 → T002 → T003…T008 (the six red tests, in that order) → T009 → T010 → T011 →
T012 → T013 → T014 → T015 → T016 → T017 → T019 → T018 → Converge → T020…T023. `[P]` tasks are
order-independent but were run sequentially in one thread.
