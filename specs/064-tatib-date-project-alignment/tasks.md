# Tasks 064: Center the Tata Ibadah date and Project button

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner on 2026-10-12
- [x] Branch from `develop` as `chore/064-tatib-date-project-alignment`
- [x] Red — domain/app tests: N/A (presentation-only CSS)
- [x] Red — E2E: `tests/e2e/test_reading.py` — new header geometry check failed by 5 px at 1440 px and 390 px widths before the CSS rule
- [x] Green — implementation: Tata Ibadah-specific date-label margin rule in `static/styles/design/components.css`
- [x] Green — targeted E2E: new date/button alignment test passes at 1440 px and 390 px widths
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: patch` on the ITEM and spec header
- [x] Bump `VERSION` to 1.6.4 and add its changelog section in the same PR
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) (In progress while implementation is underway)
- [x] Conventional Commit + draft PR #320 linking `./spec.md`

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Targeted E2E checks are green
- [x] Board, tasks, and version are complete in the implementation PR
