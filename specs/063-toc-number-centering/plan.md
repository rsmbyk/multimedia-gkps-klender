# Plan 063: Center entry numbers vertically in the Tata Ibadah contents list

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-064
- **Bump:** patch

## Why

`.songrow` uses `align-items: baseline`, so the number cell lines up with the first
line of text. On multi-line contents rows — untitled text entries, two-line labels,
and songs with a verse line — the number hangs at the top instead of reading as the
row's index.

## Scope / edges

**In:** vertical position of `.songrow__c` in the Tata Ibadah contents list
(`:root[data-section="tatib"] #chList`) and in its drag copy (`.reorder__ghost`).

**Out:** the songbook song list, text alignment, row size, typography, colors,
grip position, section-break rows, and any markup or behavior change.

## Approach

1. Add an E2E that measures the number and row boxes for one-, two-, and
   three-line contents rows and expects their vertical centers to match.
2. Add `align-self: center` to `.songrow__c` scoped to the Tata Ibadah contents
   list and the reorder ghost, next to the existing tatib `.songrow__t` rule.
3. Assert the text box position is unchanged and the songbook list still uses
   baseline alignment.

## TDD

- Domain/app tests: N/A; CSS-only change.
- E2E: new `tests/e2e/test_toc_number_centering.py`, class `TocNumberCenteringE2ETests`
  (Playwright via `StaticLiveServerTestCase`).
- Targeted local command: `DJANGO_DEVELOPMENT_MODE=True python manage.py test
  tests.e2e.test_toc_number_centering --noinput -v 1`. Full suite runs in CI.

## Risks

- The drag copy lives outside `#chList`; without its own selector the number would
  jump to the top while dragging.
- A rule on bare `.songrow__c` would also move numbers in the songbook list.
