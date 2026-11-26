# Reading Checklist: visible pending state for rail and sidebar fetches

**Spec**: `specs/243-navigation-loading-feedback/spec.md` · **Created**: 2026-11-25 · **Depth**: Standard

- [X] CHK001 Is the reported trigger — a slow rail/sidebar fetch with no sign of work — named in a testable scenario? [Completeness, Spec §Input, §US1] — Evidence: US1/AC1 pins a delayed Kidung rail click and reads the stage before and after.
- [X] CHK002 Is "changes the reading page" defined by writes into the stage rather than by which panel fetched? [Clarity, Spec §Introduction, §Scope] — Evidence: song, verse/passage and service are writes; rail, chapter-number list and songbook are list-only.
- [X] CHK003 Is the chapter-list / verse boundary explicit? [Ambiguity, Spec §Introduction, §US2/AC2] — Evidence: confirmed that the chapter-number list is list-only and the verse opened from it writes.
- [X] CHK004 Is the lock visual measured, not merely described as "busy"? [Clarity, Spec §FR-002, §UI/UX] — Evidence: rail icon opacity `0.45`, sidebar row opacity `0.58`; no spinner/label/edge/ring.
- [X] CHK005 Is the bar position and height measurable for every affected section? [Completeness, Spec §FR-003, §UI/UX] — Evidence: 3px bar at `0px` from the section's top edge for `#panel`, `#chapters` and `.stage`.
- [X] CHK006 Is the list-only promise stated as a negative assertion? [Coverage, Spec §FR-004, §US1/AC2] — Evidence: no `aria-busy`, no bar, no placeholder; the displayed passage stays.
- [X] CHK007 Are all three stage-write layouts specified separately? [Coverage, Spec §US2/AC1–AC3, §FR-006] — Evidence: Bible (`read__ed`, `read__sec`, `v__n`), song (`HAL n`, multi-line `v__text`), service (`entry__start`, `tatib__item`, `read__sub`).
- [X] CHK008 Is the placeholder origin measured against the real `.read`, not just "aligned"? [Clarity, Spec §US2/AC4, §UI/UX] — Evidence: x=520, y=218 at 1440px for both; narrow-width padding 18px at ≤720px.
- [X] CHK009 Is the settle path testable for each busy state? [Coverage, Spec §US2/AC5, §FR-008] — Evidence: `aria-busy`, bar and placeholder all clear when the fetched page paints.
- [X] CHK010 Is the supersede rule stated for both write-class combinations? [Coverage, Spec §US3/AC1–AC3, §FR-007] — Evidence: write→write cancels; write→list coexists; list→write cancels.
- [X] CHK011 Is re-activation of a cancelled item covered? [Coverage, Spec §US3/AC4] — Evidence: cancelled item unlocks and can be clicked again immediately.
- [X] CHK012 Is the full-page fallback path covered rather than silently cleared? [Coverage, Spec §US3/AC5, §FR-008] — Evidence: pending state remains until unload when `navigate()` falls back to `window.location.href`.
- [X] CHK013 Is the rail/sidebar container explicitly left interactive? [Consistency, Spec §FR-009, §Accessibility] — Evidence: only the clicked item and, for writes, the stage are locked.
- [X] CHK014 Is the single choke point named? [Consistency, Spec §FR-010, §Plan §Source] — Evidence: pending state starts and clears in `navigate()`; no per-click pending state.
- [X] CHK015 Is the accessible announcement specified without focus movement or spam? [Clarity, Spec §Accessibility] — Evidence: pre-rendered empty polite `role="status"`, one opening and one settlement message.
- [X] CHK016 Is every functional requirement traced to a user scenario? [Coverage, Spec §Requirements, §Plan §Traceability] — Evidence: FR-001…FR-010 each appear in the plan's traceability rows with a scenario or inspection.
- [X] CHK017 Is the deliberate deviation from first-party guidance recorded rather than hidden? [Consistency, Spec §Assumptions / deltas, §Plan §Complexity Tracking] — Evidence: disabling the clicked item overrides Primer/Wix with rationale.
- [X] CHK018 Are in-scope and out-of-scope surfaces stated explicitly? [Completeness, Spec §Scope] — Evidence: reading shell in scope; editor/dialog, projector/dock, full document loads, offline copies and endpoint/schema changes out. Added mechanically at this checklist from the existing scope sentence; intent unchanged.
- [X] CHK019 Is the accepted preview version named and kept with its predecessors? [Clarity, Spec §UI/UX, §Plan §Preview] — Evidence: `preview/index.html` is v14; `index-v1.html`…`index-v13.html` and their thumbnails remain.
- [X] CHK020 Does the plan's verification split match the declared requirements? [Coverage, §Plan §Traceability] — Evidence: 11 test + 8 inspection + 0 manual across 16 rows; no requirement left without a verification row.
- [X] CHK021 Does the slice avoid hidden credentials and invented identifiers? [Clarity, Spec §Header, §Plan §Bump, §Quickstart] — Evidence: demand `ITEM-258` and capability `reading/R61` rechecked free across refs; quickstart uses `***` for the DB password.
- [X] CHK022 Do the artifacts avoid personal names? [Consistency, whole pack] — Evidence: roles only (owner, operator, agent); no person name in spec, plan, data model, contracts or quickstart.

**Result**: 22/22 pass. No requirement was rewritten by this checklist except the mechanical
addition of the explicit `## Scope` section in CHK018. **Next stage: Tasks** — not started.
