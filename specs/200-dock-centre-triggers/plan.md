# Implementation Plan: the dock follows the live entry only when following

**Spec**: `specs/200-dock-centre-triggers/spec.md` (Accepted, Gate 1 2026-11-18)
**Branch**: `feat/200-dock-centre-triggers`
**Bump**: `minor` — a new operator-facing control and a new following mode, no interface or model
change (declared here for Gate 2; applied pre-merge per VER-04 with the changelog line at Fold).
**Preview**: static at `specs/200-dock-centre-triggers/preview/index.html`, the approved Gate 1
artifact; the design below follows its measured numbers, not a reinterpretation.
**Branch base**: `16a7da8a` (`develop` at cut). No rebase or fast-forward has been performed since.

## Technical Context

| Field | Value |
| --- | --- |
| Language / stack | Python 3.12, Django 4.0, DRF; server-rendered `multimedia/web/templates/reading/obs_dock.html`; vanilla `static/web/obs-dock.js`; design CSS `static/styles/design/obs-dock.css` + `tokens.css` |
| Surfaces | `obs-dock.js`: `dock` state object (`:38`), `liveNode` (`:612`), `glideScroll`/`layoutTop`/`centerRow`/`scheduleCenter` (`:560–626`), `startMorph`/`finishMorph` (`:640–708`), `cancelPendingCenter` + wheel/pointerdown (`:774–782`), `updateBand` (`:786`, sets `nextBand.dataset.screen = next.start`), `toggleBlock` (`:764`), `sync` (`:1197–1319`, subscribe at `:1831`), `step`/`stepUnit`/`projectScreen`, `entryList` click (`:1330`), prev/next handlers (`:1441–1442`), 100 ms re-read poll (`:1852`) |
| Existing patterns | the 230 ms `easeInOut` crossing morph with `.is-morph` and hand-managed `inert`/`aria-hidden`; the 190 ms quintic ease-out glide; `reduceMotion.matches` instant branches; `navbtn` stroked-SVG markup; `tabindex="-1"` panel-owned keyboard; `focusPanel()` after activation |
| Storage | none new — `following`, the previous-notice snapshot and the idle clock are page memory; `gkps-display` is read only |
| Testing | Django runner; Playwright (Python) E2E under `tests/e2e/` with `StaticLiveServerTestCase`, fixtures in `setUp`, ORM assertions after the browser closes; red-first per TDD. Heavy browser suites run at the push step |
| Target platform | OBS's embedded browser dock first; any current Chromium/Firefox/Safari opening `/obs/dock` |
| Performance goals | one extra boolean comparison per state notice, one ~100 ms interval tick, one extra button; no new fetch, no new layout measurement beyond the existing glide |
| Constraints | no server state, no channel message, no new display field, no persistence of the mode; `tabindex="-1"` and the panel-owned keyboard stay; the preview's numbers are frozen at gate 1 |
| Scale / scope | one template, one script, one new E2E file (14 methods), no CSS change, no model or endpoint change; ~90 lines JS, ~10 lines HTML |

## Constitution Check

`CONSTITUTION.md` is absent — SDD-01 makes it optional and never auto-created. The check runs
against the binding constraints in `docs/spec/dock.md`, `docs/PROCESS.md` and the accepted spec.

| Constraint | Status | Note |
| --- | --- | --- |
| Display state stays browser-local and is never extended for a UI-only concern | pass | D001 keeps `following`, the snapshot and the clock in page memory; `display.js` is untouched |
| The panel keeps the keyboard (dock R10) | pass | `#centreBtn` carries `tabindex="-1"`; its click calls `focusPanel()`; no new key binding |
| Header clicks never project or scroll (dock R14) | pass | `toggleBlock` gains only a mode write; no `centerRow`, no `projectScreen` |
| Existing accepted numbers are undisturbed | pass | D008 keeps the glide, morph, clamp, sticky row and `navbtn` metrics; no CSS added |
| One behaviour truth | pass | the static preview is the gate-1 artifact and says so; the dock's own page is the implementation truth |
| No framework, no new dependency | pass | hand-written JS and the product's own SVG vocabulary (D009) |
| No person's name in repo artifacts | pass | roles and requirements only |
| GIT-06 / GIT-07, VER-03 / VER-04 | pass | no commit before Fold, no push without the owner's word; `minor` declared here and stamped pre-merge |

