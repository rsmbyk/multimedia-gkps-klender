# Tasks: Match the Tata Ibadah date header to the songbook header

**Spec**: `specs/123-tatib-date-header-parity/spec.md`
**Plan**: `specs/123-tatib-date-header-parity/plan.md`
**Verification split**: 11 test · 2 inspection · 0 manual

## Phase 1 — Setup

- [x] T001 [P] [US1] Add `test_tatib_date_header_matches_songbook_header` to `tests/e2e/test_reading.py`
      (`ReadingE2ETests`): open a song page and a dated service, read both eyebrows' computed `font-size`,
      `letter-spacing`, `line-height`, `font-weight`, `color`, and `opacity`; assert they are equal **and**
      equal the frozen tuple (16.5px, 1.98px, 27.225px, 600, `rgb(31, 31, 29)`, `0.78`). Red against today's
      11px / 0.88px date.
- [x] T002 [P] [US2] Add `test_tatib_date_header_reflows_at_a_narrow_stage` to the same module: at 1440,
      1280, and 390 widths assert the date's box equals its full rendered text width, the Project button's
      centre is within 1px of the date's whenever the row is a single line, and
      `documentElement.scrollWidth <= innerWidth`. Red today only on the equality it re-uses from T001; the
      overflow half is a guard.

## Phase 2 — Foundational

- [x] T003 `n/a — nothing is shared beyond Phase 1's pins`.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the service page's date reads exactly like the song page's songbook header.
**Independent test**: T001 alone — open both pages and compare the recorded styles.

- [x] T004 [US1] In `static/styles/design/components.css`, drop `font-size: 11px; letter-spacing: .08em`
      from `.read[data-kind="tatib"] .read__head-top .read__eyebrow`, keeping `white-space: nowrap`, so the
      date inherits `.read__eyebrow`. *(written as the preview build before gate 1; confirmed unchanged as
      the implementation after gate 2)*
- [x] T005 [US1] Re-run T001 green; confirm `.read__eyebrow` and the `margin-bottom: 0` rule are untouched.

## Phase 4 — US2 (P2)

**Goal**: a narrow stage loses neither the date nor the layout.
**Independent test**: T002 at 1280 (the stage that wraps in the preview).

- [x] T006 [US2] Move `flex-wrap: wrap` out of the `≤600px` block and onto
      `.read[data-kind="tatib"] .read__head-top` at every width, adding `row-gap: 8px`; keep the `≤600px`
      `.read__project { max-width: 100% }` rule.
- [x] T007 [US2] Re-run T002 green and the existing centring pin
      (`test_tatib_date_and_project_button_are_vertically_centered`) unchanged.

## Phase 5 — US3 (P3)

**Goal**: the saved copy carries the same header.
**Independent test**: read `static/web/offline-render.js` `servicePage()` (writes `#readEyebrow` inside the
shell) and re-run the offline eyebrow-text pins.

- [x] T008 [US3] Inspect the saved renderer and record that no JS change is needed; no edit expected.
- [x] T009 [US3] Re-run `tests/e2e/test_offline_library.py` eyebrow scenarios and
      `multimedia/web/tests.py::ReadingViewTests`.

## Phase N — Polish

- [x] T010 Write `backlog/items/ITEM-124-tatib-date-header-parity.md` and its `backlog/board.md` row.
- [x] T011 Bump `VERSION` 1.20.1 → 1.20.2 and add the `[Unreleased]` changelog entry.
- [x] T012 Tick this list, fill `analysis.md`'s dispositions, and open the draft PR.

## Phase N+1 — Convergence

- [x] T013 [Converge] Strengthen `test_tatib_date_header_reflows_at_a_narrow_stage` so it asserts the wrap
      rule itself — the Project action sits on its own line exactly when the date and the button cannot
      share the row — not just that nothing overflows. Recorded in `converge.md` pass 1.

## Verified

- `tests.e2e.test_reading.ReadingE2ETests`: the two new pins, plus the existing centring and
  populated-header pins — **4 tests, green** (38 with `multimedia.web.tests.ReadingViewTests`).
- `tests.e2e.test_offline_library.OfflineLibraryE2ETests.test_saved_dated_tatib_reading_keeps_its_date_header`
  — green.
- Red evidence before the CSS change: both new pins failed with `'11px' != '16.5px'` at 1440, 1280, and 390.
