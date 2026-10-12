# Tasks 069: Manual screen breaks for multiline Text entries

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Draft accepted by the project owner
- [x] Confirm the current `develop` head and spec/ITEM IDs before implementation
- [x] Tests for automatic and custom grouping, blank-line boundaries, voice continuity, and invalid/stale metadata (`multimedia/tatib/tests.py`, `multimedia/web/tests.py`)
- [x] Persist validated per-entry breaks and use them in projector screen construction
- [x] Browser tests for preview-modal first-break cadence, add/remove, persistence, reset, and live projector refresh (`tests/e2e/test_text_screen_breaks.py`)
- [x] Preview-modal controls and saved break actions
- [x] Verify song, Scripture, single-screen Text, and legacy row behavior remains intact
- [x] Fill traceability in `spec.md` with exact test and implementation paths
- [x] Update ITEM, board, VERSION, changelog, and release version in the same implementation PR
- [ ] Conventional commit and draft PR into `develop` with the repository PR template

## Done when

- [ ] All acceptance scenarios hold
- [ ] Targeted domain/app tests and E2E pass
- [ ] PR traceability and release records are complete
