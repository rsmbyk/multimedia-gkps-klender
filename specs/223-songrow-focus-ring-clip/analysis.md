# Analysis: song-row focus ring is clipped at the list top

**Date**: 2026-11-22 · **Gate**: opens at zero CRITICAL and 100% coverage.

**Artifacts read** (sha256, first 12):

| Artifact | Digest |
| --- | --- |
| `spec.md` | `ed600cabb65c` |
| `plan.md` | `9a99f65fad72` |
| `research.md` | `21669f5c8cd4` |
| `data-model.md` | `37e0e4f8c40d` |
| `contracts/none.md` | `f0fca7ff776d` |
| `quickstart.md` | `99bb521b37c8` |
| `tasks.md` | `d478514e869a` |
| `checklists/requirements.md` | `b1849793fdd1` |

**Metrics**: 6 requirements · 5 success criteria · 6 story scenarios · 3 edge cases (20 traceability
rows) · 15 tasks, seven of them test work · coverage **20/20 = 100%** · CRITICAL **0**.

Coverage is read from the traceability table, not re-derived from tasks: every `FR-###`, `SC-###` and
`US1 ACn` in `spec.md` has a row in `plan.md`, and the three edge cases are mapped. No mechanical fix
was needed, so there is no before/after delta.

## Findings

| # | Class | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | medium | The Clarify question for candidate A/B timed out; A was recorded as a skipped-question assumption rather than an answer. | **Accepted at gate 1** — the owner accepted the pack on that basis, and candidate B remains visible in the preview. Reopening B now would re-enter at Clarify (SDD-25). |
| F2 | low | The E2E asserts the clearance relationship (`row.top - host.top >= outlineWidth + outlineOffset`) rather than the literal 3px, so a different implementation that gives the ring room could pass. | Accepted — that is the requirement, not the mechanism. The diff inspection row (FR-006) holds it to candidate A. |
| F3 | low | Three `manual` rows cover themes, viewports and the last row; the three E2E cases run only at 900×700 in dark mode. | Accepted — the preview makes every state reachable by hand; the browser suite stays targeted as the owner asked. |
| F4 | note | `reading/R52` is provisional until Fold; a sibling slice could claim it while this pack is open. | Recorded — re-check `### R<n>` on `origin/develop` before the delivery commit and renumber if taken. |
| F5 | note | `CONSTITUTION.md` does not exist, so Plan's Constitution Check is a no-op; the constraint row stands in. | Recorded in `plan.md`. |
| F6 | low | The spec index row for slice 222 was missing from `specs/README.md` on the base; this slice adds only its own row. | Accepted — unrelated drift, left for its own correction. |

## History

- 2026-11-22 — first run, pack as of the digests above: coverage 20/20, CRITICAL 0, one medium
  finding accepted at gate 1 and five notes/lows recorded. Gate 2 may open.
- 2026-11-22 — red run before the CSS change: 3 cases, 2 failures with
  `AssertionError: the ring needs 2px above the row, but only 0px is available`; the third case was
  green as the characterisation guard. No timeout or import error.
- 2026-11-22 — green run after `components.css:1669`: 3 cases, `OK` in 8.378s. Live page at `:8767`
  measured row top 133.0px against host top 130.0px, `padding-top: 3px`, outline unchanged.
- 2026-11-22 — `tests.e2e.test_reading` regression: 95 cases, 1 failure
  (`test_the_panel_shows_its_empty_view_when_no_songbook_exists`). The same failure was reproduced on
  the clean `develop` checkout at `8bf20f69` with a separate database; `tests/e2e/test_reading.py`
  is unchanged through this branch's re-based base `e8e79dbb`. Already represented by ITEM-137; not
  attributed to this slice.
- 2026-11-22 — base moved while the slice ran: slice 221 merged as `e8e79dbb`, taking `VERSION` to
  1.36.8. The branch was fast-forwarded (only one conflict, the capability file's `slices` header,
  resolved by keeping the base's entry and prepending this slice). The version declaration moved to
  1.36.8 → 1.36.9; the patch level and every identifier are unchanged. The re-run is recorded below.
- 2026-11-22 — visible-ring control: with a 3px red outline at a 2px offset the unfixed page loses
  its top band above y=130, while the fixed page paints it at y=130; the dark UA outline is too close
  to the canvas for a pixel diff, so the test asserts clearance instead.
