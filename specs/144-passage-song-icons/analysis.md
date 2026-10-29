# Analysis — slice 144

**Date**: 2026-10-28 · **Stage**: Analyze (gate 2 input)
**Artifacts read** (sha256, first 8):

| artifact | sha |
| --- | --- |
| `spec.md` | `d8ad7610` |
| `plan.md` | `fecc4a50` |
| `tasks.md` | `36a06b69` |
| `research.md` | `d657aae6` |
| `data-model.md` | `0090fa1a` |
| `contracts/stage-markup.md` | `4657f410` |
| `quickstart.md` | `cca5084e` |
| `checklists/requirements.md` | `9f919842` |

**Metrics**: 22 traceability rows (8 `FR`, 5 `SC`, 9 story scenarios) · **coverage 100%** · 0 CRITICAL ·
0 HIGH · 2 MEDIUM · 3 LOW · 17 tasks · 11 distinct E2E functions, each named in `tasks.md`.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A1 | MEDIUM | The two rows that carry the request's actual promise — *the kinds are told apart without reading* (US1.3) and *the chip still reads heavier* (US2.1) — are `manual`. Everything else is measured. | **Accepted.** They are judgements about reading, not geometry; a test would only re-measure size and colour, which SC-002 already does. Gate 2 shows them as the two rows that rest on a person. |
| A2 | MEDIUM | `FR-005` first read "the marking SHALL NOT change a row's height". That is false at the media column: the four fixture songs each gain a line (+23.8px). | **Fixed.** The requirement now claims only that the mark adds no height of its own; the wraps are declared with their cost, and the retraction is kept visible in `spec.md` §Clarifications. |
| A3 | LOW | `plan.md` declared the verification split as `18 test · 1 inspection · 2 manual`; the table holds **19** test rows. | **Fixed (mechanical).** Split corrected in the plan and its exit gate. |
| A4 | LOW | The spec says *mark*, the class is `entry__kind-icon`, and the media one is a *chip*. Three words for two things. | **Accepted.** The class name mirrors `entry__media-icon` on purpose — a shared suffix is worth more than prose purity — and the spec defines both terms in §Key Entities. |
| A5 | LOW | `research.md` and `plan.md` cite `components.css` line numbers that will move when this slice edits the same block. | **Accepted.** Every citation also quotes the rule, so `grep` finds it after the shift. |

## Checks that found nothing

- **Requirement coverage** — every `FR-001…008`, `SC-001…005` and every one of the nine story scenarios
  has a traceability row; none is duplicated, and no requirement appears twice in different words.
- **Task coverage** — all 11 test functions named in the plan appear in `tasks.md`, and each `test` row
  maps to at least one task. `inspection` (US3.4) and `manual` (US1.3, US2.1) rows produce no test task,
  as the contract requires.
- **Entity coverage** — `data-model.md` states "none" with the three item keys the mark reads; no
  migration, no serializer, no query.
- **Interface coverage** — `contracts/stage-markup.md` exists and says why there is no external interface.
- **Stale references** — no `specs/142`, `specs/143` or `ITEM-154` left in the pack; the only `1.22.4` is
  the bump task's *from* value, which is `VERSION` on `develop` today.
- **Unrequested work** — nothing in `tasks.md` falls outside `FR-001…008`; the sidebar and the dock are
  named only to be excluded (FR-008).

## History

- **2026-10-28 — pass 1** (these SHAs): 22 rows, 0 CRITICAL, coverage 100%, 1 mechanical fix (A3), 1
  retraction honoured (A2). Gate 2 may open.
- **2026-10-28 — correction** (Converge pass 1): this report counted **13** E2E functions; two of the
  matches were module names, so the pack names **11**. The metric above is corrected; nothing else in
  this report changed.
