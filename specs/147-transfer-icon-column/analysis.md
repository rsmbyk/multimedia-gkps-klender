# Analysis: a transfer row's icon column

**Date**: 2026-10-28 · **Gate**: opens at zero CRITICAL and 100% coverage.
**Artifacts read** (sha256, first 12):

| Artifact | Digest |
| --- | --- |
| `spec.md` | `bdb5358175de` |
| `plan.md` | `fe6dd5ead90e` |
| `research.md` | `2f39e7a2090d` |
| `data-model.md` | `3ebcd4a13308` |
| `contracts/none.md` | `f015f41e1e92` |
| `quickstart.md` | `4734c9558970` |
| `tasks.md` | `fc52e6a6e287` |
| `checklists/requirements.md` | `4e54acf430b0` |

**Metrics**: 5 requirements · 4 success criteria · 5 story scenarios · 5 edge cases (19
traceability rows) · 12 tasks (3 of them writing tests) · coverage **100%** · CRITICAL **0**.

## Findings

| # | Class | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | note | FR-001 and SC-001, FR-003 and SC-002 land on the same command: one measurement of four left edges answers all four statements. | Kept: requirements and criteria are different claims, one command observes both. Recorded so a reader does not hunt for a second test. |
| F2 | note | The three tests sit in **Foundational**, not one per story: a single declaration serves US1 and US2, and TDD-01 forbids writing a test after the code it covers. Writing US2's test inside its own phase would have made it green-on-arrival. | Recorded: the ordering is a TDD decision, not a drifted task list. Both stories are still independently demonstrable from their own test. |
| F3 | low | The "active transfer shows a percentage label" edge case has no command of its own — it needs a running companion job, which this suite fakes at the same boundary. | Accepted as `inspection`: once the mark is `flex: none`, the label's width cannot reach the mark; the assertion would prove CSS rather than the row. |
| F4 | low | The preview carries its own copy of the proposed declaration, `[data-option="fixed"] .media-transfers__mark { flex: none }`, because it is a static page with the shipped stylesheet frozen. | Expected: the preview is the design record; `components.css` is the authority once implemented, and Converge re-measures the running app against `spec.md` §UI/UX. |
| F5 | none | `docs/spec/reading.md` has no requirement for the dialog's rows yet; its R12 speaks about file names truncating, not about the column. | Not a defect: Fold adds R20 (T011); the spec's FRs cite `new: reading`. |
| F6 | low | In `test_a_long_transfer_name_still_ellipsizes_at_the_pinned_column`, the 72px height and the truncation both hold on the shipped stylesheet; only the `clientWidth == 482` assertion is red. | Kept: the test names its red reason in its own assertion message, so the TDD-02 check ("fails for the right reason") is readable from the output rather than inferred. |

No mechanical fixes were needed: terminology is stable (`mark column`, `text column`, `transfer row`,
`glyph`), every path the plan names exists in the worktree (`static/styles/design/components.css:2753`,
`static/styles/design/components.css:2796`, `static/web/media-handoff.js:59`,
`multimedia/web/templates/reading/base.html:456`, `tests/e2e/test_media_library.py`), requirement and
scenario IDs are unique, and no requirement is duplicated across the spec and the capability file.

## History

- **2026-10-28 — implement**, T005's red run: the three tests were written and run against the
  unmodified stylesheet before T006. All three failed for their own measurement — mark widths
  `{21, 22.31}` where `{32.0}` is asserted, `clientWidth 493` where 482 is reserved, and the same
  collapsed mark at a 420px window — not on an import or a missing selector.
- **2026-10-28 — first run**, on the accepted spec and the plan: 0 CRITICAL, coverage 100%, six
  findings — two notes (one command serving two statements; the TDD ordering of the three tests),
  three low (an untested percentage edge case, the preview's copy of the rule, one test whose red
  reason is a single assertion), one none (the capability delta awaiting Fold). No mechanical fix was
  applied and the run was not repeated.
