# Implementation Plan: the dock's entry headers expand and collapse their own block

**Spec**: `specs/198-dock-entry-toggle/spec.md` (Accepted, Gate 1 2026-11-18)
**Branch**: `feat/198-dock-entry-toggle`
**Bump**: `minor` — new operator-facing capability, no interface change, no model change (declared
here for Gate 2; applied pre-merge per VER-04: `VERSION` 1.32.2 → 1.33.0, `CHANGELOG.md`
`[Unreleased]` line at Fold).
**Preview**: static at `specs/198-dock-entry-toggle/preview/index.html` — the approved Gate 1
preview; every state reachable by hand, chevron vertically centred (probe-verified, D008). The
design below follows what was approved.
**Branch base**: `13baf77f` — the branch was fast-forwarded from its cut at `341cf340` on
2026-11-18 (owner's choice at Plan) so red runs are literally against `develop`. Spec 197's delta
is picker CSS above `.entryrow` (+13 lines — the CSS refs below were re-read against the new tip),
one new picker-only test file, and docs; `obs-dock.js` and the seven rewire files are byte-identical
between the refs (analysis A2).

## Technical Context

| Field | Value |
| --- | --- |
| Language / stack | Python 3.12, Django 4.0, DRF; server-rendered template `reading/obs_dock.html`; vanilla JS `static/web/obs-dock.js`; design CSS `static/styles/design/obs-dock.css` + `tokens.css` |
| Surfaces | `obs-dock.js` (`entryRowContent` L148, break early-return L155-161, `buildInner` L250 with divider guard L251 / empty return L274, `renderList` L295-307, `focusPanel` L311, `reduceMotion` L481, `easeInOut` L561-563, `startMorph` L565-604 duration L577 / reduce L588, `finishMorph` L606-624 with the hardcoded out-closed/in-open L615-620, `sync()` inner paint L1118-1133, list click L1168-1188 with the `.entryrow` branch L1182-1187); `obs-dock.css` (`.entryrow` L369-385 baseline L371, `:hover` L386, sticky L390, `.entryinner` L463-488 `.is-open` L470 / `.is-morph` L477 / reduce L486-488, live hover L608); `tokens.css` `--ease` L48 |
| Existing patterns | the crossing hand-off (`startMorph`/`finishMorph`, `easeInOut(t)`, `.is-morph`, 230 ms, reduce branch); `sync()`'s per-`li` repaint loop; `focusPanel()` after every activation; `.iconbtn` stroked-SVG vocabulary; the `reduceMotion.matches` instant-swap idiom |
| Storage | none new — `entryOverrides` is a page-memory `Map`; `gkps-display` untouched |
| Testing | Django runner (`multimedia.web.test_obs_dock`); Playwright (Python) E2E under `tests/e2e/`, tag `e2e`; red-first per TDD against `develop` (`13baf77f`) |
| Target platform | the dock runs in OBS's browser source; also any Chromium/Firefox/Safari the operator opens it in |
| Performance goals | none new — one class flip, one `hidden` flip and one attribute per `li` per repaint; no fetch, no layout beyond the measured block height |
| Constraints | no keyboard binding (A9); `tabindex="-1"` stays; no persistence; no broadcast; no display-state write from a header; no scroll/glide on toggle; no plus/minus glyph; chevron vertically centred (`align-self: center`, D008) |
| Scale / scope | one script, one stylesheet, one E2E file's fixtures+methods, seven files' projection rewire (17 click sites); ~70 lines JS, ~35 CSS, 8 new test methods, no template/model change |

## Constitution Check

`CONSTITUTION.md` is absent — SDD-01 makes it optional and never auto-created. The check runs
against the binding constraints the capability specs and `docs/PROCESS.md` impose.

| Constraint | Status | Note |
| --- | --- | --- |
| The display state never reaches the server, and a header writes nothing | pass | the toggle calls no `gkpsDisplay.write`, sends no channel message, touches no model or endpoint; the toggle tests assert the stored shape byte-identical after a header click |
| The panel keeps the keyboard (dock R10) | pass | header stays `tabindex="-1"`; activation calls `focusPanel()`; no new binding (A9) |
| No framework, no new dependency | pass | hand-written JS/CSS only, reusing the crossing's curve, class and reduce idiom |
| Existing accepted numbers undisturbed | pass | row `min-height: 38px`, sticky pin `top: -4px`, `--ease` 200 ms, fluid width (spec 164), re-read (spec 195) all keep their rules; the chevron adds a child, not a box |
| Names in repo artifacts | pass | roles only; the accessible name stays the entry title (A5) |
| One behaviour truth | pass | the dock's own page is the truth; the preview is static and says so |
| GIT-06 / GIT-07, VER-03 / VER-04 | pass | nothing committed before Fold; nothing pushed without the owner's word; the minor bump is declared here and applied pre-merge |

Re-checked after Phase 1: pass — the only post-Gate-1 addition is D008's centring declaration
(`align-self: center`), which adds no constraint and changed no row above.

## Phase 0 — Research

See `research.md` (D001-D011). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no model changes; the one new state is the page-memory `entryOverrides` map;
  `.entryinner` gains an `id` for `aria-controls`.
- `contracts/` — **none** (client-only slice; the only new attribute contract is internal to one
  document — stated in `contracts/README.md`).
- `quickstart.md` — serve, the three test lanes, the eight manual checks, honest limits.

## Traceability

Every `FR-###`, `SC-###`, story scenario and edge case, with its component and how it is
verified. `test` names the file and method; `inspection` names what is read (I1-I3, defined in
`tasks.md` Phase 6); `manual` gives steps in `quickstart.md`.

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `obs-dock.js` `renderList` chevron build (D002) + `sync()` presence | `test` → `tests/e2e/test_obs_dock.py::test_the_chevron_marks_the_state_and_the_eligible_rows` | chevron on every non-break, non-empty, non-live header; none on live/break/empty; bbox centred in the row |
| FR-002 | `obs-dock.js` list click `.entryrow` branch → `toggleBlock` (D004/D005) | `test` → `::test_the_header_toggles_its_block_and_never_projects` | no write, no scroll, no `aria-current`; live / break / empty clicks are no-ops |
| FR-003 | `obs-dock.js` chevron SVG; `obs-dock.css` `.entrychev` (D007/D008) | `inspection` → I1 | viewBox `0 0 20 20`, stroke 1.7 round, 15 × 15, `currentColor`, rotation 0°→90° `var(--ease)` 200 ms, `align-self: center` (probe offset 0), no plus/minus glyph |
| FR-004 | `obs-dock.js` handler — screen row / band / chips / transport only (D009) | `test` → `::test_browsing_does_not_project_and_a_screen_row_click_does` | headers removed from the trigger set; the screen-row path is today's |
| FR-005 | `obs-dock.js` `toggleBlock` + `.is-morph` reuse (D004) | `inspection` → I2 | 230 ms, `easeInOut(t)` reuse, `.is-morph` suppression, reduce branch, no scroll call; behaviour split: normal path in the toggle test, reduce in `::test_the_toggle_swaps_instantly_under_reduced_motion` |
| FR-006 | `obs-dock.js` `entryOverrides`/`effectiveOpen` + `sync()` paint (D003) | `test` → `::test_open_blocks_survive_crossings_and_forget_on_reload` | override survives crossings and repaints; live-locked; reload forgets |
| FR-007 | `obs-dock.js` `toggleBlock` (no `centerRow`/`glideScroll`/cursor) | `test` → `::test_the_header_toggles_its_block_and_never_projects` | `runBody.scrollTop` and `aria-current` asserted unchanged; no screen row selected by opening |
| FR-008 | `obs-dock.js` header attributes + `focusPanel()` (D006) | `test` → `::test_the_header_keeps_the_panel_keyboard_and_the_title_name` | `tabindex="-1"`, `aria-expanded` matches state, `aria-controls` → `#entryinner-<n>`, name = entry title, panel keeps focus |
| FR-009 | `obs-dock.js` mid-crossing branch + `finishMorph` settle (D005/D010) | `inspection` → I3 | record-and-return when `morphState` names the inner; settle paints effective state with `keepOutOpen`/arrival guards; feel → manual (quickstart #4) |
| FR-010 | `obs-dock.js` `buildInner` null → no chevron (D002) | `test` → `::test_the_chevron_marks_the_state_and_the_eligible_rows` | break + verse-less-song fixtures; their header clicks are no-ops |
| FR-011 | `obs-dock.css` `.entryrow:hover` (unchanged) + chevron inside the row | `test` → `::test_the_chevron_marks_the_state_and_the_eligible_rows` | hover tint covers the whole header incl. the chevron; live hover keeps the selected tint |
| SC-001 | as FR-001/FR-010 | `test` → `::test_the_chevron_marks_the_state_and_the_eligible_rows` | DOM count vs the entry list |
| SC-002 | as FR-002/FR-005 | `test` → `::test_the_header_toggles_its_block_and_never_projects` | morph + attribute flips + untouched state |
| SC-003 | the rewired projection path (D009) | `test` → suite run (tasks T013) + `::test_browsing_does_not_project_and_a_screen_row_click_does` | all seven rewired files green; the projection path itself untouched |
| SC-004 | live / break / empty no-ops | `test` → `::test_the_live_header_is_locked_open_and_chevronless` (break/empty half in the chevron test) | no write, no morph, no class change |
| SC-005 | override survival (D010) | `test` → `::test_open_blocks_survive_crossings_and_forget_on_reload` | a crossing never reopens a closed block; the live entry never collapses |
| SC-006 | suites + red-first | `test` → red runs at Implement + the fast lane and E2E suites | each new test fails against `13baf77f` for the toggle reason, not an import |
| US1/AC1 | FR-002, FR-005 | `test` → `::test_the_header_toggles_its_block_and_never_projects` | opens over 230 ms, attributes flip, no write |
| US1/AC2 | FR-005 | `test` → `::test_the_header_toggles_its_block_and_never_projects` | closes again; nothing projected |
| US1/AC3 | FR-002 live half | `test` → `::test_the_live_header_is_locked_open_and_chevronless` | block stays open, `aria-current` stays, no write |
| US1/AC4 | FR-006 | `test` → `::test_open_blocks_survive_crossings_and_forget_on_reload` | hand-opened block stays open through the crossing |
| US1/AC5 | FR-007 | `test` → `::test_open_blocks_survive_crossings_and_forget_on_reload` | multi-open; no other block closes |
| US2/AC1 | FR-004 | `test` → `::test_a_screen_row_inside_projects_that_screen` | that exact screen on air, `aria-current` moves |
| US2/AC2 | FR-008 (closed half) | `test` → `::test_a_screen_row_inside_projects_that_screen` | closed block `aria-hidden="true"` + inert; nothing clickable until opened |
| US2/AC3 | FR-004 (band) | `test` → `::test_a_screen_row_inside_projects_that_screen` | the Next band projects its screen, unchanged |
| US2/AC4 | FR-004 | `test` → `::test_browsing_does_not_project_and_a_screen_row_click_does` | no `gkps-display` write, no `OBS-*` message from a header |
| US3/AC1 | FR-003 | `test` → `::test_the_chevron_marks_the_state_and_the_eligible_rows` | right-pointing at rest, ink via `currentColor` |
| US3/AC2 | FR-003 | `test` → `::test_the_chevron_marks_the_state_and_the_eligible_rows` | rotation follows the state (reduce instant → `::test_the_toggle_swaps_instantly_under_reduced_motion`) |
| US3/AC3 | FR-001 live rule | `test` → `::test_the_live_header_is_locked_open_and_chevronless` | no chevron on the live row |
| US3/AC4 | FR-010 | `test` → `::test_the_chevron_marks_the_state_and_the_eligible_rows` | break and empty render none |
| US3/AC5 | FR-005 reduce | `test` → `::test_the_toggle_swaps_instantly_under_reduced_motion` | Playwright `reduced_motion` context: instant, no `is-morph` |
| US3/AC6 | FR-006 / A2 | `test` → `::test_open_blocks_survive_crossings_and_forget_on_reload` | reload: overrides gone, only the live block open |
| Edge: override inert while live | FR-006 | `test` → `::test_open_blocks_survive_crossings_and_forget_on_reload` | departing entry's stored state re-applies |
| Edge: mid-crossing toggle | FR-009 / D005 | `manual` — quickstart #4 | timing lives in a human hand |
| Edge: break / empty click | FR-010 | `test` → `::test_the_chevron_marks_the_state_and_the_eligible_rows` | no toggle, no projection, no write |
| Edge: non-live header shows chevron | FR-001 | `test` → `::test_the_chevron_marks_the_state_and_the_eligible_rows` | right at rest, down when open |
| Edge: screen-row click keeps the block open | FR-006 | `test` → `::test_a_screen_row_inside_projects_that_screen` | the live hand-off, not the click, decides after a crossing |

**Verification split**: `33 test · 3 inspection · 1 manual`. Manual steps live in `quickstart.md`;
the `test` rows are written red-first — each fails against `develop` (`13baf77f`) for the toggle
reason, not an import (SC-006) — before their implementation task runs. The one deliberate
exception is the projection rewire (D009): it is semantics-neutral on both trees and is verified
green on `develop` at its own task, so the suite never sits red between phases.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| `toggleBlock` re-measures and steps the height instead of reusing `startMorph` | `startMorph` is a two-block hand-off with scroll centring; the toggle is one block and FR-007 forbids any scroll — sharing would couple the toggle path to the crossing path and risk R3 | sharing the function (couples two motions that must stay independent); CSS-only transition (different curve, unmeasured ends) |
| The seven suites' projection helpers become two clicks (expand → screen row) | under FR-004 the header cannot project, so the operator's real path is two clicks; the pair lands the same end state on both trees (D009) | writing `gkpsDisplay.write` directly (bypasses the projection path SC-003 pins as bit-for-bit); a JS test hook (tests the hook, not the dock) |

## Project Structure

### Documentation

```
specs/198-dock-entry-toggle/
  spec.md  plan.md  research.md  data-model.md  quickstart.md
  contracts/README.md                (none — stated there and in data-model.md)
  checklists/requirements.md  preview/index.html
  tasks.md  analysis.md  converge.md  fold.md      ← later stages
```

### Source

```
static/web/obs-dock.js            + entryOverrides/effectiveOpen (D003), chevron build in
                                  renderList + sync presence/aria-expanded paint (D002),
                                  toggleBlock (D004), handler .entryrow branch (D009's JS half),
                                  finishMorph effective paint + guards (D010), buildInner id (D006)
static/styles/design/obs-dock.css + .entrychev: flex none, margin-left auto, align-self center,
                                  15×15 stroked SVG, rotate 90° on [aria-expanded="true"],
                                  transform var(--ease), reduce instant, [hidden] display none
tests/e2e/test_obs_dock.py        + fixture eligibility matrix, 7 new methods, 1 renamed+flipped
tests/e2e/test_display_session.py         rewire 3 header-click sites (D009)
tests/e2e/test_display_session_refresh.py rewire 1 (_project helper)
tests/e2e/test_dock_goto.py               rewire 3
tests/e2e/test_dock_keys.py               rewire 4
tests/e2e/test_obs_overlay.py             rewire 4 (_project helper + 3 inline)
tests/e2e/test_obs_overlay_wrap.py        rewire 1 (_project helper)
multimedia/web/test_obs_dock.py   unchanged (server side untouched)
reading/obs_dock.html             unchanged (already links both files)
```

### Structure Decision

The slice touches exactly the script, the stylesheet and the tests. No template edit is needed:
`obs_dock.html` already links both files. No new directory, no new dependency, no new module: the
toggle is a behaviour of the runner the way the crossing already is. The rewire is test-only and
deliberately lands before the handler change (Foundational) so the seven suites stay green
throughout the run.
