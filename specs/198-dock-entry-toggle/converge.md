# Converge — spec 198 (2026-11-18)

## Pass 1 — 2026-11-18

**Checked**: all 37 traceability rows against the working tree, grouped by requirement; each row by its
declared method (test, inspection or manual). Every test row runs in the final seven-suite gate unless it
is named below.

| Row | Finding | Type | Outcome |
| --- | --- | --- | --- |
| FR-001 (chevron per state) | T014's presence matrix: exactly one rendered chevron in entries 0/1/2/5; none in the verse-less song, the break or the live row; `node --check` + T016/T017. | `test` | pass |
| FR-002 (a header never projects) | T004/T014: a header click leaves `gkps-display`, `aria-current` and selection untouched; the same assertion runs in the 81-test gate. | `test` | pass |
| FR-003 (morph + chevron flip) | T004 (230 ms, `.is-morph`, 0.2s/curve on the svg) + T014 (no rotation collapsed, 90° matrix open, ≤ 1 px centred in both states) + T015 (`0s`, no animation under reduce); numbers inspected in I1. | `test` + `inspection` | pass |
| FR-004 (items jump) | The seven-suite gate (81 tests) covers every rewired projection path; the matrix fixture exercises the middle screen row of a multi-screen entry. | `test` | pass |
| FR-005 (timing, no scroll, reduce) | I2: `duration = 230`, shared `easeInOut`, per-inner `is-morph`, no scroll/glide in `toggleBlock` → `startToggleMorph` → `finishToggleMorph`; T015: 0 morph windows, sub-frame swap, no inline height. | `test` + `inspection` | pass |
| FR-006 (overrides, crossings, reload) | T006: hand-opened blocks survive the hand-off, the departing entry's state reapplies, the live override is inert, reload forgets; live-locked assertions in T005/T006 re-check green after the rendered-count helper change. | `test` | pass |
| FR-007 (no scroll on toggle) | T004 and T013 assert `runBody.scrollTop` and `aria-current` unchanged across a header click; no scroll call exists in the hand-toggle path (I2). | `test` + `inspection` | pass |
| FR-008 (keyboard + accessible name) | T007 plus `tests.e2e.test_dock_keys` in the final gate: `tabindex="-1"`, `aria-expanded`, `aria-controls` → the inner, name = entry title, panel keeps focus. | `test` | pass |
| FR-009 (mid-crossing queue) | I3: `toggleBlock` records the override before its `morphState` return; `finishMorph` paints both blocks from `effectiveOpenFor` with `keepOutOpen`/`inWasOpen` guards; `sync()` skips morphing inners — the settle is the single writer. The final gate exercises crossings in the overlay and session suites. | `inspection` + `test` | pass |
| FR-010 (break / empty inert) | T014: no chevron node, no display write, no scroll, no gained attributes on either inert header. | `test` | pass |
| FR-011 (hover face) | T014: generic rows tint their whole line (`--icon-hover-bg`) with the chevron inside it; the live row rests on exactly `--sidebar-selected-bg` and never falls back to the generic hover face under the pointer. Baseline `.entryrow[aria-current="true"]:hover` (the 84/16 selected/ink mix) stands unchanged — plan.md:79 maps FR-011 to `.entryrow:hover` (unchanged) and the approved preview reuses that sheet, so "keeps the selected tint" is executed as "keeps the selected family of fill". | `test` | pass — interpretation recorded in tasks.md and analysis.md |
| SC-001…SC-006 | Each maps to the FR tests above; no SC has its own method. | `test` | pass |

**Verification runs**

- Seven rewired E2E suites: **81 tests OK, no skips, 246.9 s** — real run after restoring the container's
  Playwright Chromium and host libraries (both wiped with the old container at the session checkpoint);
  an earlier `OK (skipped=81)` run was discarded as invalid, never counted. This is the post-T018 full run
  analysis A3 called for — T005's live-chevron line is now pinned for real.
- Fast lane (`--exclude-tag=e2e`): 642 tests, **FAILED (failures=11, errors=9)** — 20 reds in songs/tatib/
  media/template/CI-selection modules. A clean-baseline run with this slice's tracked changes stashed
  produced the identical 11/9 set; `multimedia.web.test_obs_dock` passes in both. **No red is attributable
  to spec 198**; fixing them is a separate card's work, not a Converge fix here.
- `manage.py check`: no issues. `manage.py makemigrations --check --dry-run`: no changes detected.
- T019 inspections I1–I3: all three pass against the built code; glyph sweep clean.

**Declared to the owner**

- The fast lane's 20 pre-existing reds (proved identical on the stashed baseline) — tracked separately, not
  an accepted gap of this slice.
- The traceability table's 1 `manual` row (quickstart #4, mid-crossing feel) and the OBS passes
  (quickstart #6/#8) stay the owner's.

**Findings requiring code**: none. **Passes**: 1. Converged.
