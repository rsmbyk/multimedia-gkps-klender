# Analysis — the rail's marks and the stage's own

**Date**: 2026-10-29
**Artifacts read**: `spec.md` `e46ebb00` · `plan.md` `f6861de0` · `research.md` `88116a9f` ·
`tasks.md` `eee5b663` · `checklists/requirements.md` `7783cef3` · `preview/preview.html` `98f2d3ba`
**Metrics**: 9 requirements · 13 acceptance scenarios · 24 tasks · 100% coverage · **0 open CRITICAL ·
0 open HIGH · 2 MEDIUM · 1 LOW open** (5 findings: 2 fixed before this report, 3 accepted and declared)

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| F-001 | HIGH | FR-001 and FR-003 named only the rail, while `plan.md` also changes the Alkitab and Tata Ibadah **panel empty states** — work the requirements did not ask for. | **Fixed** — both FRs now name the panel's own empty state; the traceability rows carry the second file range. |
| F-002 | MEDIUM | §What the page does today claimed "three different open books"; the product draws **two** different paths in **four** copies (rail, panel empty state and Add Passage tile share one; the kind mark is the other). A reader checking the claim would have found it wrong. | **Fixed** — the paragraph and `research.md` now state two drawings across four places, with each file cited. |
| F-003 | MEDIUM | SC-004 ("a song row and an audio row draw different silhouettes") rests on a manual read; the test can only assert that the paths differ. | **Accepted** — the plan's traceability row declares it `manual` with the exact surface; a silhouette is not a number, and inventing one (bounding-box overlap) would measure ink, not shape. |
| F-004 | MEDIUM | The 20px legibility of the cross is a visual judgement carried by one 4× crop, not an assertion. | **Accepted** — declared `manual` in the plan and backed by the preview; the alternative (enlarging the kind mark to 24px) is a contract change the owner did not ask for. |
| F-005 | LOW | The waveform was chosen at 23px; the upload preview draws the same path at 27px and the pack never rendered that size. | **Accepted** — `manual` check added to T020's sweep; the path scales with the box, and the 27px tile is the loosest of the four. |

## Coverage

Every FR-001…FR-009 and SC-001…SC-005 appears in `plan.md`'s traceability table with a component and a
`Verified by`; the table is the source Analyze reads rather than re-deriving coverage from tasks. Every
task in `tasks.md` names a requirement, a file and a behaviour. **Coverage: 9/9 requirements, 5/5
success criteria, 13/13 scenarios.**

## History

- 2026-10-29 — first run, against the artifacts above: 0 CRITICAL, 1 HIGH, 2 MEDIUM, 1 LOW. F-001 and
  F-002 applied as mechanical fixes; the spec, plan, research and checklist re-read afterwards; this
  report re-issued at 0 CRITICAL, 0 HIGH.
- 2026-10-29 — implement: the seven cases ran **red** against the unmodified templates and failed for
  their own reasons — the rail's Bible is two nodes where the mark has three; the rail's Tata Ibadah is
  a `rect` plus the page's three rules; a song row draws the single flag's ellipse, not the pair's two
  heads; `gkpsMediaIcon('audio')` is the beamed pair. The three geometry/ink cases passed before the
  change, which is what they exist to protect. After the eight markup edits (7 inline SVGs, 2 JS map
  entries) all seven pass, and `tests.e2e.test_stage_kind_marks` (11) passes untouched.
