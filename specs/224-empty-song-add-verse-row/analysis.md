# Analysis: Empty song paints one Add verse control

**Date**: 2026-11-23 · **Gate**: opens at zero CRITICAL and 100% coverage.

**Artifacts read** (sha256, first 12):

| Artifact | Digest |
| --- | --- |
| `spec.md` | `38944116767b` |
| `plan.md` | `d41a8eec60cc` |
| `research.md` | `916a7e574400` |
| `data-model.md` | `784a68536d34` |
| `contracts/none.md` | `375e1f194cfa` |
| `quickstart.md` | `9a7a3aa90300` |
| `tasks.md` | `0a93acfbe292` |
| `checklists/requirements.md` | `b20b735d55d1` |

**Metrics**: 6 requirements · 5 success criteria · 9 story scenarios · 2 edge cases (23
traceability rows) · 19 tasks, nine of them test work · coverage **23/23 = 100%** · CRITICAL **0**.

Coverage is read from the plan's traceability table, not re-derived from tasks: every `FR-###`,
`SC-###`, `US1 ACn` and edge case in `spec.md` has a row. No mechanical fix was needed, so there is
no before/after delta.

## Findings

| # | Class | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | low | The static preview shows the proposed state by removing the `.verse-add` element from captured markup; it cannot run the server-side `{% if %}`. | Accepted — the live route supplies the before measurement and the post-change readout through `probe.py`; the preview's own README states the limit. |
| F2 | note | `reading/R40` is modified in place rather than adding `R53`. | Recorded — the behaviour narrows an existing requirement; re-check R40's wording against `origin/develop` at Fold. |
| F3 | low | SC-003's "button does not move" is only predicted from the static preview (x=1060.1, 111.8×38). | Accepted with a `manual` row requiring a live re-measure after T006; the row is not marked done until then. |
| F4 | note | Card `ITEM-239` entered `Ready` on the gate-1 Accept and was anchored on issue #590. | Recorded in the card; the PR carries `Refs #590`, never `Closes`. |
| F5 | note | `preview/test.sh` names `test_verse_add_gate.py`, which does not exist until T001. | Recorded in the plan's task order; the script is for the Implement pass, not for the gate-2 reader. |
| F6 | note | The first gate-1 question timed out; the owner's next turn was the single word `accept`. | Accepted as gate 1 — the accept named the drafted pack explicitly, and no implementation has happened. |
| F7 | note | No `CONSTITUTION.md` exists, so Plan's Constitution Check is a no-op. | Handled in `plan.md`; the constraint row stands in. |
| F8 | medium | The owner added US2 while gate 2 was open, so the plan pack was rewritten and gate 1 re-opened. | Accepted on 2026-11-23 with the revised preview; the earlier gate-1 accept covered US1 only and no implementation happened in between. |
| F9 | low | At 390×844 the two empty titles differ by 5.5px because the song title wraps to a taller header. | Recorded as tolerance in US2 AC4 and SC-005, not held to the 1px criterion; the mechanism is the same. |

## History

- 2026-11-23 — first run on the one-story pack: coverage 16/16, CRITICAL 0, three low findings
  and four notes. Gate 2 opened.
- 2026-11-23 — US2 added at the owner's word during gate 2; gate 1 re-opened and accepted on the
  revised preview. Second run on the pack whose digests are above: coverage 23/23, CRITICAL 0,
  four low findings, one medium finding accepted at re-opened gate 1, and four notes. Gate 2 may
  open again.
- 2026-11-23 — red run before either product edit: 13 tests, 5 failures, all for the intended
  reasons — `'class="verse-add"' unexpectedly found` (two subtests), `2 != 1` button count (two
  subtests), and `47.609375 not less than or equal to 1.0` between the two titles at 1440×900.
  No import, fixture or database error.
- 2026-11-23 — green run after `song.html:45` and the three `components.css` rules: 13 tests,
  `OK` in 7.967s on `gkps224`.
- 2026-11-23 — live readout after `collectstatic`: empty song 1 button, 0 rows, title y=253.9;
  Tata Ibadah reference y=253.5; with-verses row unchanged at x=856, y=681.3; 390×844 residual
  5.5px as recorded. Convergence passed in two passes; R40 modified at Fold.
