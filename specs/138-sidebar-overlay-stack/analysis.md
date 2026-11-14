# Analysis: the sidebars are a drawer stack

**Date**: 2026-10-27 · **Gate**: opens at zero CRITICAL and 100% coverage.
**Artifacts read** (sha256, first 12):

| Artifact | Digest |
| --- | --- |
| `spec.md` | `b8f1182eb4bf` |
| `plan.md` | `1e8c335d570c` |
| `research.md` | `88d1d6022cda` |
| `data-model.md` | `379d325eccbd` |
| `contracts/shell-state.md` | `c5a1a78b30ac` |
| `quickstart.md` | `657701f31ea2` |
| `tasks.md` | `c7bae50464a1` |
| `checklists/requirements.md` | `1b169425e020` |

**Metrics**: 23 requirements · 10 success criteria · 18 story scenarios · 7 edge cases (43
traceability rows) · 17 tasks (5 of them test-writing) · coverage **100%** · CRITICAL **0**.

## Findings

| # | Class | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | note | FR-001 and FR-013 resolve to one test: "the drawer never changes the stage's width" and "the stage is unchanged by opening and closing" are the same rectangle read twice. | Kept: two statements, one measurement. Recorded so nobody looks for a second test. |
| F2 | note | FR-014's test is the *absence* of a change at 1440 — it asserts today's pushed widths. If the desktop layout ever changes for another reason, this test fails and will read as this slice's fault. | Kept: it is the only way to prove "unchanged above the breakpoint". The failure message names the widths, so the next reader can tell a regression from a redesign. |
| F3 | low | The touch exemption (FR-021) is keyed on the pointer, not the width: a narrow desktop window keeps the hover behaviour. The prototype shows it at 425px because the drawer cannot hover; the E2E emulates a touch pointer for that row. | Kept and stated in the spec. Cost of leaving it: one test needs pointer emulation, which Playwright supports and the suite already uses for hover-free checks. |
| F4 | low | `US5.2`'s scroll lock is the shell's first document-level scroll lock. A lock that outlives a closed drawer freezes the page, and the only proof is a test that closes the stack and then scrolls. | Kept as a test (T012); the implementation clears the attribute in `closeAll()` and on a resize above the breakpoint, both stated in `plan.md`'s Risks. |
| F5 | low | Two requirements are only reachable through the phone's own states (FR-019, FR-020): above 720px the menu does not exist, so the rows cannot demonstrate it. | Accepted: the E2E sets a phone viewport for those rows; the inspection rows (search landing, empty second level, modal stacking) cover what a rectangle cannot. |
| F6 | note | The prototype's `proto.css`/`proto.js` stay in the repository after Implement, and they will then describe a shell that has the behaviour itself. | Kept: they are how the preview was built and what makes the numbers repeatable; `quickstart.md` says they become redundant probes, not the source of behaviour. |
| F7 | fixed | **First pass:** `test_a_navigation_keeps_the_open_stack` was named in the traceability table but assigned to no task — the navigation edge had no task behind it. | Mechanical fix applied before re-running: added to T012, and the verification split corrected from a hand-written count to the counted one (40 test · 3 inspection). |

No other mechanical fixes were needed: terminology is consistent (`level`, `stack`, `menu`,
`control`), every requirement has at least one task, and every path the plan names exists in the
worktree (`components.css`, `base.html`, `reading.js`, `tests/e2e/`).

## History

- **2026-10-27 — first run**, on the accepted spec and the plan above: 0 CRITICAL, coverage 98% —
  one requirement had no task (F7). The task list and the split were corrected, the digests
  refreshed, and the run repeated.
- **2026-10-27 — second run**, on the corrected artifacts: 0 CRITICAL, 100% coverage, seven findings
  — four notes, three low, none fixed silently except F7, which is reported above.
