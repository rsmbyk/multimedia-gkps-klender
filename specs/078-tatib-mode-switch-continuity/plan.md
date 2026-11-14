# Plan 078: Preserve the open Tata Ibadah during list-mode switches

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-081
- **Bump:** patch

## Why

The dated/template toggle currently fetches a Tata Ibadah landing page without the open service ID. That response closes the service-entries sidebar and loses the first sidebar's selection even though the reading stage still shows the previously open Tata Ibadah.

## Scope / edges

**In:** switching the Tata Ibadah first sidebar between dated orders and templates while a Tata Ibadah page is open.

**Out:** main-rail menu changes, service entry content or order, and creation/editing of dated orders or templates.

## Approach

Keep the open service ID in mode navigation, preserve the second sidebar and stage during the list swap, and mark the exact open service row as current. If the open service belongs to the other list mode, include one contextual current-page row after the destination list, labeled with its actual date/template identity. Reveal that row in the first sidebar after layout settles. Clear only a first-sidebar filter that would hide it; keep the service-entry filter.

## TDD

- Domain/app tests: view-context tests in `multimedia/web/tests.py` for both mode directions and contextual row identity.
- E2E: `tests/e2e/test_reading.py` for open second sidebar, stage continuity, selected row, first-panel scroll, and filter edge cases.

## Risks

- The two list modes contain disjoint records. A contextual row must be clearly identified, use the actual service ID, and never appear twice.
- The sidebar scroll must not move the reading page.
