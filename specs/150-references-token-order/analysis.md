# Analysis: the first refresh authenticates its references write

**Date**: 2026-10-28 · **Gate**: opens at zero CRITICAL and 100% coverage.
**Artifacts read** (sha256, first 12):

| Artifact | Digest |
| --- | --- |
| `spec.md` | `3aa222c82bb8` |
| `plan.md` | `e392506e44b9` |
| `research.md` | `8cd745946b70` |
| `data-model.md` | `2acb3529293d` |
| `contracts/none.md` | `b968cd6cea15` |
| `quickstart.md` | `c43a14c916fb` |
| `tasks.md` | `a378229935ef` |
| `checklists/requirements.md` | `b8efe757a12e` |

**Metrics**: 4 requirements · 4 success criteria · 5 story scenarios · 4 edge cases (17 traceability
rows) · 13 tasks (7 writing or driving tests) · coverage **100%** · CRITICAL **0**.
`check_pack_consistency.py specs/150-references-token-order` → `COVERAGE 8/8`, `SPLIT 13/3/1`,
`ASSIGNMENT 10/10`, `clean`.

## Findings

| # | Class | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | note | FR-002's evidence is spec 148's six cases rather than new ones: this slice changes *when* a value exists, and their assertions already state the outcome. Only the stub under them changes. | Kept: the six keep their wording, so a red points at the fix rather than at rewritten tests (FR-004). |
| F2 | low | SC-001 cannot be measured on the branch — the compose page serves `develop` and a worktree server is refused by the companion's origin allow-list. | Accepted as the pack's one `manual` row, with the exact commands in `quickstart.md`; spec 148 recorded the same limitation. |
| F3 | low | The new case asserts the header on the page's `/references` request; a page that sent the token *after* a failed first attempt would still pass it if it recovered on the same write. | Accepted: the stub's 403 makes a first attempt without the token visible in the draw as well (US1 AC2 asserts the first draw carries the references), so the two assertions together pin the first attempt. |
| F4 | none | `docs/spec/reading.md` states the one-draw rule as R24; this slice's authentication rule is folded as R25 rather than as a modification of R24, because it can fail alone. | Recorded: Fold adds R25 (T011); R24 stays as accepted. |

No mechanical fixes were needed beyond the split line and the symbol list (both corrected before this
run — the declared split now counts the same rows the table holds, and all ten symbols the plan names are
assigned in `tasks.md`).

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T003, T005 |
| FR-002 | ✅ | ✅ | T004, T006 |
| FR-003 | ✅ | ✅ | T002, T004, T007 |
| FR-004 | ✅ | ✅ | T008 |
| SC-001 | ✅ | ✅ | T013 (`manual`) |
| SC-002 | ✅ | ✅ | T003 |
| SC-003 | ✅ | ✅ | T004, T006 |
| SC-004 | ✅ | ✅ | T008, T006 |
| US1 AC1…AC3 | ✅ | ✅ | T003, T006 |
| US2 AC1…AC2 | ✅ | ✅ | T002, T004 |
| 4 edge cases | ✅ | ✅ | T006, T007, T008 |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 2 (F2, F3) · notes: 2 (F1, F4).

## Applied mechanically

- **Split corrected**: declared `15 test · 4 inspection · 1 manual` against a table that counts
  `13 / 3 / 1`. The declared line now matches the counted one.
- **Symbols reconciled**: the three spec-148 cases named in `tasks.md` (T006) were not in the plan's rows;
  the plan's FR-002 row now names all six, and no symbol is named on one side only.

## Escalated

- Nothing. No finding changed what the spec means.

## History

- **2026-10-28 — first run**, on the accepted spec and the plan: `COVERAGE 8/8`, split and assignment
  corrected before the clean run above, four findings — one note (FR-002 evidenced by 148's cases), two low
  (the live readout is post-merge; the new case's single-attempt reading), one none (R25 rather than a
  modification of R24). The digest line is the post-fix run and reports `clean`.
- **2026-10-28 — implement, T004's red run**: against the unmodified `static/web/media-library.js` with the
  stricter stub, the new case failed on the header (`'' != 'test-token'`) and three spec-148 cases failed on
  their own numbers — `rows moved while a cancelled remove: [0.0, 26.0]`, the same for Share online, and a
  placeholder frame list of ones. `test_the_library_list_is_drawn_once_per_refresh` passed in that run because
  its reset happens after the load's single failed refresh; the first-load defect is caught by the placeholder
  case and by the new case, which is why both carry it.
- **2026-10-28 — implement, T006's green run**: `7 tests … OK` in 25.0s after the one statement; the module in
  full `Ran 38 tests in 302.4s`, one failure — `test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen`
  (`20.0 != 12`), the pre-existing red carried by ITEM-156. No other case changed.
