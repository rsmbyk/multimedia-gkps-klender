# Analysis: a playing recording owns the projector screen until it pauses

**Date**: 2026-10-29 · **Gate**: opens at zero CRITICAL and 100% coverage.
**Artifacts read** (sha256, first 12):

| Artifact | Digest |
| --- | --- |
| `spec.md` | `7ed930c3a6cc` |
| `plan.md` | `71117690174d` |
| `research.md` | `be4cbc776423` |
| `data-model.md` | `3078d166e4d7` |
| `contracts/none.md` | `80aa928da8ad` |
| `quickstart.md` | `3f292470b1e3` |
| `tasks.md` | `8d2b42426fe7` |
| `checklists/checklist.md` | `3374d4f8c35c` |

**Metrics**: 10 requirements · 3 success criteria · 8 story scenarios · 5 edge cases (17 traceability
rows) · 17 tasks (8 writing or driving tests) · coverage **100%** · CRITICAL **0**.

`check_pack_consistency.py specs/155-audio-presentation-lock` → `COVERAGE 13/13`, `SPLIT 16/1/0`,
`ASSIGNMENT 12/12`, `clean`. The split was re-derived after the regression row was added; the first run
counted `15/1/0` and reported the video module as an orphan, which is why the plan now carries that row
explicitly.

## Findings

| # | Class | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | note | FR-002's pointer evidence has two shapes: while the takeover holds, the mouse zones are not painted, so the case clicks where the next zone sits (on the fullscreen box) and, under a refused fullscreen, clicks the zone itself. | Kept: both are in `test_projector_playing_audio_ignores_pointer_navigation`, so the guard is exercised where the zone is reachable and the takeover is exercised where it is not. |
| F2 | low | Headless Chromium does not leave fullscreen on a bare `Escape` press — measured — so the escape case holds the key for 1000 ms, which is the app's own gesture (`projector.js:1324`, 900 ms). | Accepted: the case exercises the shipped gesture rather than a browser behaviour the app never relied on. |
| F3 | note | The E2E harness stubs `http://127.0.0.1:63174/v1/files/<sha>` with `page.route`, so the companion's origin allow-list never enters the test; only the live preview fetches the real file. | Recorded: `quickstart.md` carries the preview recipe and the probe, and the spec's numbers come from that run. |
| F4 | none | The behaviour folds as a new `projector/R3` rather than a modification of R1 (Go To) or R2 (page renders from its own response): it fails alone, and neither existing requirement changes. | Recorded: Fold adds R3 (T017). |
| F5 | note | FR-010 (`c`/`t` keep working) has no test: both keys are read below the guard and touch no audio state. | Accepted as the pack's one `inspection` row, read back at T016. |
| F6 | note | The preview's code was parked before gate 2 and is re-applied after it, tests first; the branch's first commit therefore carries the Draft pack alone. | Kept: the acceptance order is the record, and the implementation commit follows the gate rather than preceding it. |
