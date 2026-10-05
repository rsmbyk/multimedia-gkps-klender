# Tasks 005: Sidebar editors for Kidung and Tata Ibadah

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`feat/005-sidebar-editors`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): create/update per record; the
      constraint matrix (duplicate short name, duplicate song number, hymn number required);
      CSRF; the login hook; hymn exclusion in the shell markup
- [ ] Green — forms + POST endpoints (`multimedia/web/reading/editors.py`, `views.py`, `urls.py`)
- [ ] Red — E2E (`tests/e2e/test_editor.py`): the three add flows, an edit flow, hover/focus
      reveal, the error path, the stage surviving a save
- [ ] Green — modal + controls (`_editor_modal.html`, `components.css`, `editors.js`) and the
      `shell:applied` event in `reading.js`
- [ ] Update the mockup parity harness for the new named deviations (add button, row controls)
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump` on the ITEM and spec header (`minor`)
- [ ] `VERSION` 0.8.0 → 0.9.0, changelog `## [0.9.0]`, and `release_version` in **this PR**
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR**
- [ ] Conventional Commit + draft PR linking `./spec.md`

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version are complete in this PR
- [ ] The accepted-risk note and the `SIDEBAR_EDITORS_REQUIRE_LOGIN` hook are still accurate
      and documented in the changelog
