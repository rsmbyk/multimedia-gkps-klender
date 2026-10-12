# Tasks 059: Color liturgy speakers as a congregation cue

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch `feat/059-speaker-colors` from `develop` (its own worktree; the highlight branch is untouched)
- [x] Red — `multimedia/web/test_speaker_voices.py`: leader labels, bare `P`, joined forms, ordinary speakers, cues, sentences and references, continuation across a blank line, a new item resetting, and rendered classes for a text, a single-screen text, a legacy row, a song, a passage, the stage, and the preview — fails on the missing `voices` module
- [x] Red — `tests/test_design_tokens.py`: `--speaker-join` and `--speaker-leader` on `--canvas` in both themes (at least 4.5:1), ordinary contrast above join, join above leader — fails with `--speaker-join missing from :root`
- [x] Green — `multimedia/web/reading/voices.py`; `multimedia/web/reading/views.py`; `projector.html` and `tatib.html`; `tokens.css`, `projector.css`, `components.css`
- [x] Red — E2E `tests/e2e/test_speaker_voices.py`: light and dark stage, projector, computed colors for leader, congregation, joined, and the gold header
- [x] Green — targeted runs (`tests.test_design_tokens`, `multimedia.web.test_speaker_voices`, `multimedia.web.tests`, `SpeakerVoicesE2ETests`, `ProjectorE2ETests`); full suite is the push step
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
