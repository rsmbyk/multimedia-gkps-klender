# Analysis: the dock's entry headers expand and collapse their own block

**Spec**: `specs/198-dock-entry-toggle/spec.md`
**Plan**: `specs/198-dock-entry-toggle/plan.md`
**Tasks**: `specs/198-dock-entry-toggle/tasks.md`

**Run**: 2026-11-18, gate 2 pre-check.
**Artifacts read** (SHAs — the slice is uncommitted; the branch sits on `develop` @ `13baf77f`
after the Plan-stage fast-forward, see A2; recomputed at Fold against the final working tree):
`spec.md` 3c1f7b9b · `plan.md` 4265b39a · `research.md` bc879ed6 · `data-model.md` ca80a896 ·
`quickstart.md` c64ab62c · `tasks.md` fe289f3d · `checklists/requirements.md` 482d9f76 ·
`contracts/README.md` 4fddd0a0 · `preview/index.html` 849c7adf · `static/web/obs-dock.js` 2f0c3dec ·
`static/styles/design/obs-dock.css` 79c1b3e6.
**Metrics**: 3 stories · 11 FRs · 6 SCs · 15 acceptance scenarios + 5 edge cases · 12 assumptions
(A1–A12) · 20 checklist items (CHK001–CHK020) · 20 tasks (T001–T020) · 37 traceability rows ·
verification split **33 test · 3 inspection · 1 manual** · 0 open markers · 0 questions escalated.

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | ambiguity | `spec.md` FR-005 | The literal "0fr ↔ 1fr" is looser than the mechanism: the hand morph animates *measured pixels* on `grid-template-rows`, exactly as the crossing does (D004). Behavioural content is fully bound; only the literal CSS keyframe reading drifts. | Carried — Gate 1 accepted the wording; tighten at Converge if the owner wants the prose to match the mechanism. Cost of leaving: a reader may expect literal `0fr↔1fr` keys; no test reads CSS keyframes, so evidence is unaffected. |
| A2 | LOW | stale ref | `plan.md`, `research.md`, `tasks.md`, checklist, spec | `develop` moved from the branch's cut `341cf340` to `13baf77f` (spec 197) during Plan, so every `develop (341cf340)` claim, the 8 CSS line refs (+13 picker lines above `.entryrow`) and the bump base (`1.32.1`, now `1.32.2`) were stale. | Fixed in place (mechanical): branch fast-forwarded `341cf340 → 13baf77f` on the owner's word, 21 references re-read/updated (delta below), plan gained a branch-base note. `obs-dock.js` and the seven rewire files are byte-identical between the refs, so no JS/test ref needed a change. Cost of leaving: red runs would test "develop minus 197" while claiming `develop`, and Fold would meet a VERSION/CHANGELOG conflict for no reason. |
| A3 | LOW | protocol | `tasks.md` T005 | US1's live-header test asserts the live row has no chevron — vacuous until US3's chevron build (T016) lands later in the run; the intermediate green proves nothing for that line. | Accepted with the declared exception (tasks preamble, research "Noted"): the final full-suite run after T018 pins it for real. Cost of leaving: an intermediate green over-read as evidence for the live-chevron rule. |
| A4 | LOW | protocol | `tasks.md` T003 | The 17-site projection rewire runs Foundational — *before* the handler change — on the claim that the two-click pair lands the same end state on both trees (D009). | Declared exception, verified: T003 requires one helper-based suite and one inline suite green on stashed `13baf77f` before proceeding. Cost of leaving if the claim were wrong: caught at T003 in minutes, never carried to delivery. |
| A5 | LOW | naming | `tasks.md` T012 | The rename `test_browsing_does_not_project_and_an_entry_click_does → ..._a_screen_row_click_does` flips a test's meaning, not just its name. | Recorded in tasks; grep confirms the old name appears only in the rename instruction and the test file itself — no orphan references anywhere. Cost of leaving: none, rename is a task with its red act. |
| A6 | LOW | ordering | `tasks.md` T008/T018 | The `reduceMotion` branch in `toggleBlock` is deferred from US1's T008 to US3's T018, so FR-005's reduce half lands a phase after its normal half. | Declared in T008 and in the traceability (reduce verified by `::test_the_toggle_swaps_instantly_under_reduced_motion`, T015/T018). Cost of leaving: a within-run gap only — between T008 and T018 a reduced-motion context would still run the rAF morph; the final suite closes it before any delivery. |
| A7 | LOW | latent | `static/web/obs-dock.js:615-620` | `finishMorph` hardcodes out-closed / in-open at settle. Correct *today* (no override state exists), it becomes an SC-005 violation the moment overrides land: a crossing would reopen a closed block. | Fixed by plan: D010's `keepOutOpen`/arrival guards are a named part of T010, and inspection I3 reads them. Cost of leaving: silent reopening of operator-closed blocks at every crossing — the exact bug SC-005 forbids. |
| A8 | LOW | baseline | board known-red cards | Seven known-red E2E cards on develop (ITEM-139/140/141/144/153/156/184) name their files explicitly; none of them is one of the seven rewire suites. | Verified from the cards' file lists — no action; T013's "seven suites green" is a clean claim. Cost of leaving: a final run misattributing a pre-existing red to this slice (none of the known reds live there anyway). |

