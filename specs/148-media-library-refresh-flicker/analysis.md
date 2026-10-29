# Analysis: the Media Library list holds still while it refreshes

**Date**: 2026-10-28 · **Gate**: opens at zero CRITICAL and 100% coverage.
**Artifacts read** (sha256, first 12):

| Artifact | Digest |
| --- | --- |
| `spec.md` | `8c4ed0e26135` |
| `plan.md` | `6cc5306e84e7` |
| `research.md` | `f5bae6181409` |
| `data-model.md` | `c862124a3d46` |
| `contracts/none.md` | `0cc110e7f11d` |
| `quickstart.md` | `060a4eb4cd4e` |
| `tasks.md` | `7f2ddcb0bac0` |
| `checklists/requirements.md` | `8af6f6a17971` |

**Metrics**: 5 requirements · 5 success criteria · 8 story scenarios · 6 edge cases (23 traceability
rows) · 18 tasks (7 of them writing or driving tests) · coverage **100%** · CRITICAL **0**.
`check_pack_consistency.py specs/148-media-library-refresh-flicker` → `COVERAGE 10/10`,
`SPLIT 20/3/0`, `ASSIGNMENT 12/12`, `clean`.

## Findings

| # | Class | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | note | FR-002, SC-001 and US1 AC2/AC3 all land on one command: the per-row `top` spread answers the requirement, the criterion and two scenarios at once. | Kept: they are different claims (a rule, a measured criterion, two triggers); one sampler observes all of them. Recorded so a reader does not hunt for a second test. |
| F2 | note | The six cases are written in **Foundational**, not one per story: both stories are served by a single control-flow change, and TDD-01 forbids writing a test after the code it covers — a US2 test placed in its own phase would be green on arrival. | Recorded: the ordering is a TDD decision, not a drifted task list. Each story is still demonstrated by its own cases. |
| F3 | low | US1 AC1 (`Share online`) needs a same-origin `…/cloud/<sha>/begin/` stub to reach `refresh()` without an upload; the case proves the refresh's invariant, not the upload. | Accepted: the upload path is out of this slice (spec's scope), and the stub only replaces a server call the page makes before the refresh it is testing. Named in T004. |
| F4 | low | The preview's live readout runs against the compose `web` service, which serves `develop` until this slice merges — so the sampler shows the defect now and cannot show the fix on that port. | Accepted with a task: T012 gives the sampler a `--url` argument and re-reads a worktree `runserver` (the companion echoes the request `Origin`, `local_media.py:456`), so the fix has a live readout of its own. |
| F5 | none | `docs/spec/reading.md` has no requirement for this list's redraw; its R12 speaks about filenames truncating and its R13 about text wrapping. | Not a defect: Fold adds R24 (T017); the spec's FRs cite `new: reading` → R24. |
| F6 | low | The plan's design is a sketch of `refresh()`'s control flow, written before the tests exist; a sketch in a plan is not evidence that the sequence closes every path. | Accepted: T009's red run and T010's green run are what prove it, and Converge re-reads the code against FR-001's three paths. |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T005, T010, T013 |
| FR-002 | ✅ | ✅ | T003, T004, T010 |
| FR-003 | ✅ | ✅ | T005, T006, T007, T010 |
| FR-004 | ✅ | ✅ | T008 |
| FR-005 | ✅ | ✅ | T014 (inspection + the unchanged re-run) |
| SC-001 | ✅ | ✅ | T003, T004 |
| SC-002 | ✅ | ✅ | T006 |
| SC-003 | ✅ | ✅ | T005 |
| SC-004 | ✅ | ✅ | T005 |
| SC-005 | ✅ | ✅ | T014 |
| US1 AC1…AC5 | ✅ | ✅ | T003, T004, T005, T008 |
| US2 AC1…AC3 | ✅ | ✅ | T005, T006, T007 |
| 6 edge cases | ✅ | ✅ | T002's fixture, T003, T006, T014 |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 4 (F3, F4, F6 low, plus F1/F2 notes).

## Applied mechanically

- **Split corrected**: the plan declared `17 test · 7 inspection`; the table's 23 rows count
  `20 test · 3 inspection · 0 manual` (two rows name two kinds and are charged to their first). The
  declared line now matches the counted one.
- **Two symbols unassigned**: `test_disconnected_library_hides_local_inventory_details` and
  `test_empty_library_keeps_tall_create_modal_and_quiet_empty_state` were named in the plan's edge row
  but in no task. Both are now in T014's unchanged re-run.

Both were applied before the run was repeated; the re-run is the clean one whose digests are above.

## Escalated

- Nothing. Every finding is a note or a recorded acceptance; no question changed what the spec means.

## History

- **2026-10-28 — first run**, on the accepted spec and the plan: `COVERAGE 10/10`,
  `SPLIT` mismatched (declared 17/7/0, counted 20/3/0), `ASSIGNMENT 12/12` after two fixes, six
  findings — two notes (one command serving several statements; the TDD ordering of the six cases),
  three low (the Share-online stub, the preview reading `develop`, the plan's sketch of the control
  flow), one none (the capability delta awaiting Fold). Two mechanical fixes applied, the digest line
  above is the post-fix run, and it reports `clean`.
- **2026-10-28 — implement, T009's red run**: the six cases were written and run against the
  unmodified `static/web/media-library.js` before T010. Three failed, each on its own measurement —
  `rows moved while a cancelled remove: [0.0, 26.0]`, `[0.0, 26.0]` again for Share online, and
  `2 not less than or equal to 1` list changes for one refresh. Two more are **guards** that were green
  on the shipped page by design: a failed references read and the 2s poll both end in one picture
  either way, so there is no visible failure to start from, and they were reworded to guard form
  (at most one change, no row moved). The failed-read case first asserted exactly one change and went
  red the wrong way (`0 != 1` — the unfixed page draws its two identical placeholder passes, which a
  change counter cannot see); that reading was rejected as a wrong-reason red and the case became a
  guard.
- **2026-10-28 — implement, T011/T013's green run**: `6 tests … OK` in 28.4s after the one control-flow
  change. The module in full: `Ran 28 tests in 82.3s`, one failure —
  `test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen`, proven identical on unmodified
  `develop` under the same command and database (`19.8453369140625 != 12` there, `19.67…` on this
  branch) and carded as ITEM-156; nothing else in the module fails.
- **2026-10-28 — T012's live readout, not taken**: the sampler gained its URL argument, but the compose
  `web` service serves the `develop` checkout and the companion admits only its configured origins
  (`local_media.py:447`), so a worktree server shows `Local library unavailable on this computer.` The
  readout is recorded as a convergence task (T019) and runs after the merge.
