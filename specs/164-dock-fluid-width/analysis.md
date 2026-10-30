# Analysis: the dock fills whatever panel it is given

**Date**: 2026-10-29
**Artifacts read** (SHA-1, as written):

| Artifact | SHA |
| --- | --- |
| `spec.md` | `f8a34c518ee2dffd84c230310cba28f8131ce036` |
| `plan.md` | `4f389dcaf43a1aa932b06fd8f9bb6e10127a48a1` |
| `tasks.md` | `890007eebbd1ad4db663de4bf4121ff22e43eed1` |
| `research.md` | `1a41d22d57f209b91891f1206068cda3081b21bf` |
| `data-model.md` | `6433f8171de85539f9c03ec9427fbfc959d5762c` |
| `quickstart.md` | `a756482196589a1b7b6f9516472571b27cea5441` |
| `contracts/none.md` | `103c2231ad07d9b65fae72a0ebd0be4203b1a161` |
| `checklists/requirements.md` | `ba4b8e590e4ad0aba8f7668d12c41218d982fc77` |
| `probe/probe.py` | `eec97f3cc972f07c6d5c45b18bbff4aa67ab4fc8` |

**Metrics**: 3 user stories · 6 FR · 5 SC · 12 tasks · 19 traceability rows = 14 `test` · 3
`inspection` · 2 `manual` · **0 CRITICAL, 0 HIGH**.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A001 | MEDIUM | `data-model.md` described the picker body's padding as `0 8px`, while the sheet carries `padding: 4px 8px 10px` — the figure a reader would use to reproduce the row width. | **fixed — mechanical.** The line now reads `4px 8px 10px`; the SHA above is the fixed file, and `probe/probe.py` measures `clientWidth − paddingLeft − paddingRight` rather than hard-coding 16. |
| A002 | LOW | `plan.md` declares `bump: patch` → 1.23.2 while slices 155, 158 and 165 are in flight; whichever merges first takes the number. | **accepted.** The level is what the plan may declare; C-GIT-VER stamps the number against `develop` in the pre-merge commit. Recorded on the plan's `Bump` line. |
| A003 | LOW | SC-005 (both cases fail on 1.23.1) is verified by `inspection` and has no task that writes a test — a test cannot assert its own redness. | **accepted.** The evidence is the stashed-stylesheet run recorded in `converge.md`, with its two messages; a task would only restate it. |
| A004 | LOW | US2 AC2 (name at the row's left padding, date at its right) is `inspection`, although the one-column case measures the row's width: the test never reads the date's own box. | **accepted.** The row's width plus the flex order (the date is the row's last item, the rule that already right-aligns it at 560px) is the evidence; a date-box assertion would re-test the mockup's anatomy, not this slice. |

No CRITICAL, no HIGH, no intent-level conflict: nothing in the plan narrows or contradicts a
requirement, and every FR and SC appears in the traceability table against at least one task.

## History

- **2026-10-29 — first run.** 4 findings (1 MEDIUM, 3 LOW); A001 applied as a mechanical fix and the
  artifact re-read; A002–A004 accepted with the reasons above. Coverage 100% (6/6 FR, 5/5 SC, 3/3
  stories).
