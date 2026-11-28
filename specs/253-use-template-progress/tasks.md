# Tasks — spec 253

Ordered by user story: Setup, Foundational, US1, US2, Polish. `[P]` means order-independent, not
concurrent — one agent, one thread; the run records the order actually used. Every `Verified by: test`
row gets a failing test before its implementation, per TDD-01.

## Setup

- [X] T001 [P] [SETUP] Verify the Playwright E2E lane and create `tests/e2e/test_use_template_progress.py` with the template fixture
- [X] T002 [P] [SETUP] Add the leave-confirmation layer and its Stay/Leave actions to `multimedia/web/templates/reading/_generate_modal.html`

## Foundational

- [X] T003 [US1] Write a failing E2E test for `FR-001`/`US1-AC1`: settling a slot writes a record keyed by template id
- [X] T004 [US1] Implement `storageKey()` and `save()` call sites in `static/web/generate.js` so every slot/name/date/step change writes (FR-002, FR-003)
- [X] T005 [US1] Write a failing E2E test for `US1-AC4`: a fresh browser context has no progress

## US1 — progress survives a close

- [X] T006 [US1] Write a failing E2E test for `FR-004`/`US1-AC2`: reopening restores slots, step, name and date
- [X] T007 [US1] Implement `restore()` and wire it into `open()` without saving from `reset()` in `static/web/generate.js`
- [X] T008 [US1] Write a failing E2E test for `FR-005`: a slot removed from the template is ignored on restore
- [X] T009 [US1] Implement the version check and stale-slot filter in `restore()`
- [X] T010 [US1] Write a failing E2E test for `FR-002`: each of slot, choice, name, date and step change rewrites the record
- [X] T011 [US1] Write a failing E2E test for `FR-003`/`SC-002`: the record holds the slots, step, name and date, and a reload restores them
- [X] T012 [US1] Write a failing E2E test for `SC-001`/`US1-AC3`: two templates hold separate progress

## US2 — the close says the work is kept

- [X] T013 [US2] Write a failing E2E test for `FR-006`/`SC-003`/`SC-004`: Cancel, backdrop and Esc each show the leave confirmation, while a clean modal closes silently
- [X] T014 [US2] Implement `attemptClose()` and the `data-leave-stay` / `data-leave-accept` wiring in `static/web/generate.js`, keeping chooser and Create-confirm precedence
- [X] T015 [US2] Write a failing E2E test for `FR-007`/`US2-AC2–AC3`: Stay keeps the modal and rows, Leave closes without discarding
- [X] T016 [US2] Write a failing E2E test for `FR-008`/`SC-005`: a successful Create clears that template's record
- [X] T017 [US2] Remove the record on the successful Create response in `submit()`
- [X] T018 [US2] Write a failing E2E test for `FR-009`: the template is byte-identical after close and after Create

## Polish

- [X] T019 [P] [POLISH] Align the preview's confirm wording with the shipped markup and re-run `preview/probe.py`
- [ ] T020 [P] [POLISH] Run `tests.e2e.test_tatib_templates` and the new module together for regressions

## Delivery (from the repo's declared parts)

- [X] T021 [DELIVERY] Fold `reading/R65` into `docs/spec/reading.md`, append the `CHANGELOG.md` line and apply the declared `patch` at delivery
- [X] T022 [DELIVERY] Move `ITEM-270` to `In review` then `Done` in the same PR, with `Refs` to the anchor issue
