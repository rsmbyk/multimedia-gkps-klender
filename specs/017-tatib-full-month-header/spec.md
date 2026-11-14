# Spec 017: Show a full month name in the Tata Ibadah date header

- **ID:** 017
- **Status:** Accepted (owner, 2026-10-07)
- **Item:** ITEM-019
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Use the full Indonesian month name in the date eyebrow above a dated Tata Ibadah page title.

## Scope

### In scope

- Format a dated service's page header with the numeric day, full Indonesian month name, and year.

### Out of scope

- Date formats in sidebars, search results, forms, APIs, or other pages.
- Undated service labels or projection button styles.

## Domain rules

- The date eyebrow above the Tata Ibadah title uses a full Indonesian month name; for example, 23 August 2026 is `23 Agustus 2026`.
- An undated service keeps its current `Tata Ibadah` label.

## Acceptance scenarios

### Scenario: Show a full month name for a dated service

- **Given** a Tata Ibadah dated 23 August 2026
- **When** I open its reading page
- **Then** the date eyebrow above the title reads `23 Agustus 2026`

### Scenario: Preserve the undated label

- **Given** an undated Tata Ibadah template
- **When** I open its page
- **Then** its eyebrow remains `Tata Ibadah`

## Traceability

- E2E: `tests/e2e/test_reading.py` (`ReadingE2ETests`).
- Implementation: `multimedia/web/reading/views.py` and the date-format helper in `multimedia/web/reading/search.py` if reused/extended.
