# BL-003 — Wire web tatib calendar to month/year API filters

| Field | Value |
|-------|--------|
| **ID** | `BL-003` |
| **Status** | `ready` |
| **Priority** | `P1` |
| **Size** | `S` |
| **Area** | `web` |
| **Owner** | |

## Problem / why

`WEB-TATIB` documents an as-built quirk: the month calendar UI requests
`is_active=true&has_date=true` but does **not** send `month`/`year`, even though
`API-TATIB` supports those filters. Operators may think they are filtering by
month when they are not.

## Outcome

Calendar selection drives `month`/`year` (and documented behavior matches the
UI), or the UI is clarified if product chooses not to filter by month.

## Acceptance sketch

- WHEN a month is selected, THE list request SHALL include the corresponding
  `month`/`year` **or** the UI SHALL not imply month filtering (product choice).
- Update `WEB-TATIB` spec if behavior changes.
- TDD: Vitest and/or pytest as appropriate.

## Links

| Kind | Ref |
|------|-----|
| Spec | `WEB-TATIB-AC3`, `API-TATIB-AC3` |
| Notes | Honest quirk called out in web tatib plan/spec |

## History

| Date | Note |
|------|------|
| 2026-07-10 | Seeded from `WEB-TATIB` as-built notes |
