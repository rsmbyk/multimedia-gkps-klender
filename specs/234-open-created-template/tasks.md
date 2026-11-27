# Tasks: a created Template opens on the reading stage

**Spec**: `specs/234-open-created-template/spec.md`
**Plan**: `specs/234-open-created-template/plan.md`
**Verification split**: 19 test · 2 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 Add a `_create_template_from_sidebar(page, name, start='/tatib/')` helper to
      `tests/e2e/test_editor.py` beside the spec 209 helper: open `start`, click `#panelAdd`,
      select `[data-tatib-kind="1"]`, wait for the date field to hide, fill the name and save.
      No assertion changes yet.

## Phase 2 — US1 (P1) 🎯 MVP

**Goal**: saving a Template lands on the saved template with no second click.
**Independent test**: from `/tatib/`, create `Skeleton`, read the URL, stage name and current row.

- [X] T002 [P] [US1] Rewrite the superseded `test_a_template_create_keeps_the_stage` in
      `tests/e2e/test_editor.py` as `test_a_created_template_opens_on_the_stage`: assert
      `location.pathname + location.search == '/tatib/<id>/?mode=template'`, `#readName` equals the
      saved name, and `#panelBody a.book[data-name="<id>"][aria-current="true"]` exists. Confirm it
      fails on the base code with the list URL.
- [X] T003 [P] [US1] Write a failing `test_an_empty_created_template_shows_its_add_actions`:
      after the same create the stage shows the empty-service invitation and the add actions a
      hand-opened empty template shows.

## Phase 3 — US2 (P1)

**Goal**: the template open carries the dated-create guarantees.
**Independent test**: mark the page, save a Template, compare marker, `timeOrigin`, `data-nav`,
`data-ch` and the focused row.

- [X] T004 [P] [US2] Write a failing `test_a_created_template_open_does_not_reload_the_document`:
      set `window.__gkps234 = 'alive'`, create, assert the marker survives, `performance.timeOrigin`
      is unchanged and `data-nav` keeps its value.
- [X] T005 [P] [US2] Write a failing `test_a_created_template_restores_focus_to_its_row`: assert
      the new row carries `aria-current="true"`, quiet focus lands on it with `row-flash`, and
      `data-name` is the new id.
- [X] T006 [P] [US2] Write a failing `test_a_created_template_opens_its_contents_pane`: assert
      `document.documentElement.dataset.ch === 'open'` after the create, as the spec 209 dated case
      does.

## Phase 4 — US3 (P2)

**Goal**: other creates and the template-list start are unchanged; the new start also opens.
**Independent test**: create from `/tatib/?mode=template`, then run the existing spec 209/215/167
create cases.

- [X] T007 [P] [US3] Write a failing
      `test_a_created_template_from_template_list_opens_on_the_stage`: start at
      `/tatib/?mode=template`, create, assert the same destination and `#tatibMode`
      `aria-pressed="true"`.
- [X] T008 [US3] Run the existing spec 209/215/167 cases from `tests/e2e/test_editor.py` and
      `tests/e2e/test_tatib_templates.py` — dated create, edit, refused create, failed create,
      generate from template and copy as template — and confirm each still lands where it did on
      the base commit; fix any regression caused by the widened condition.

## Phase 5 — Foundational implementation

**Goal**: one condition change makes the red tests green without touching other flows.

- [X] T009 In `static/web/reading.js`, change the `editor:saved` create branch to accept
      `record_kind === 0 || record_kind === 1`, choose `'/tatib/' + id + '/'` for a dated service
      and `'/tatib/' + id + '/?mode=template'` for a template, and keep the same `kind: 'service'`
      navigation and focus restore. This is the same edit already applied uncommitted for the live
      preview; make it the permanent slice change. Confirm T002–T007 turn green and T008 stays
      green.

## Phase 6 — Polish

- [X] T010 Re-check the next spec number, card ID, requirement number and patch version against
      `develop`, `origin/develop` and every unmerged local branch before delivery.
- [X] T011 At Fold, modify `reading/R46` in `docs/spec/reading.md` with the complete replacement
      block and mark the superseded Template clause; keep the edit and other-record clauses.

## Phase 7 — Convergence

<!-- written by Converge only; absent until it runs -->
