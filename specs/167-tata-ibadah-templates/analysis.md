# Analysis: a Tata Ibadah is a service or a template

**Date**: 2026-10-30
**Artifacts read** (SHA-1, as written):

| Artifact | SHA |
| --- | --- |
| `spec.md` | `1527a7fd49a5a88a13fa6b3438402153b90ef0f5` |
| `plan.md` | `83f27cb32e90e910597a5ae7750a9614ec9e88d8` |
| `tasks.md` | `b4cc0ffa1102d732678a06ce53c328bb19f81435` |
| `research.md` | `08a678360dba70dc8d18982fe015a15b3ae9fbd6` |
| `data-model.md` | `c70c5f3c888b10ba5cdb4b9870410decf7f190a6` |
| `quickstart.md` | `bb826388f3e69cf0af1d495870127b0d4a5d5d61` |
| `contracts/README.md` | `58e7ef889fd6781fe4990087a94754038bbaa405` |
| `checklists/requirements.md` | `66e40aaeae561d72366ae28ecbd0c622c52114c6` |
| `preview/probe.py` | `fe479f858b149dbba3d363c7af821cda7c3447ba` |

**Metrics**: 5 user stories · 24 FR · 6 SC · 39 tasks · 69 traceability rows = 67 `test` · 2
`inspection` · 0 `manual` · **0 CRITICAL, 0 HIGH, 0 open MEDIUM, 3 LOW**. Coverage 100% (24/24 FR, 6/6 SC,
38/38 scenarios, 5/5 stories).

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A001 | MEDIUM | The running order is reorderable today (`static/web/reorder.js`, `entry_reorder` at `views.py:597`), and a choice now owns child rows. The plan said nothing about dragging a choice: moving it away from its options would leave them rendering under another entry, and `entry_reorder` names entries one by one, so the client could send only the parent. | **fixed — owner's decision.** A choice moves as a block: `reorder.js` sends the choice followed by its options and the endpoint keeps them contiguous. The rule is now in `plan.md`'s design, its traceability table (`test_a_choice_moves_with_its_options`) and `tasks.md` T020. |
| A002 | LOW | A template's Media files dialog tags each row `data-media-past="true"`, because `service_media_past = not service.date or service.date < today` (`views.py:1951`). That flag is what offers the manual download control (`media-handoff.js:110`). | **accepted.** FR-024 forbids *automatic* download, not a manual one; a template's operator may still fetch a file to preview it. The name reads oddly for a template, but the behaviour is the wanted one and no requirement says otherwise. |
| A003 | LOW | The chooser's **Preview** opens the app's preview dialog on top of the generate modal — a third layer — and no task verifies that closing it returns to the generate modal rather than closing it. | **accepted.** An HTML `<dialog>` closes only itself; the parent modal is a separate open dialog, so the return holds by construction. T028 exercises the chooser's own three dismissal paths, and the spec's states clause names the Preview case explicitly. |
| A004 | LOW | `plan.md` declares `bump: minor` → 1.24.0 while sibling slices are in flight on `develop`. | **accepted.** The level is what a plan may declare; the number is stamped against `develop` in the pre-merge commit (C-SDD-VER), and A12 already requires the capability numbers to be re-read then. |

No CRITICAL, no HIGH, no open MEDIUM, and no requirement is narrowed or contradicted: every FR and SC carries a plan row
with a verification method, and every one of them is reachable from at least one task.

## Applied mechanically

- `plan.md`'s verification split read 54 `test` before the table was counted; the table holds 66, and both
  the split line and the exit-gate row now say 66.
- `tasks.md` numbering runs T001–T038 with no gaps; each `test` row from the plan appears in a task that
  names its test functions, so the traceability table can be walked in either direction.

## History

- **2026-10-30 — first run.** 4 findings (1 MEDIUM, 3 LOW); A002–A004 accepted with the reasons above;
  A001 escalated to the owner at gate 2 with a recommendation and its cost. Coverage 100%.
- **2026-10-30 — second run.** A001 fixed by the owner's choice (a choice moves as a block): the rule
  joined the plan's design and traceability and became T020, tasks renumbered T020–T039 with no gaps, the
  split reads 67 `test`. SHAs re-taken; no new finding, 0 open MEDIUM.
