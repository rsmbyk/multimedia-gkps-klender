# Tasks 070: Manual breaks for Single-screen Text entries

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Implement on the existing `feat/069-manual-text-screen-breaks` branch and PR #323, as the owner requested
- [x] Add kind-specific boundary and default tests in `multimedia/tatib/tests.py`
- [x] Green — validate Single-screen custom boundaries while preserving both kinds' defaults
- [x] Add save/reset, projector grouping, stale-edit, permissions, and voice tests in `multimedia/web/tests.py` and `multimedia/web/test_speaker_voices.py`
- [x] Green — preview payload, save endpoint, text-edit invalidation, projector grouping, and modal controls
- [x] Add browser acceptance in `tests/e2e/test_single_screen_text_breaks.py`
- [x] Green — browser acceptance, including live projector refresh
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on ITEM-073 and spec header
- [x] Share the existing `VERSION` 1.7.0 and changelog section with Spec 069 in PR #323; set ITEM-073 `release_version`
- [x] Update ITEM-073 and [`backlog/board.md`](../../backlog/board.md) in the same PR
- [x] Conventional Commit and update draft PR to link `./spec.md`

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Named tests are green
- [x] Board, tasks, and version are complete in the implementation PR
