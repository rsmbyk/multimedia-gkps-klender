# Tasks 091: Quiet controls for the mirrored service projector

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner accepts this Draft spec; stop until then.
- [x] Confirm the current feature branch is based on `develop`; keep preview files as reference only.
- [x] Add targeted domain/application tests for boundaries, translation payloads, lookup, and detours.
- [x] Add projector state and payload helpers for service entries and baits.
- [x] Add targeted `tests/e2e/test_projector.py` cases for keyboard navigation, mouse jumps, overlay interception, and fitting.
- [x] Implement projector keyboard behavior, find, detours, and shortcut sheet.
- [x] Implement the corner HUD, mouse zones, entry list, inactivity, and responsive overlays from the accepted previews.
- [x] Run the targeted projector unit and browser classes (45 passing tests).
- [x] Fill test and implementation paths in `spec.md` traceability.
- [x] Set ITEM-094 to In review, update the board, version and changelog for the minor bump, and open a draft PR against `develop` in the same PR.
- [ ] Before merge, complete the required remote CI and E2E, mark ITEM-094 Done, and check off delivered tasks in the same PR.

## Done when

- [x] Targeted projector scenarios pass and mouse and keyboard operation both work.
- [x] Implemented geometry and interaction states follow the accepted preview.
- [x] ITEM, board, tasks, version, changelog, and PR all describe the same delivered slice.
