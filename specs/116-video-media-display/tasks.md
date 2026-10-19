# Tasks 116: Display Video media entries

- **Status:** Accepted (owner, 2026-10-19)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Red targeted test → implement → green. Browser E2E is covered by CI after push. -->

## Checklist

- [x] Draft explicitly Accepted by the project owner.
- [x] Continue on the owner-requested shared `feat/115-116-audio-video-display` branch and PR #364.
- [x] Red — targeted Django tests in `multimedia/web/test_media.py` for Video-only metadata and projector order, with other families unchanged.
- [x] Green — emit Video-specific Preview/projector data and preserve the immutable local media identity.
- [x] Red — focused browser E2E in `tests/e2e/test_video_display.py` for local playback, seek, modal dismissal, fullscreen, idle, keyboard, missing/decode failure, and lifecycle cleanup.
- [x] Green — implement Video Preview and projector transport, fullscreen transitions, keyboard behavior, and Video-specific unavailable icons.
- [x] Update the projector shortcuts sheet from `Audio Play/Pause` to contextual `Audio/Video Play/Pause`; retain `Show or Hide Words` for other entries and preserve overlay/key precedence.
- [x] Run the targeted Django tests and focused Video E2E class plus Audio/Image browser regressions.
- [ ] Confirm full PR CI is green at the updated head.
- [x] Fill Traceability in `./spec.md` with final implementation paths.
- [x] Move ITEM-116 from Speccing into In progress after Draft acceptance.
- [x] Include final Video changelog text and version `1.17.0` in the shared PR with ITEM-115; do not increment the version a second time for this same PR.
- [x] Conventional Commit and update draft PR #364 to link this spec (same PR).

## Done when

- [x] All acceptance scenarios in [spec.md](./spec.md) hold.
- [ ] Targeted tests are green and CI evidence is recorded on the PR head.
- [x] Board, tasks, changelog, ITEM, and PR references are complete in the same PR.
