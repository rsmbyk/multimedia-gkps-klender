# Tasks — the dock's entry headers expand and collapse their own block

**Spec**: `specs/198-dock-entry-toggle/spec.md`
**Plan**: `specs/198-dock-entry-toggle/plan.md`
**Verification split**: 33 test · 3 inspection · 1 manual (the plan's traceability table is the
row-level source; this file carries one task per row it can act on)

Ordered by user story. `[P]` means order-independent, not concurrent; the run states the order it
used. **Red-first**: every test task is run against `develop` (`13baf77f`) — with the branch's
changes stashed — and must fail for the toggle reason, not an import (SC-006), before its
implementation task runs. Two declared exceptions to *in-phase* red-green: US2's behaviour shares
the handler branch US1 lands (one branch serves both stories, so US2's red is the stashed-against-
develop run), and US1's live-row test carries a chevron assertion that only becomes real once US3's
chevron build lands (research, "Noted"). The final full-suite run pins both.

## Phase 1 — Setup

- [x] T001 `tests/e2e/test_obs_dock.py` — extend the suite's fixtures with the eligibility matrix:
  one dated service carrying a passage with verses, a song with verses, a verse-less song
  (`start > end` → empty inner), and a `SECTION_BREAK` entry, so every row of FR-001/FR-010 has a
  real counterpart to count against.

## Phase 2 — Foundational

- [x] T002 `static/web/obs-dock.js` — the shared state: `entryOverrides` Map (page memory only),
  `effectiveOpen(index)` = `live ? open : (override ?? false)`, and `buildInner` gains
  `inner.id = 'entryinner-' + index` so `aria-controls` has a referent (research D003/D006).
- [x] T003 the projection rewire (research D009) — the seven suites' projection clicks become two
  clicks (header to expand, then the first `.screenerow` inside `.entryli[data-index="N"]`):
  helpers `test_display_session.py::_project` (L90), `test_display_session_refresh.py::_project`
  (L71), `test_obs_overlay.py::_project` (L121), `test_obs_overlay_wrap.py::_project` (L143),
  `test_obs_dock.py::_project_first_entry` (L102), plus 12 inline sites
  (`test_display_session.py:264,351`, `test_dock_goto.py:265,292,346`,
  `test_dock_keys.py:258,377,407,456`, `test_obs_overlay.py:265,283,319`). Semantics-neutral on
  both trees — verify green on `develop` (stashed branch) for one helper-based suite and one
  inline suite at this task, so the suite never sits red between phases.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the header is a door — it toggles its own block, never projects, and the live entry is
locked open with no chevron; overrides live in page memory.
**Independent test**: the four red methods below against the fixture matrix alone.

- [x] T004 [P] [US1] `tests/e2e/test_obs_dock.py::test_the_header_toggles_its_block_and_never_projects`
  (red) — click a non-live header: block morphs (`is-morph` appears, `is-open` lands after the
  settle), `aria-expanded` true, inner `aria-hidden` false + `inert` cleared; `gkps-display`
  byte-identical, `aria-current` unchanged, `runBody.scrollTop` unchanged, no screen row selected;
  click again: closes with the same flips; break and empty headers are no-ops
  (FR-002/FR-005/FR-007/FR-010, SC-002, US1/AC1-2).
- [x] T005 [P] [US1] `tests/e2e/test_obs_dock.py::test_the_live_header_is_locked_open_and_chevronless`
  (red) — the live header's click changes nothing (no class, no attribute, no write) and its
  block stays open with `aria-current` on its row; no `.entrychev` in its `li`
  (US1/AC3, US3/AC3, SC-004).
- [x] T006 [P] [US1] `tests/e2e/test_obs_dock.py::test_open_blocks_survive_crossings_and_forget_on_reload`
  (red) — open two non-live blocks, cross the live entry to a third: both stay open through the
  hand-off, the new live row stays open and chevronless, the departed entry's stored state
  re-applies; reload: every override gone, only the live block open
  (FR-006, SC-005, US1/AC4-5, US3/AC6, edges "override inert while live" + reload).
- [x] T007 [P] [US1] `tests/e2e/test_obs_dock.py::test_the_header_keeps_the_panel_keyboard_and_the_title_name`
  (red) — every header carries `tabindex="-1"`, `aria-expanded` matching its block,
  `aria-controls` → `#entryinner-<n>`; the accessible name is the entry's title (no verb label);
  activation leaves focus on the panel (FR-008, A5).
- [x] T008 [US1] `static/web/obs-dock.js` — `toggleBlock(index)`: record the override, measure the
  body, hand-morph the one block 0fr ↔ measured height over 230 ms `easeInOut(t)` with `.is-morph`
  suppressing the CSS transition; no `centerRow`/`glideScroll`, no cursor move; **the reduce
  branch lands with US3 (T018)** (research D004, FR-005 normal half, FR-007).
