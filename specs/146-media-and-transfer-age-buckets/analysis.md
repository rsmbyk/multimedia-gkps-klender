# Analysis: the Media Library and the transfer history group by age

**Run**: 2026-10-28 · **Slice**: `specs/146-media-and-transfer-age-buckets`
**Artifacts read** (sha256, first 12, after this run's mechanical fixes): `spec.md` 2a9f0b418bbc ·
`plan.md` cc2557c75da6 · `tasks.md` 19bf51ec8886 · `research.md` e7d2ac33a52a · `data-model.md`
580bb27fdd41 · `contracts/README.md` 5c44ee3f9314 · `quickstart.md` 56d12dc2a489 ·
`checklists/requirements.md` b6400dc17234 · `preview/preview.html` a20d885827fa · `preview/README.md`
954beb05be43

**Metrics**: 17 FR · 7 SC · 14 story scenarios · 23 tasks · 17 tests · 3 inspection · 0 manual.
**Coverage 100%** (17/17 requirements reach at least one task through the plan's traceability table, 7/7
success criteria reach a named verification). **0 CRITICAL · 0 HIGH · 2 MEDIUM · 3 LOW · 1 INFO.**

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A1 | MEDIUM | Neither the spec nor the initial contract says what happens to a row whose timestamp will not parse. `fileKey`/`transferKey` must be total (`contracts/README.md` guarantee 1 said "every row with a parseable timestamp" and stopped there), so the behaviour was undefined exactly where a malformed companion row would land. | **Fixed** mechanically: the contract now states that an unparseable timestamp is drawn in `older` and never dropped, so no row disappears from a list. The spec is untouched — it never promised the case either way, and the contract owns a total function's fallback. |
| A2 | MEDIUM | The plan's verification split was typed as "15 test · 4 inspection" while its own rows give 14 test rows (two of them also inspected) and 3 inspection-only rows. A gate-2 reader counting the split would find it disagreed with the table under it. | **Fixed** mechanically in `plan.md`: the split reads `14 test · 3 inspection · 0 manual`, with the two tested-and-inspected rows named, and the exit-gate row restated. |
| A3 | LOW | Terminology drift: US1's title, its task phase, one traceability row and the preview's state table called the buckets "shelves", while every requirement, key and test says "bucket". | **Fixed** mechanically: all four now say bucket; the vocabulary is `bucket` throughout, as `reading/R9` already has it. |
| A4 | LOW | The spec first claimed the companion's eight files draw "five headings". They draw four (`28`, `25`, `19`, `17` Oct). Caught before gate 1 and corrected in `spec.md` and `preview/README.md`. | **Fixed** before gate 1; recorded here because the analysis reads the corrected text and a later reader should know the claim was checked against the payload. |
| A5 | LOW | FR-009 writes the rungs as "24 hours to 7 days" and "7 to 30 days", which leaves the instant exactly 24 h old to inference. | **Accepted** as-is in the spec; `data-model.md`'s boundary table fixes the reading — `24h ≤ age < 7d`, `7d ≤ age < 30d` — so the implementation and its tests have one answer. |
| A6 | INFO | `renderTransfers()` already rebuilds every row on each 2-second poll; it now rebuilds the headings with them. No state is lost (the dialog holds none, and the rail's session object lives outside the DOM), but a reader should know the heading walk runs on a timer, not once. | **Accepted**; pre-existing shape, and the walk is O(rows) over a list the companion caps by its own retention. |
| A7 | INFO | The owner accepted gate 1 while the two new transfer labels rested on a recorded assumption: the question was asked through the tool and timed out unanswered, and `Last 24 hours` · `Last 7 days` was recorded as the recommendation. | **Accepted** by gate 1. The preview still carries the alternative behind a control, and a change at gate 2 is a one-word revision. |

## Coverage detail

- Every `FR-001`…`FR-017` appears in the plan's traceability table and is reached by at least one task.
  FR-006 and FR-013 are the two rows carrying both a test and an inspection; FR-008, FR-015 and FR-016
  are inspection-only by design (a diff of the row builder; a diff of the transfer row; a grep proving the
  rule is defined once).
- Every `SC-001`…`SC-007` names its measurement; SC-007 is the suite run rather than a test.
- Every story scenario (US1.1–1.5, US2.1–2.7, US3.1–3.2) appears in the scenario table with a test, except
  none — all fourteen resolve to a test, so no scenario rests on prose.
- No requirement is un-verifiable; no task exists without a requirement behind it (23 tasks, of which 16
  are the test/code pairs for the plan's test rows, 1 is Setup, and 6 are the delivery and bookkeeping
  steps the repo's git, versioning and board parts declare).

## History

- 2026-10-28 — run 1: 0 CRITICAL, 0 HIGH, 2 MEDIUM, 3 LOW, 1 INFO; coverage 100%.
- 2026-10-28 — delta before run 2: A1 fixed in `contracts/README.md` (fallback stated), A2 fixed in
  `plan.md` (split restated), A3 fixed in `spec.md`, `tasks.md`, `plan.md` and `preview/README.md`
  (shelves → buckets). A4 was already fixed before gate 1. Re-read at the SHAs above: no new finding, no
  requirement moved, coverage still 100%. Gate 2 may open.
