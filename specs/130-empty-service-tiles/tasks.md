# Tasks — An empty Tata Ibadah is centred, and its five kinds are tiles

## Phase 1: Setup

- [X] T001 Worktree and branch: `git worktree add ../multimedia-gkps-klender-130 -b fix/130-empty-service-stage develop`

## Phase 2: Foundational

- [X] T002 [P] Read the three renderers and the block's stylesheet — `templates/reading/tatib.html:187`,
      `static/web/offline-render.js:110`, `static/web/entries.js:100`,
      `static/styles/design/components.css:2168` — so the markup changes in step.

## Phase 3: US1 — centred empty service (P1)

- [X] T003 `tests/e2e/test_entries.py::test_an_empty_service_centres_a_row_of_square_icon_buttons`, asserting
      equal gaps above and below the block at 1440×900. *Written after the first implementation pass, as the
      owner asked for the change in a working session; it then drove the corrections in T005 and T007 rather
      than preceding the whole change.*
- [X] T004 `components.css`: `.read[data-kind="tatib"]:has(.entry__empty)` flex column with
      `min-height: 100%`; `.read__body:has(> .entry__empty)` `flex: 1` and centred; drop the header's bottom
      margin and the body's top margin in this state only (FR-001, FR-007).
- [X] T005 Re-measure at 1440×900, 1280×800, 1024×700 and 390×844 with
      `specs/130-empty-service-tiles/preview/probe_empty_stage.py`: the first pass measured 37.9px of bias
      from the two kept margins, the second 19px from the body's alone; both margins dropped, the gaps are
      now equal to 0.1px at all four sizes.

## Phase 4: US2 — square icon-only tiles in one row (P1)

- [X] T006 The same test asserts five tiles, one row, square, ≥44px, one glyph each, `title` and `.sr` name
      per tile. *Added with T003, after the first implementation pass.*
- [X] T007 `components.css`: `.entry__empty-actions` as a five-column grid, `.entry__empty-btn` square with
      `aspect-ratio: 1`, glyph capped at 60% of the tile; `@container (max-width: 300px)` for three and two
      (FR-002, FR-005). The first pass let `flex-wrap` produce 4 + 1 at 1280×800; the second shrank five tiles
      to 29.1px at 1024×700; the container query is what the measurement drove.
- [X] T008 `templates/reading/tatib.html`: the five buttons become glyph + `.sr` label + `title`; `Add Media`
      gains its frame-and-play glyph (FR-003, FR-004).

## Phase 5: US3 — the other two renderers (P2)

- [X] T009 `static/web/offline-render.js::emptyAddButtons()` builds the same markup, media glyph included.
- [X] T010 `static/web/entries.js::emptyAddButton()` builds the same markup for the post-delete rebuild.
- [X] T011 `tests/e2e/test_saved_render_parity.py`: five glyphs, and tiles compared by label, glyph count and
      square size rather than by absolute position; wait for the saved row before counting (FR-006).

## Phase 6: Polish

- [X] T012 `docs/spec/reading.md` folds the behaviour as R4.
- [X] T013 This slice's record: spec, plan, research, data-model, quickstart, contracts, checklist, analysis.
- [X] T014 Board card `ITEM-131`, `specs/README.md` index row, `CHANGELOG.md` entries, `VERSION` → `1.20.6`.
- [X] T015 Report: no push, no PR until the owner asks.
