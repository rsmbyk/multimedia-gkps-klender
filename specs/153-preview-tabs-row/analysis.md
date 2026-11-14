# Analysis: the preview's verse tabs get their own row

**Date**: 2026-10-29
**Artifacts read** (SHA-1, as written):

| Artifact | SHA |
| --- | --- |
| `spec.md` | `a62171e4ab02187cf83217d929ff1f36f447047e` |
| `plan.md` | `e7f609ff732b4d91c79f5a4991475cdd6dc95afa` |
| `tasks.md` | `895ed7fbb6496873a552e7795d3a5d3319d1ff05` |
| `research.md` | `17eac909af390f4d4f54a14efa6ff4d4db04061b` |
| `data-model.md` | `3ab30421d140d586085a7d1ff941d7eeeff74304` |
| `quickstart.md` | `c42d715af9d77b21c2613ae63556590679b864a1` |
| `contracts/none.md` | `cd43bd2b686f713eaf8fd5842422a2abceac3990` |
| `checklists/requirements.md` | `5eb997f26c39d68ac632b9ded5f796695c132812` |

**Metrics**: 3 user stories · 7 FR · 6 SC · 12 tasks · 28 traceability rows = 22 `test` · 4 `inspection`
· 2 `manual` · **0 CRITICAL, 0 HIGH**.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A001 | MEDIUM | Case count drifted between artifacts: `research.md` D005 said "four cases", the plan's Technical Context said "six", and `tasks.md` T002/T005/T007 spell out seven. | **fixed — mechanical.** Both say seven, listing them; re-read after the fix. |
| A002 | LOW | `plan.md` declares `bump: patch` → 1.22.11 while slices 151 and 152 are in flight; whichever merges first takes 1.22.11. | **accepted.** The level is what the plan may declare; C-GIT-VER stamps the number against `develop` in the pre-merge commit. Recorded on the plan's `Bump` line. |
| A003 | LOW | FR-006 (30px circles, 4px gap, horizontal scroll) has no task that *writes* a test — the behaviour is already pinned by the 12-tab case, whose locator T009 moves. C-SDD-TDD asks for a test task per `test` row. | **accepted.** The test exists and its assertions do not change; a new case would duplicate it. Recorded here so the missing task is a decision, not an oversight. |
| A004 | LOW | `SC-003` reads "`:focus-visible` paints on the body for a keyboard open and on no tab, ever", while US3 AC2 says the keyboard open does paint a ring — on the body. | **accepted.** The two sentences name different elements; read together they are the requirement. No edit needed. |

No CRITICAL, no HIGH, no intent-level conflict: nothing in the plan narrows or contradicts a requirement,
and every FR/SC appears in the traceability table against at least one task.

## History

- **2026-10-29 — first run.** 4 findings (1 MEDIUM, 3 LOW); A001 applied as a mechanical fix and the
  artifacts re-read; A002–A004 accepted with the reasons above. Coverage 100% (7/7 FR, 6/6 SC).
