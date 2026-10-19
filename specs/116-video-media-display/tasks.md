# Tasks 116: Display Video media entries

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Red targeted test → implement → green. Browser E2E is covered by CI after push. -->

## Checklist

- [ ] Draft explicitly Accepted by the project owner.
- [x] Continue on the owner-requested shared `feat/115-116-audio-video-display` branch and PR #364.
- [ ] Red — targeted Django tests in `multimedia/web/test_media.py` for Video-only metadata and projector order, with other families unchanged.
- [ ] Green — emit Video-specific Preview/projector data and preserve the immutable local media identity.
- [ ] Red — focused browser E2E in `tests/e2e/test_video_display.py` for local playback, seek, modal dismissal, fullscreen, idle, keyboard, missing/decode failure, and lifecycle cleanup.
- [ ] Green — implement Video Preview and projector transport, fullscreen transitions, keyboard behavior, and Video-specific unavailable icons.
- [ ] Update the projector shortcuts sheet from `Audio Play/Pause` to contextual `Audio/Video Play/Pause`; retain `Show or Hide Words` for other entries and preserve overlay/key precedence.
- [ ] Run the targeted Django tests and focused Video E2E class; CI runs the full suite for the PR.
- [ ] Fill Traceability in `./spec.md` with final implementation paths.
- [ ] Keep ITEM-116 and the board in Speccing until this Draft is Accepted; then Ready, In progress, and In review per process.
- [ ] Include final Video changelog text and version `1.17.0` in the shared PR with ITEM-115; do not increment the version a second time for this same PR.
- [ ] Conventional Commit and update draft PR #364 to link this spec (same PR).

## Done when

- [ ] All acceptance scenarios in [spec.md](./spec.md) hold.
- [ ] Targeted tests are green and CI evidence is recorded on the PR head.
- [ ] Board, tasks, changelog, ITEM, and PR references are complete in the same PR.
