# Converge

## Pass 1 — 2026-11-22

**Checked**: the code against `plan.md`'s traceability table, row by row, with each row checked by the
method it declared (`test` rows re-run, `manual` rows re-measured, the `inspection` row read).

| Requirement | Result | Evidence |
| --- | --- | --- |
| FR-001 (fitted at rest) | met | `test_a_text_screen_arrives_without_being_fitted` passes; `preview/verify_sizes.py` reports 0 of 126 screens differing between the slice's arrival and develop's at-rest size |
| FR-002 (neighbours fitted in idle time; arrival still fits) | met | the same test: max 1 layout read per paced advance, and the first press after a load still arrives fitted |
| FR-003 (remembered by stage and body; cleared on the faces) | met | the resize and fonts-ready paths re-fit; the key's four parts are the fit's four inputs (inspection) |
| FR-004 (largest fitting size kept) | met | `test_a_body_too_long_for_the_screen_comes_down_to_fit` (one pixel more does not fit), the new test (every fitted screen is maximal) |
| FR-005 (the cut halves, same cut) | met | `test_a_single_screen_text_fits_its_whole_body_on_one_screen`; a 400-row body keeps 116 rows / 10 711 characters / 2 px on both builds |
| FR-006 (resize, faces, translation re-fit) | met | `test_a_gap_opens_between_the_words_own_lines` (re-fits on `resize`) |
| SC-001 (no fitting on arrival) | met | `preview/probe.py`: 135.6 → 1.0 reads |
| SC-002 (paced advance inside a frame) | met | 16.4 → 3.7 ms median, 66.9 → 7.4 ms worst |
| SC-003 (rapid advance no worse) | met as stated | 13.9 → 2.3 ms median, 70.4 → 67 ms worst — the fallback path, unchanged in kind (analysis F003) |
| SC-004 (arrival size = at-rest size) | met | 53 mismatches on develop, 0 on the slice |
| SC-005 (existing fitting contracts) | met | four fitting tests pass |
| SC-006 (the cut) | met | 2 992 → 81.5 ms, same rows and characters |

**Browser module**: `tests/e2e/test_projector` — 68 tests, 11 failures/errors, and the same 11 with the
same assertions fail on unmodified `develop` in the main checkout (five Go To locking tests, the
passage translation flip, the missing-PDF resume, the corner-control colours, the screen shapes, the
HUD popups, the keyboard jumps and the service-list picker). No failure names the fitting.

**Findings**: none — `missing` 0 · `partial` 0 · `contradicts` 0 · `unrequested` 0.

**Outcome**: converged on pass 1.
