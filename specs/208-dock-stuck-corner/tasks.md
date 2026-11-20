# Tasks: the live entry header's corners follow its pin state

**Spec**: `specs/208-dock-stuck-corner/spec.md` · **Plan**: [./plan.md](./plan.md)
**Bump**: `minor` (two new dock capabilities).

## Phase 1 — Setup

- [x] **T001** Take over the empty `fix/208-dock-stuck-corner` worktree, fast-forward it to the
  current `develop` (`c385a194`), and confirm the spec number, ITEM-219 and the preview port are free.
  (PASS — 0/0 to base at `c385a194`, no spec folder or PR, port 8767 free.)
- [x] **T002** Write `run-tests.sh` against a throwaway `gkps208` database, inheriting the compose
  web container's own `DATABASE_URL` so credentials are never written into the file.
  (PASS — module and full dock suites run without touching the shared test database.)

## Phase 2 — US1: the top corners follow the pin state

- [x] **T003** Write the six top-corner E2E pins in `tests/e2e/test_dock_stuck_corner.py` and run
  them RED on the unmodified base. (PASS — six red at the intended assertions.)
- [x] **T004** Add an unguarded `updateStuck()` and wire it to scroll frames, sync, every glide and
  morph frame and landing, block toggles and resize; remove the toggle from `updateBand()`.
  (PASS — 6/6 green; `node --check` clean.)
- [x] **T005** Prove before/after with the per-frame probe: develop 328/328 pinned frames
  mismatched, slice 0/328. (PASS — counts recorded in the spec's `## UI/UX`.)

## Phase 3 — US2–US4: the bottom pin, the band and the click act

- [x] **T006** Write the bottom-pin E2E pins (faithful copy, no-doubling, per-frame, click act,
  reduced motion) and run RED. (PASS — red at the intended assertions.)
- [x] **T007** Add the list-level `.liveband-slot` holding a faithful clone of the live header,
  clipped when its bottom reaches the Next band's top, stacked directly above the band.
  (PASS — 11/11 module after the US4 iterations.)
- [x] **T008** Move the Next band to a list-level slot, always shown while a next entry exists,
  and make the list fill the scrollport so the band pins flush even when every entry fits.
  (PASS — 1920×1200 band 1033–1068 = the edge; 420×860 band 693–728.)
- [x] **T009** Fold in the owner's live rulings in order: stack above the band, faithful clone
  (no caption), click re-centres and returns to following, always-visible band, band-top clip.
  (PASS — each ruling E2E-backed; superseded rulings kept in the spec's Revision.)

## Phase 4 — Polish

- [x] **T010** Run the full dock regression: `test_obs_dock`, `test_dock_open_reset`,
  `test_obs_dock_follow`, `test_dock_text_wrap`, `test_dock_stuck_corner`.
  (PASS — 67 tests, OK; the one intermittent chevron settle-wait error is the pre-existing
  machine-local ITEM-220, reproduced on the unmodified base.)
- [x] **T011** Fold `dock/R17` and `dock/R18` into `docs/spec/dock.md` and write `fold.md`.
  (PASS — 16 → 18 rules, one header update.)
- [x] **T012** Update `CHANGELOG.md` and bump `VERSION` to 1.35.0 (minor, declared at Plan);
  mark ITEM-219 and ITEM-221 in review with the PR link. (PASS — see PR.)
- [x] **T013** Re-read the preview states against the shipped code and keep the screenshots under
  `preview/shots/`. (PASS — full-fit and staged/band-contact states verified.)

**Summary**: T001–T013 complete; 12 E2E pins green, 67/67 full dock regression green.
