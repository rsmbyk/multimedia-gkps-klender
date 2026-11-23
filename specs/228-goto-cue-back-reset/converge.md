# Convergence: Back clears the Go To from the cue over an empty stage

**Spec**: `specs/228-goto-cue-back-reset/spec.md`
**Passes**: 3 of 3

## Pass 1 — 2026-11-23

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| none | — | FR-001 … FR-005, SC-001 … SC-003, US1/AC1 … AC5 | Each row checked by its declared method below. |

**Outcome**: zero findings, so no `## Phase N: Convergence` tasks were appended.

### Read-back by declared method

- **test** — the three new cases were red with `goto: null`, `detour: false` and the stale label in
  the cue (`'Matius 5:3 · ' != ''`, `'NKB 43 Sinar Matahari Pagi ·' != ''`). Green after the clear:
  `tests.e2e.test_goto_shared_state` + `tests.e2e.test_dock_goto`, 28 tests, `OK` in 100.736s.
- **test** — live probe at `http://127.0.0.1:8765/projector`: during the Go To the cue reads
  `· HAL 1 Jahowa Sihol Pujionku ·12345671/2 back to service` with seven baits; after the dock's
  Back it reads `·` with no prefix, no flip, zero baits, empty Back and `#cue-next.hidden === true`.
- **inspection** — `git diff` on source touches only `static/web/projector.js` `renderCue()`'s empty
  branch. `leaveDetour()`, `paintIdle()`, `renderDetourCue()`, `display.js`, templates and endpoints
  are byte-identical to the base.
- **inspection** — the three exit paths (`leaveDetour()`, the dock's goto message via
  `applyGoto()`/`paintIdle()`, and `rereadSession()`) all call `renderCue()`, so the clear runs on
  each; spec 227's 2 cases remain green in the 28-test lane.
- **test** — the populated-service cases in the same lane kept their entry labels, baits and next
  control, so the non-empty path did not move.

## Pass 2 — 2026-11-23 (owner revision, same unpushed slice)

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| none | — | FR-006 … FR-009, SC-004 … SC-005, US2/AC1 … AC5 | Each row checked by its declared method below. |

**Outcome**: zero findings, so no `## Phase N: Convergence` tasks were appended; the pack, the
capability delta and the card row were re-folded into the same commit (`git commit --amend`, since
the slice is still local and unpushed).

- **test** — three new cases red: cue text `· != ''` in both empty situations, zone
  `pointerEvents: auto != none`, and `cursor-hidden` still present after 2.3s. Green after the
  `empty-stage` class, the cursor guard and the two CSS rules: 3 cases, `OK` in 9.746s.
- **test** — loaded lane of 39 tests (31 goto, 8 directly touched projector cases): 38 pass.
  `test_quiet_controls_support_keyboard_and_mouse_jumps` fails on a `Control+ArrowRight` step both
  here and on unmodified `develop` (33 tests, identical assertion, 115.366s); it passes alone on the
  slice in 3.591s. Pre-existing load sensitivity, not a regression.
- **inspection** — the source diff is confined to `static/web/projector.js` (`syncEmptyNotice()`,
  `revealCursor()`, `renderCue()`) and `static/styles/design/projector.css` (two scoped rules). No
  template, endpoint, state field or message changed; the spec 227 detour cases stay green.
- **test** — live probe at 8765: `innerText ''`, separator `display: none`, zones
  `pointerEvents: none`, `cursor-hidden false`, body cursor `auto`, keys and service button still
  hit-testable, and a click at (100, 100) enters fullscreen.

## Pass 3 — 2026-11-23 (owner finding, same unpushed slice)

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| none | — | FR-002, US2/AC1 | Checked by the read-back below. |

**Outcome**: converged; the pack and capability delta were amended into the same local commit.

- **test** — two assertions added to the Back and idle-cue cases read `display: flex` before the CSS
  rule and `display: none` after; the 31-test goto lane is `OK` in 110.810s.
- **test** — live probe at 8765: `#cue-next.hidden === true`, computed `display: none`,
  `#cue-arrow` box 0 × 0, cue `innerText ''`.

## Pass 4

Not needed — Pass 3 converged.

## Accepted gaps

None.

## Cap reached

Not reached.