**Coverage**: 100% (37/37 rows) · **CRITICAL**: 0 · **HIGH**: 0 · **MEDIUM**: 0 · **LOW**: 8 —
one fixed in place (A2), seven accepted with the guards named in the table.

**Gate 2 opens** (SDD-17: zero CRITICAL, 100% coverage). `tasks.md` was generated before this
analysis and re-checked against it; `converge.md` is absent by design (Converge writes it).

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | T001, T010, T014, T016 | eligibility at build, presence in `sync()` |
| FR-002 | ✅ | T004, T008, T009 | handler branch never projects |
| FR-003 | ✅ | T014, T017, T019 (I1) | numbers + centring + glyph sweep |
| FR-004 | ✅ | T003, T011, T012, T013 | trigger set enumerated; rewire proof |
| FR-005 | ✅ | T008, T015, T018, T019 (I2) | hand morph; reduce split A6 |
| FR-006 | ✅ | T002, T006, T010 | effective state + painters |
| FR-007 | ✅ | T004, T008 | no scroll, no selection |
| FR-008 | ✅ | T007, T011 | attributes, name, panel focus |
| FR-009 | ✅ | T010, T019 (I3) | queue branch + settle guards; feel → manual |
| FR-010 | ✅ | T001, T014, T016 | break + verse-less fixtures |
| FR-011 | ✅ | T014, T017 | chevron inside the row, tint covers it |
| SC-001 | ✅ | T014 | DOM count vs entry list |
| SC-002 | ✅ | T004 | morph + attribute flips + untouched state |
| SC-003 | ✅ | T003, T013 | seven rewired suites green, path untouched |
| SC-004 | ✅ | T005, T014 | live / break / empty no-ops |
| SC-005 | ✅ | T006, T010 | crossing never reopens a closed block |
| SC-006 | ✅ | red runs at Implement + T013/T020 | red-first, final full-suite run |
| US1/AC1 | ✅ | T004 | |
| US1/AC2 | ✅ | T004 | |
| US1/AC3 | ✅ | T005 | chevron half pins at T016 (A3) |
| US1/AC4 | ✅ | T006 | |
| US1/AC5 | ✅ | T006 | multi-open |
| US2/AC1 | ✅ | T011 | |
| US2/AC2 | ✅ | T011 | closed block inert |
| US2/AC3 | ✅ | T011 | Next band unchanged |
| US2/AC4 | ✅ | T012 | flipped act |
| US3/AC1 | ✅ | T014 | |
| US3/AC2 | ✅ | T014, T015 | reduce instant |
| US3/AC3 | ✅ | T005 | |
| US3/AC4 | ✅ | T014 | |
| US3/AC5 | ✅ | T015, T018 | |
| US3/AC6 | ✅ | T006 | reload forgets |
| Edge: override inert while live | ✅ | T006 | |
| Edge: mid-crossing toggle | ✅ | T019 (I3) | structural; feel → manual quickstart #4 |
| Edge: break / empty click | ✅ | T014 | |
| Edge: non-live header chevron | ✅ | T014 | |
| Edge: screen-row click keeps block open | ✅ | T011 | |

## Applied mechanically

- Branch fast-forwarded `341cf340 → 13baf77f` (owner's choice at Plan, 2026-11-18; FF creates no
  commit, so GIT-06's Fold floor is untouched). Spec pack untracked throughout — intact after.
- 21 stale references updated: research 11 (9 CSS line refs +13, bump base, header SHA) · plan 5
  (CSS line refs block, bump base, 3 × base SHA) · tasks 3 (2 × base SHA, bump base) ·
  checklist 1 (bump base) · spec 1 (the UI/UX "today (HEAD …)" row). The spec's two remaining
  `341cf340` mentions are the historical revert point — fact, not staleness.
- Bump base corrected `1.32.1 → 1.32.2` everywhere; target unchanged: `1.33.0` (D011).
- `plan.md` gained a **Branch base** paragraph; counts re-verified after edits (37 rows parsing
  as 33 · 3 · 1; 20 CHK; 20 tasks); no duplicate IDs, no orphaned references, no terminology drift
  found; zero `[NEEDS CLARIFICATION]` markers.

## Escalated

none — no intent-changing finding, no requirement conflict, no question to ask the owner here.

## History

- 2026-11-18 — initial run at Plan (SHAs above): 0 CRITICAL · 100% coverage · 8 LOW · gate 2 opens.
- 2026-11-18 — **Gate 2 accepted** (owner: "tick and accept all"): all 20 checklist items ticked,
  findings A1 and A3–A8 accepted, A2 already fixed in place. Implement opens.
- 2026-11-18 — **Converge + Fold**: all 20 tasks done; seven E2E suites green in a real, unskipped run
  (81 tests, 246.9 s) after the checkpoint-wiped container's Playwright browser and host libraries were
  restored; fast lane red with 20 failures/errors, byte-identical on a stashed clean baseline (dock's own
  server suite green); `check` + `makemigrations --check` green. Dock R14 folded, minor bump 1.33.0 applied,
  ITEM-208 recreated in Speccing; nothing committed or pushed (GIT-06/GIT-07). FR-011's live-hover clause
  executed as "keeps the selected family, never the generic hover face" — plan.md:79 maps FR-011 to
  `.entryrow:hover` (unchanged) and the approved preview reuses the same sheet; baseline CSS untouched.
