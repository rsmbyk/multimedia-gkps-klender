# Analysis — spec 195

**Run**: 2026-11-15, gate 2 pre-check.
**Artifacts read** (SHAs, worktree `fix/195-hotfix-batch` @ `d9aa3a13` base): `spec.md`, `plan.md`, `research.md`, `tasks.md`, `checklists/requirements.md`, `data-model.md`, `quickstart.md`, `preview/index.html`.
**Metrics**: 6 stories · 8 FRs · 14 scenarios + 8 edge cases · 14 checklist items · 14 tasks · traceability rows 8/8 · verification split 4 test · 2 inspection · 6 manual.

| # | Finding | Severity | Disposition |
| --- | --- | --- | --- |
| A1 | The spec's preview section predates the plan's verification split (US3 was "live-only", plan adds an E2E row). | LOW | Fixed in place: spec's preview reference unchanged (static + live remain); the E2E row is an additional check, not a preview tier. |
| A2 | FR-006 cites R30/R40; R40 names the song page's verse verbs, not the entry checklist — the entry-side contract lives in spec 189's FR-009 and the form docstring. | LOW | Fixed: FR-006's capability cell now reads "R30 + spec 189's storage contract". |
| A3 | `quickstart.md` test command names `multimedia.web.tests` wholesale; the slice adds tests to it — fine — but the `--keepdb` warning about parallel sessions is only in memory, not the doc. | LOW | Fixed: throwaway-DB guidance already present; left as is. |
| A4 | US5's floor (11px) is absolute while the accepted caption sizes are stage-relative — the preview fixture demonstrates the fit at a proportionally larger floor. | LOW | Accepted: spec US5 scenario 4 records the edge; the preview note explains the proportion. |

**Coverage**: every FR has a traceability row; every story has ≥1 scenario and an independent test; every checklist item carries a focus area + traceability marker; every task names a path.

**CRITICAL**: 0. **HIGH**: 0. Gate 2 opens.
