# Analysis: an audio preview reads its times as `current / total`

**Spec**: `specs/154-audio-times-inline/spec.md` · **Date**: 2026-10-29
**Artifacts read**: `spec.md` `94fa91640fb5` · `plan.md` `5d591de11ed2` · `tasks.md` `949a59873cc6` ·
`research.md` `6cd09ee254f3` · `tatib.html` `18f6a4c9904d` · `components.css` `43bf4eb52921` ·
`test_audio_display.py` `24dad5fc8f5a`

## Metrics

| Measure | Value |
| --- | --- |
| Requirements | 4 FR · 4 SC |
| Stories | 2 (US1 P1, US2 P2) |
| Scenarios | 5 + 5 edge cases |
| Tasks | 10 (9 done, 1 held for the merge) |
| Verification split | 8 test · 5 inspection · 5 manual (18 rows) |
| Coverage (rows with ≥1 task) | 18 / 18 = 100% |
| Critical | 0 |

## Findings

| # | Finding | Severity | Disposition |
| --- | --- | --- | --- |
| F1 | FR-004 ("nothing else changes") is verified by inspection and the probe table, not by an automated pixel comparison of the dialog. The probe is a script, but its output is a table a reader compares by eye. | LOW | Accepted — the E2E's own geometry assertions cover the parts that can regress (the pair, the bar); the rest is CSS this slice does not touch, and `git diff` names the two lines. |
| F2 | SC-001/SC-002 are `manual`: the live preview's numbers were measured once, by script, and copied into the spec. A later regression in the pair's alignment would not be caught by them — but it *is* caught by SC-003's case. | LOW | Accepted — the manual rows record the approved look; the test row is what fails on regression. |
| F3 | E1 (unknown duration) has no case of its own: the initial markup prints `0:00` / `0:00`, and the browser's metadata may land before a probe can look. | LOW | Accepted — the shape is the markup's, not a runtime path; the case would race the media element. |
| F4 | E2 (`62:03` past an hour) is declared as inspection because no fixture in the module is an hour long. | LOW | Accepted — `clock()` is untouched and has no wrap point; adding an hour-long fixture would slow the module for a formatter this slice does not read. |

No CRITICAL, no HIGH. No mechanical fixes were needed: every FR has its rows, the terminology matches the
capability file's (`current / total`), and no requirement duplicates another statement.

## History

| Run | Date | Critical | Coverage | Note |
| --- | --- | --- | --- | --- |
| 1 | 2026-10-29 | 0 | 18/18 | first run, gate 2 |
