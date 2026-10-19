# Tasks 115: Play audio media entries

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing targeted tests first, then implementation and verification. -->

## Checklist

- [x] Draft explicitly Accepted by the project owner.
- [x] Recheck the `feat/115-audio-media-display` branch against current `develop` before implementation.
- [x] Red — targeted Django tests in `multimedia/web/test_media.py` for Audio-only Preview metadata, exactly one projector screen, and preserved ordering/other-media behavior.
- [x] Green — emit safe Audio metadata from `multimedia/web/reading/views.py` and existing reading/projector templates without sending bytes through Django.
- [x] Focused browser E2E class under `tests/e2e/` for real local Audio playback, titled/untitled Preview, seek and Space, projector navigation/reset, idle/paused states, missing/decode failure, and display-off.
- [x] Green — load verified local audio through the companion; implement the approved Preview and projector transports, URL cleanup, and stale-request guards in focused browser JS/CSS.
- [x] Update the projector shortcuts sheet with contextual Audio Space, preserving the existing Display row and overlay key precedence.
- [x] Run targeted Django tests and the focused browser E2E class locally; CI runs the full suite after push.
- [x] Fill Traceability in `./spec.md` with final paths.
- [x] In the same implementation PR, update ITEM-115 and the board to In review, set the minor version bump and changelog/release_version, and check completed tasks before merge.
- [x] Conventional Commit and draft PR to `develop` linking `./spec.md`.

## Done when

- [x] All acceptance scenarios in [spec.md](./spec.md) hold.
- [x] The owner has Accepted this Draft before implementation.
- [x] Tests, board/ITEM, version, changelog, and PR evidence land together.