Re-checked after Phase 1: **pass** — the design adds one DOM button, one page-memory flag, one
notion snapshot and one interval; none of them touches the display record, the keyboard contract,
the accepted geometry or a server interface.

## Phase 0 — Research

See `research.md` (D001–D010). **Unknowns remaining: 0.** The decisive ones: D002 recognises an
advance from a same-service/goto, changed-screen notice at the single `subscribe` fan-in; D003 lets
the crossing morph run height-only in browsing; D004 narrows the clock to scroll, press and key.

## Phase 1 — Design

- `data-model.md` — three page-memory entities (following mode, previous notice, idle clock), no
  database change.
- `contracts/` — **none**; client-only slice, stated in `contracts/README.md`.
- `quickstart.md` — the venv/compose setup, the E2E lane, six manual checks, and the honest limits.

## Traceability

Every FR, SC, story scenario and edge case, with the component and how it is verified. `test`
names a method in `tests/e2e/test_obs_dock_follow.py`; `inspection` names I1–I3 below; `manual`
names M1–M3 in `quickstart.md`.

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `obs_dock.html` `.navpair` + `obs-dock.css` `.navbtn` (D008/D009) | `inspection` → I1 | one control between prev and next, 40 × 40, radius 10, 10 px gap |
| FR-002 | `#centreBtn` click → `centre()` + `following = true` | `test` → `test_the_centre_control_centres_and_enters_following` | 190 ms quintic ease-out glide, clamped, instant under reduce, no display write |
| FR-003 | `sync()` paints `centreBtn.disabled` (D009) | `test` → `test_the_control_is_disabled_without_a_live_row_and_centres_a_goto` | no live row → disabled; go-to marked row is still a target |
| FR-004 | `entryList` click screen-row/band branch + `syncLivePos` (D006) | `test` → `test_an_item_click_centres_and_reenters_following` | item click centres and re-enters following |
| FR-004 (band) | `updateBand()`'s `dataset.screen` + band branch | `test` → `test_the_next_band_jumps_the_pointer_and_reenters_following` | pointer jumps to the next entry, first row marked |
| FR-005 | `toggleBlock()` mode write; header click unchanged (D005) | `test` → `test_scrolling_and_expanding_another_entry_end_following` | opens a block, ends following, no centre |
| FR-006 (following) | `sync()` notice comparison (D002) + `startMorph(…, carry=true)` (D003) | `test` → `test_advances_follow_when_following_and_not_when_browsing` | every advance path centres, including across entries |
| FR-006 (browsing) | same discriminator + `startMorph(…, carry=false)` | `test` → `test_advances_follow_when_following_and_not_when_browsing` | screen changes, `scrollTop` and mode do not |
| FR-006 (transport) | prev/next handlers call `step()` only | `test` → `test_advances_follow_when_following_and_not_when_browsing` | Next and Back never change the mode |
| FR-007 | idle interval + document listeners (D004) | `test` → `test_the_idle_elapse_centres_and_reenters_following` | 15 s, six conditions, scroll/press/key only, re-entry |
| FR-008 | conditions read in the firing tick | `test` → `test_each_idle_condition_holds_the_centring_back` | one condition false at a time → no move |
| FR-009 | `visibilitychange` branch of the clock | `test` → `test_each_idle_condition_holds_the_centring_back` | hidden page never fires; visible restarts |
| FR-010 | `cancelPendingCenter` unchanged (D007) | `test` → `test_centring_stays_one_motion_and_clamps_at_the_ends` | wheel/pointerdown cancels the glide, mode unaffected |
| FR-011 | `following = true` initialiser (D001) | `test` → `test_advances_follow_when_following_and_not_when_browsing` | load follows; first notice never centres |
| FR-012 | `runBody` wheel listener + `toggleBlock` (D005) | `test` → `test_scrolling_and_expanding_another_entry_end_following` | two exits, neither centres itself |
| FR-013 | `sync()` guard `state.service === dock.service`, no go to | `test` → `test_the_dock_does_not_follow_a_service_it_is_not_showing` | picker/other service/go to → no centre |
| FR-014 | notice discriminator's screen-unchanged branch (D002) | `test` → `test_other_state_notices_never_centre` | display switch, re-read, reload, open, go-to rows, layer close |
| SC-001 | glide target + go-to fallback (D008/D009) | `test` → `test_the_centre_control_centres_and_enters_following` | ≤1 px off centre after settle; band moves the pointer |
| SC-002 | discriminator + browse guard | `test` → `test_advances_follow_when_following_and_not_when_browsing` | `scrollTop` identical before/after each browse advance |
| SC-003 | condition gate at fire time | `test` → `test_each_idle_condition_holds_the_centring_back` | six false states, one all-true |
| SC-004 | glide + morph frame sampling (D003/D008) | `test` → `test_centring_stays_one_motion_and_clamps_at_the_ends` | no direction reversal before the settle |
| SC-005 | `reduceMotion.matches` branches | `test` → `test_reduced_motion_jumps_instead_of_gliding` | instant, no glide, all triggers |
| SC-006 | document listeners + `holding` tick (D004) | `test` → `test_the_clock_counts_scrolls_presses_and_keys_but_not_pointer_movement`, `test_a_held_press_suspends_the_clock` | pointer move keeps counting; held press suspends |
| SC-007 | all transitions (D001–D006) | `test` → `test_advances_follow_when_following_and_not_when_browsing` | follow → browse → re-entry → follow |
| US1/AC1 | `obs_dock.html` + `.navbtn` | `inspection` → I1 | middle control, same face and height as the arrows |
| US1/AC2 | centre click | `test` → `test_the_centre_control_centres_and_enters_following` | glides to centre, no write/selection change |
| US1/AC3 | reduce branch | `test` → `test_reduced_motion_jumps_instead_of_gliding` | instant in reduced motion |
| US1/AC4 | `centreBtn.disabled` | `test` → `test_the_control_is_disabled_without_a_live_row_and_centres_a_goto` | disabled, press is a no-op |
| US1/AC5 | `liveNode()` off-body fallback (D009) | `test` → `test_the_control_is_disabled_without_a_live_row_and_centres_a_goto` | go-to marked row centred |
| US1/AC6 | centre click from browsing | `test` → `test_the_centre_control_centres_and_enters_following` | following again; next advance centres |
| US1/AC7 | Next from browsing | `test` → `test_advances_follow_when_following_and_not_when_browsing` | mode unchanged, list still |
| US2/AC1 | item click path | `test` → `test_an_item_click_centres_and_reenters_following` | projects and centres |
| US2/AC2 | item click, same entry | `test` → `test_an_item_click_centres_and_reenters_following` | glide to the new live screen row |
| US2/AC3 | item click, crossing | `test` → `test_an_item_click_centres_and_reenters_following` | crossing morph carries the scroll |
| US2/AC4 | sticky band branch | `test` → `test_the_next_band_jumps_the_pointer_and_reenters_following` | band projects the next entry's first screen |
| US2/AC5 | header click | `test` → `test_scrolling_and_expanding_another_entry_end_following` | toggles, ends following, never centres |
| US2/AC6 | re-entry from browsing | `test` → `test_the_next_band_jumps_the_pointer_and_reenters_following` | band re-enters following |
| US3/AC1 | idle fire | `test` → `test_the_idle_elapse_centres_and_reenters_following` | all six conditions true → glide |
| US3/AC2 | other header open | `test` → `test_each_idle_condition_holds_the_centring_back` | still, timer keeps running |
| US3/AC3 | layer open | `test` → `test_each_idle_condition_holds_the_centring_back` | still |
| US3/AC4 | words hidden / go to | `test` → `test_each_idle_condition_holds_the_centring_back` | still |
| US3/AC5 | live row on screen | `test` → `test_each_idle_condition_holds_the_centring_back` | still |
| US3/AC6 | picker / other service | `test` → `test_each_idle_condition_holds_the_centring_back` | still |
| US3/AC7 | clock events | `test` → `test_the_clock_counts_scrolls_presses_and_keys_but_not_pointer_movement` | zero on each event |
| US3/AC8 | pointer movement | `test` → `test_the_clock_counts_scrolls_presses_and_keys_but_not_pointer_movement` | count does not restart, elapse still centres |
| US3/AC9 | held press | `test` → `test_a_held_press_suspends_the_clock` | suspended until release |
| US3/AC10 | hidden page | `test` → `test_each_idle_condition_holds_the_centring_back` | no fire; restart on show |
| US3/AC11 | idle re-entry | `test` → `test_the_idle_elapse_centres_and_reenters_following` | following after the glide |
| US4/AC1 | following advances | `test` → `test_advances_follow_when_following_and_not_when_browsing` | centres every step, crossing included |
| US4/AC2 | open blocks / dark display | `test` → `test_advances_follow_when_following_and_not_when_browsing` | neither breaks following |
| US4/AC3 | browsing advances | `test` → `test_advances_follow_when_following_and_not_when_browsing` | no move, mode stays browsing |
| US4/AC4 | browsing after expansion | `test` → `test_scrolling_and_expanding_another_entry_end_following` | no move |
| US4/AC5 | sticky band re-entry | `test` → `test_the_next_band_jumps_the_pointer_and_reenters_following` | centres and follows |
| US4/AC6 | service not on air | `test` → `test_the_dock_does_not_follow_a_service_it_is_not_showing` | no centre |
| US4/AC7 | other notices | `test` → `test_other_state_notices_never_centre` | no move, no glide |
| US4/AC8 | exit by scroll/expand | `test` → `test_scrolling_and_expanding_another_entry_end_following` | mode leaves, no centre itself |
| Edge: no own row | `liveNode()` fallback | `test` → `test_the_centre_control_centres_and_enters_following` | blank-only entry centres its label row |
| Edge: item-click crossing | D003 carry flag | `test` → `test_an_item_click_centres_and_reenters_following` | one motion to the middle |
| Edge: control during crossing | glide vs morph ownership | `manual` → M1 | crossing finishes; no second motion |
| Edge: already centred | glide no-op | `test` → `test_centring_stays_one_motion_and_clamps_at_the_ends` | no visible move |
| Edge: clamped at list ends | glide clamp | `test` → `test_centring_stays_one_motion_and_clamps_at_the_ends` | geometry wins |
| Edge: unsigned pointer | D004 | `test` → `test_the_clock_counts_scrolls_presses_and_keys_but_not_pointer_movement` | still idle |
| Edge: press held through 15 s | D004 holding | `test` → `test_a_held_press_suspends_the_clock` | suspended, restarts on release |
| Inspection I1 | markup + stylesheet | `inspection` | crosshair SVG, placement, no CSS additions |
| Inspection I2 | `display.js` | `inspection` | record shape unchanged; no new verb or field |
| Inspection I3 | `obs-dock.js` mode variable | `inspection` | no localStorage write, no channel post for the mode |
| Manual M1 | motion feel | `manual` | one continuous glide/crossing, no bounce |
| Manual M2 | dark-mode face | `manual` | the control follows the navpair's focus fill |
| Manual M3 | live 15 s | `manual` | the real clock reads and behaves like the preview |

