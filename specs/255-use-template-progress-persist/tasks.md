# Tasks — spec 255

Ordered by user story: Setup, Foundational, US1, US2, Polish, Delivery. `[P]` means order-independent,
not concurrent. Every `Verified by: test` row gets a failing test before its implementation.

## Setup

- [X] T001 [P] [SETUP] Create `tests/e2e/test_use_template_progress_persist.py` from the spec 253 fixture lane
- [X] T002 [P] [SETUP] Add `data-generate-tatib="{{ service_id }}"` and the `.read__draft-dot` span to the `[data-generate-open]` button in `reading/tatib.html`

## Foundational

- [X] T003 [US1] Write a failing E2E for `FR-001`: the record is in `localStorage`, `v: 2`, with `savedAt`
- [X] T004 [US1] Move `save`/`saved`/`clearSaved` in `static/web/generate.js` from `sessionStorage` to `localStorage` and write `savedAt`
- [X] T005 [US1] Write a failing E2E for `FR-003`/`SC-002`: a record 168 h + 1 s old is ignored and removed
- [X] T006 [US1] Implement `liveRecord()` and `pruneExpired()` with the 168 h rule

## US1 — persists for seven days

- [X] T007 [US1] Write a failing E2E for `SC-001`: a new browser context restores progress
- [X] T008 [US1] Write a failing E2E for `SC-003`: a six-day-old record plus an edit restarts the clock
- [X] T009 [US1] Write a failing E2E for `FR-002`: every slot/choice/name/date/step change rewrites `savedAt`
- [X] T010 [US1] Write a failing E2E for `FR-004`: reopening restores slots, step, name and date
- [X] T011 [US1] Write a failing E2E for `US1/AC4`: two templates keep separate clocks and records

## US2 — the button says a draft is saved

- [X] T012 [US2] Write a failing E2E for `FR-006`/`SC-004`: a live draft marks the button; none does not
- [X] T013 [US2] Implement `paintMark()` and paint it at load, on `shell:page`, after `save()` and after `clearSaved()`
- [X] T014 [US2] Add the dot's CSS in `static/styles/design/components.css` (7 × 7, inset 3px, `--active-ink`)
- [X] T015 [US2] Write a failing E2E for `FR-006`: the dot is 7 × 7 at the 4px border-box inset and the button does not reflow
- [X] T016 [US2] Write a failing E2E for `FR-007`/`SC-006`: the accessible name states the saved draft, and is absent without a draft
- [X] T017 [US2] Write a failing E2E for `FR-008`/`SC-005`: the mark appears on the first save and is gone after Create
- [X] T023 [US2] Write a failing E2E for `FR-011`: the leave confirmation says "seven days", never "browser session"

## Polish

- [X] T018 [P] [POLISH] Write a failing E2E for `FR-010`: a storage that throws still opens and operates the modal
- [X] T019 [P] [POLISH] Write a failing E2E for `FR-009`: the template is byte-identical after Create
- [X] T020 [P] [POLISH] Re-run the spec 253 and template E2E modules for regressions

## Delivery (from the repo's declared parts)

- [ ] T021 [DELIVERY] Fold `reading/R67` into `docs/spec/reading.md`, add the `CHANGELOG.md` line and apply the declared `patch`
- [ ] T022 [DELIVERY] Move `ITEM-276` to `In review` then `Done` in the same PR, with `Refs` to its anchor issue