# Tasks 005: Sidebar editors for Kidung and Tata Ibadah

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`feat/005-sidebar-editors`, stacked on the 004 branch
      because the sidebars it edits only exist there)
- [x] Red — domain/app tests (`multimedia/web/tests.py`, `EditorViewTests`): create/update per
      record; the constraint matrix (duplicate short name, duplicate song number, hymn number
      required); CSRF; POST-only; the login hook; hymn exclusion in the shell markup
- [x] Green — forms + POST endpoints (`multimedia/web/reading/editors.py`, `views.py`,
      `urls.py`, `context_processors.py`)
- [x] Red — E2E (`tests/e2e/test_editor.py`): the three add flows, both edit flows, the
      hover-reveal with its keyboard reach, the error path, and the stage surviving a save
- [x] Green — modal + controls (`_editor_modal.html`, `_editor_form.html`, `components.css`,
      `editors.js`) and the `refresh` kind in `reading.js`
- [x] Update the mockup parity harness for the new named deviations (the add buttons push the
      exempted toolbar band to 120px)
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`minor`)
- [x] `VERSION` 0.8.0 → 0.9.0, changelog `## [0.9.0]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR**
- [x] Conventional Commit + draft PR linking `./spec.md`

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green (110 in the suite)
- [x] Board, tasks, and version are complete in this PR
- [x] The accepted-risk note and the `SIDEBAR_EDITORS_REQUIRE_LOGIN` hook are documented in
      the changelog
