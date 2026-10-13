# Tasks 079: One Text entry with a selectable default screen mode

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Draft Spec 079 accepted by the project owner
- [x] Branch from current develop as feat/079-unified-text-screen-mode
- [x] Red — model and migration tests for existing Text modes, custom breaks, unchanged projector screens, and boundary validation in multimedia/tatib/tests.py
- [x] Green — add the default screen-mode field, migrate former Single-screen rows to Text, and route model validation through the field
- [x] Red — web tests for one Add Text action, Create mode selection, Edit preservation, Preview writes, confirmation outcomes, stale-state conflicts, and live projector data in multimedia/web/tests.py
- [x] Green — update forms, endpoints, Preview payload, projector grouping, and save notification
- [x] Red — browser acceptance in tests/e2e/test_unified_text_screen_mode.py for Create and Edit, both defaults, first custom break, non-clickable Custom state, confirmation/cancel, viewer state, and open projector refresh
- [x] Green — implement the Create switch, Preview footer switch, accessible confirmation, and responsive light/dark styling
- [x] Refactor — remove active use of the old Single-screen entry kind and duplicate Add action without changing song, Scripture, legacy, or old OBS behavior
- [ ] Verify targeted domain, web, and browser tests; let CI run the full required checks on the ready PR
- [ ] Fill final implementation traceability in spec.md
- [ ] Set ITEM-082 to In review with a draft PR, then Done with this spec and tasks in the same PR
- [ ] Bump VERSION from the current integration version, add the matching CHANGELOG section, and set ITEM-082 release_version in this PR
- [ ] Conventional Commit with the repository’s actual Codex coauthor trailer and a draft PR linking Spec 079

## Done when

- [ ] All Spec 079 acceptance scenarios hold for existing and newly created Text entries
- [ ] Targeted tests and required remote checks pass at the PR head
- [ ] Board, item, tasks, and version records are complete in the same PR
