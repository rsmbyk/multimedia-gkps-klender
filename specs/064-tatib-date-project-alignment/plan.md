# Plan 064: Center the Tata Ibadah date and Project button

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-067
- **Bump:** patch

## Why

On the Tata Ibadah page, the date label and Project button share a header row, but the date label's bottom margin makes the pair look vertically misaligned. Align the date label and button cleanly while retaining the existing title and button design.

## Scope / edges

**In:**

- Vertically center the Tata Ibadah date label with the Project button in the existing header row.
- Verify the alignment at desktop and narrow viewport widths.

**Out:**

- Moving the Project button or changing its appearance, behavior, or position in the row.
- Changing the service title, non-Tata Ibadah headers, or other page layout.

## Approach

- Remove the date label's bottom margin only for the Tata Ibadah reader; keep the header row's existing centered flex alignment and spacing.
- Keep the date left, the Project button right, and the service title on its separate row below.
- Match the preview approved in this task conversation on 2026-10-12.

## TDD

- Domain/app tests: N/A; presentation-only CSS.
- E2E (Playwright, Python): assert the date label and Project button vertical centers match within 1 px at 1440 px and 390 px viewport widths.

## Risks

- The shared date-label style is used on other reading pages; scope the margin adjustment to the Tata Ibadah reader only.