- [x] T009 [US1] `static/web/obs-dock.js` — the `entryList` click handler's `.entryrow` branch
  (L1182-1187) becomes the toggle: `toggleBlock` + `focusPanel()`, **no `projectScreen` call**;
  the screen-row, band, chip and transport branches are untouched (FR-002/FR-004, US1/AC1).
- [x] T010 [US1] `static/web/obs-dock.js` — the effective-state painters: `sync()`'s inner loop
  (L1118-1133) paints `is-open`/`aria-hidden`/`inert`/`aria-expanded` from `effectiveOpen` instead
  of `current`, plus the null-guarded `chev.hidden` on the live row; `finishMorph` (L606-624)
  paints both blocks from `effectiveOpen` with the `keepOutOpen`/arrival guards instead of the
  hardcoded out-closed/in-open; the toggle branch records-and-returns when `morphState` names the
  inner (research D003/D005/D010, FR-006/FR-009).

## Phase 4 — US2 (P1)

**Goal**: the items inside are the jump targets — screen rows, band, chips and transport project
exactly as today; headers never do.
**Independent test**: the two red methods plus the whole rewired projection suite.
(Red note: US2's behaviour is the other half of T009's handler branch, so these methods' red run
is against `13baf77f` with the branch stashed — see the preamble.)

