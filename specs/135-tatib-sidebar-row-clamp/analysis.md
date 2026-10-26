# Analysis: a Tata Ibadah sidebar row is three lines, ellipsized

**Date**: 2026-10-26 · **Gate**: opens at zero CRITICAL and 100% coverage.
**Artifacts read** (sha256, first 12):

| Artifact | Digest |
| --- | --- |
| `spec.md` | `8473e65d9b8d` |
| `plan.md` | `b16496826c01` |
| `research.md` | `a147258399e1` |
| `data-model.md` | `bc1b529284f6` |
| `contracts/toc-item.md` | `46c586acd336` |
| `quickstart.md` | `4728c16d6eb0` |
| `tasks.md` | `9a7f93e523bb` |
| `checklists/requirements.md` | `e5916aed9785` |

**Metrics**: 10 requirements · 5 success criteria · 9 story scenarios · 3 edge cases (27
traceability rows) · 16 tasks (9 of them tests) · coverage **100%** · CRITICAL **0**.

## Findings

| # | Class | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | note | FR-001 and SC-001 are satisfied by the same E2E function (a row that is three lines and a page where no row exceeds three lines are the same measurement at three viewports). | Kept: two statements, one command. Recorded so the reader does not look for a second test. |
| F2 | note | `quickstart.md`'s test commands are marked not-yet-runnable: the tests are written in Implement (T002, T005–T006, T008–T009, T011). | Expected ordering under TDD; the commands are named so Implement's red run needs no invention. |
| F3 | low | The preview's `build_preview.py` mutates the rendered page (scripts stripped, rows re-marked). After Implement the mutation is a no-op, but the script stays in the repo as a preview tool. | Kept: it is how the preview was built and what makes it reproducible; the README says so. |
| F4 | low | FR-008's test also discharges SC-005 (both assert `scrollWidth == clientWidth` on every row). | Kept, same shape as F1. |
| F5 | none | The capability file has no `R11` yet. | Not a defect: Fold adds it (T014), and the spec cites `new: reading`. |

No mechanical fixes were needed: every requirement has at least one task, terminology is consistent
(`row`, `label_lines`, `Bait …` line), and every path named in the plan exists in the worktree
(`multimedia/web/reading/views.py`, `_toc.html`, `components.css`, `offline-render.js`,
`multimedia/web/tests.py`, `tests/e2e/test_reading.py`, `tests/e2e/test_saved_render_parity.py`).

## History

- **2026-10-26 — first run**, on the Accepted spec and the plan above: 0 CRITICAL, 100% coverage,
  five findings, all notes or low, none fixed silently.