**Verification split**: `60 test · 5 inspection · 4 manual` (69 traceability rows). Every `test`
row is written red-first before its implementation task; the rows share 14 E2E methods, grouped in
`tasks.md` by method rather than repeated verbatim.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| `startMorph` gains a `carry` argument instead of leaving one morph for both modes | the same 230 ms height animation must scroll in following and stand still in browsing, with `finishMorph` owning `inert`/classes once | a second morph duplicates ownership of the same `.entryinner` nodes; skipping the morph makes block heights pop |
| The advance discriminator lives in `sync()`, not at the ~17 projection call sites | it covers advances made in another window and excludes FR-014 notices by construction | call-site flags miss external writers and drift as call sites are added; centre-on-every-notice reintroduces the removed behaviour |
| One ~100 ms interval rather than a `setTimeout` per event | FR-008 reads all six conditions at fire time, and a held press must suspend the count | `setTimeout` reads stale conditions when armed; a held press would need a second mechanism anyway |

## Project Structure

### Documentation

```
specs/200-dock-centre-triggers/
  spec.md  plan.md  research.md  data-model.md  quickstart.md
  contracts/README.md  checklists/requirements.md  preview/
  tasks.md  analysis.md  converge.md  fold.md   (added by their own stages)
```

### Source

```
multimedia/web/templates/reading/obs_dock.html   + #centreBtn in .navpair
static/web/obs-dock.js                            following mode, notice discriminator, clock, morph guard
tests/e2e/test_obs_dock_follow.py                 new red-first E2E suite
docs/spec/dock.md                                 Fold: dock/R15 added (after Converge)
```

### Structure Decision

The dock is server-rendered markup plus one vanilla script; the new control belongs in the existing
template beside its two siblings, and every behaviour change belongs in the one script that already
owns centring, morphing and the display subscription. No CSS file is added — `.navbtn` already
encodes the approved geometry. Tests follow the repo's E2E lane; the capability delta lands at Fold.