- [x] T011 [P] [US2] `tests/e2e/test_obs_dock.py::test_a_screen_row_inside_projects_that_screen`
  (red) — a collapsed non-live entry's block is `aria-hidden` + inert; expand it (asserting the
  display state is still untouched); click a middle `.screenerow`: exactly that screen goes on
  air, `aria-current` moves to it, the block stays open; the Next band projects its screen
  unchanged (FR-004, FR-008 closed half, SC-003 partial, US2/AC1-3, edge "screen-row click keeps
  the block open").
- [x] T012 [P] [US2] `tests/e2e/test_obs_dock.py` — rename
  `test_browsing_does_not_project_and_an_entry_click_does` →
  `test_browsing_does_not_project_and_a_screen_row_click_does` and flip its middle act (red):
  browsing writes nothing, a header click writes nothing (no `gkps-display`, no `OBS-*`), then a
  screen-row click projects the entry (US2/AC4, FR-004, SC-003).
- [x] T013 [US2] run the seven rewired suites green —
  `test_display_session`, `test_display_session_refresh`, `test_dock_goto`, `test_dock_keys`,
  `test_obs_overlay`, `test_obs_overlay_wrap`, `test_obs_dock` — the SC-003 bit-for-bit proof:
  the projection path itself is untouched, only its triggers moved (commands in `quickstart.md`).
  (2026-11-18: 79 tests, OK, 550 s. Fixes along the way: verse-pk fixtures in `test_dock_keys`,
  `test_obs_overlay`, `test_obs_overlay_wrap` — `verses` stores pks, not numbers; T011's Next band
  now gets its own short-viewport moment since `updateBand` hides the band whenever the live
  entry's end is in view; the crossing test waits on the DEPARTING inner's `.is-morph` (the
  arriving one only carries it when the block was closed before the crossing); both overlay
  suites settle the plate's enter motion and the web font before pixel measurements.)

## Phase 5 — US3 (P2)

**Goal**: the chevron shows the state; quiet answers for motion, breaks and reloads.
**Independent test**: the two red methods below plus the inspections.

- [x] T014 [P] [US3] `tests/e2e/test_obs_dock.py::test_the_chevron_marks_the_state_and_the_eligible_rows`
  (red) — presence matrix: a chevron in every non-break, non-empty, non-live header; none on the
  live row, a section break or the verse-less song; collapsed = no rotation, open = rotated 90°
  (`transform` matrix) after the settle; the chevron's bbox is vertically centred in the header
  (≤ 1 px off row centre — the owner's 2026-11-18 ask, research D008); hover the header: the row
  face tint covers the whole line incl. the chevron, the live row keeps the selected tint; break
  and empty header clicks change nothing (FR-001/FR-003/FR-010/FR-011, SC-001, US3/AC1-4, edges).
  (2026-11-18: red against the working tree, no stash needed — fails on `entry 0 chevron:
  {'count': 0, 'rendered': 0}`, i.e. T016/T017 absent while US1/US2 stand green underneath.
  `_block['chev']` now counts RENDERED chevrons (client rects), because sync hides — not
  removes — the live row's node; the break/empty and rotation/tint waits re-checked green.)
  (2026-11-18: **GREEN after T016/T017** — presence matrix, inert break/empty rows, the 90°
  matrix, ≤ 1 px centring on both states, tint coverage and live-none all pass. FR-011's live
  clause resolved against the pre-existing `obs-dock.css:641` (`.entryrow[aria-current="true"]:
  hover`, the 84/16 selected/ink mix): plan.md:79 maps FR-011 to `.entryrow:hover` (unchanged)
  and the owner-approved preview reuses this very sheet, so the test pins FR-011's literal half
  at rest (exactly `--sidebar-selected-bg`) and its intent under the pointer (a selected-family
  tone, never the generic `--icon-hover-bg`) — baseline CSS untouched.)
- [x] T015 [P] [US3] `tests/e2e/test_obs_dock.py::test_the_toggle_swaps_instantly_under_reduced_motion`
  (red) — a context with `reduced_motion='reduce'`: clicking a header opens the block with no
  `is-morph` ever appearing and `is-open` set within one frame, the chevron flips without a
  transition (US3/AC5, FR-005 reduce half).
  (2026-11-18: red — `a morph ran under prefers-reduced-motion: reduce (FR-005)` (1 != 0, the
  T018 gap). Everything ahead of that line already green: reduce emulation seen by matchMedia,
  no projection, swap within a frame on the page-side clock; the svg half is red by construction,
  unreachable until the morph assertion flips.)
  (2026-11-18: **GREEN after T018** — 0 morph windows counted by the in-page observer, swap
  within a frame on the page-side clock, no inline height left, chevron at the full 90° matrix
  with `transition: 0s` and no running animation.)
- [x] T016 [US3] `static/web/obs-dock.js` — the chevron build: `renderList` appends
  `<span class="entrychev" aria-hidden="true">` + the D007 SVG to the row **only when
  `buildInner` returned an inner** (breaks and empties never get one); the break early-return in
  `entryRowContent` stays chevron-free; `sync()`'s presence branch from T010 now has its node
  (research D002, FR-001/FR-010).
  (2026-11-18: svg/polyline via `createElementNS` — `el()` writes `className`, read-only on SVG
  elements; D007's polyline `7 4 13 10 7 16` over the preview's superseded `path`; appended
  inside the same `if (row)` as `aria-controls`; `node --check` green, T014's presence matrix
  proves the build, T005/T006's rendered-count `chev == 0` still green on the live row.)
- [x] T017 [US3] `static/styles/design/obs-dock.css` — `.entrychev`: `flex: none`,
  `margin-left: auto` (trailing), **`align-self: center`** (the row is baseline-aligned; probe
  offset 0 — D008), `color: var(--ink)` via the row, 15 × 15 svg, stroke rules (D007),
  `svg { transition: transform var(--ease) }`,
  `[aria-expanded="true"] .entrychev svg { transform: rotate(90deg) }`, both instant under
  `prefers-reduced-motion: reduce`, `.entrychev[hidden] { display: none }` (FR-003/FR-011 style
  side, UI/UX row).
  (2026-11-18: block placed after the stuck-row rule with its rationale comment; the reduce
  media block kills the svg transition; T014's `0.2s`/`cubic-bezier(0.32, 0.72, 0.28, 1)` +
  ≤ 1 px centring on both states, and T015's `0s`, prove it.)
- [x] T018 [US3] `static/web/obs-dock.js` — the reduce branch in `toggleBlock`:
  `if (reduceMotion.matches) { paint effective state; return; }` before any rAF — the idiom
  already at `:588` (FR-005 reduce half, US3/AC5; completes T008).
  (2026-11-18: `finishToggleMorph(inner, next)` IS the paint — it already runs `paintEntry`
  (which runs `paintInner`), cancels any stray frame and clears the inline height, so the
  reduce path shares the morph's own finish path (D003's single painter); branch sits after the
  `morphState` guard, before `startToggleMorph`; T015 green.)

## Phase 6 — Polish

- [x] T019 inspections (one pass, three rows — plan I1-I3):
  **I1 · FR-003** — read the built chevron against the spec's numbers: viewBox `0 0 20 20`,
  polyline `7 4 13 10 7 16`, stroke 1.7 round, 15 × 15, `currentColor` ink, rotation 0°→90° with
  `transform var(--ease)` (200 ms), `align-self: center` with the container probe reading offset
  0 on collapsed and expanded rows, and the glyph sweep: no `+`/`−`/`×` enters `obs-dock.js` or
  `obs-dock.css` (SC-004's prohibition half).
  (2026-11-18: all present at `obs-dock.js:320-325` (viewBox, polyline) and `obs-dock.css:408-432`
  (15 px, stroke 1.7 round, `currentColor`, `transition: transform var(--ease)` = 200 ms,
  `rotate(90deg)` on `[aria-expanded="true"]`, reduce → `transition: none`, `align-self: center`);
  runtime halves pinned by T014 (≤ 1 px centring both states, 0.2s / the curve, 90° matrix) and
  T015 (`0s`). Glyph sweep: no affordance glyph anywhere — the only `×` in `obs-dock.css` are two
  comment dimensions (`400×800`, `1.3×`); no `content`/`textContent` `+`/`−`/`×` string.)
  **I2 · FR-005** — read `toggleBlock` against the numbers: 230 ms, `easeInOut(t)` reuse from
  `:561`, `.is-morph` suppression, reduce branch before rAF, no scroll/glide call anywhere in the
  path.
  (2026-11-18: `startToggleMorph` (`obs-dock.js:722-748`) — `duration = 230`, `easeInOut` defined
  once at `:636` and shared with the crossing's frame, `is-morph` added for the flight (the
  comment at `:710-714`: per-inner tracking in `toggleMorphs`, "No scroll, no glide"); the reduce
  branch sits in `toggleBlock:768`, returning through `finishToggleMorph` before
  `startToggleMorph` can request a frame; no `scrollTop`/`centerRow`/`glide` appears in
  toggleBlock → startToggleMorph → finishToggleMorph — the one `scrollTop` in the crossing
  belongs to `startMorph:683`, not this path.)
  **I3 · FR-009** — read the mid-crossing queue: the `morphState`-names-this-inner
  record-and-return branch, `finishMorph`'s effective-state paint with `keepOutOpen`/arrival
  guards, `sync()`'s skip guard (`:1125`) leaving the settle as single writer.
  (2026-11-18: `toggleBlock:766-767` records the override first, then returns when
  `morphState.out/inn === inner` (record-and-return, D005); `finishMorph:690-708` clears
  `morphState`, strips both `is-morph`, clears inline heights, paints both blocks from
  `effectiveOpenFor` — `keepOutOpen` (`:652/:661/:677`: a hand-opened departing block is never
  collapsed by the crossing) and the `inWasOpen` arrival guard (`:653/:662`) — with the
  single-writer comment at `:701-704`; `sync()`'s skip guard is now `:1286-1287` (old `:1125`):
  `is-morph` or a member of the morphing pair → the settle paints them alone, D010.)
- [x] T020 Fold + delivery — `docs/spec/dock.md` gains **R14** (the entry list's headers toggle
  their own block; items jump; chevron per state; live locked) with the revision's scenarios and
  the `last folded: 2026-11-18` stamp, the `slices` line adding `198-dock-entry-toggle`; no
  `reading.md` change (no existing rule binds header projection — verified at research);
  `CHANGELOG.md` `[Unreleased]` gains the Added line; `VERSION` 1.32.2 → 1.33.0 (declared minor,
  plan.md); `converge.md`/`fold.md` written; the ITEM-208 card recreated from
  `/tmp/opencode/spec-198-v1/ITEM-208-dock-entry-toggle.md` with its facts updated and a board row
  added, the card staying in Speccing for the owner to promote (BRD-04); fast lane +
  `manage.py check` + `makemigrations --check --dry-run` run green before the fold; **nothing
  committed before Fold and nothing pushed without the owner's word** (GIT-06/GIT-07). The
  traceability table's 1 `manual` row (quickstart #4, mid-crossing feel) and the OBS passes
  (quickstart #6/#8) are the owner's — carried in the closing report, not gaps.
   (2026-11-18: R14 + 4 scenarios appended to `docs/spec/dock.md`, `last folded` → 2026-11-18, slices
   line prepended; `CHANGELOG.md` `[Unreleased]` Added line; `VERSION` 1.33.0; `converge.md`/`fold.md`
   written; analysis SHAs recomputed with `git hash-object` (checklists and tasks changed at Gate 2 and
   Implement, the two static files at US3) and a Converge/Fold history entry added. ITEM-208's source in
   `/tmp/opencode/spec-198-v1/` was wiped with the session checkpoint — the card was recreated from the
   spec, tasks and `_template.md` (status `speccing` per the ITEM-193 precedent) and its row added under
   Speccing; no anchor issue needed until it passes Speccing (BRD-10).
   Seven E2E suites: **81 OK, no skips** after restoring the checkpoint-wiped Playwright browser and host
   libraries (an earlier `OK (skipped=81)` run was discarded, never counted). Fast lane: **not green** —
   642 tests, 11 failures + 9 errors, and a stashed clean-baseline run produced the identical set (dock's
   own server suite green in both); no red attributable to this slice, recorded as a Converge exception.
   `manage.py check`: no issues; `makemigrations --check --dry-run`: no changes. **No commit, no push.**)
