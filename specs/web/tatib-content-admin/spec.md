# Spec: WEB-TATIB — Tatib content admin (web)

| Field | Value |
|-------|--------|
| **Spec ID** | `WEB-TATIB` |
| **Area** | `web` |
| **Status** | `as-built` |
| **Folder** | `specs/web/tatib-content-admin/` |

## Problem / goal

Editors manage tata ibadah lists and ordered items (TEXT / END_OF_SECTION) in
the browser, including insert-after, reorder, and preview.

## User stories

- **WEB-TATIB-US1:** As a content editor, I want to list and open tatibs, so
  that I can prepare a service order.
- **WEB-TATIB-US2:** As a content editor, I want to add TEXT and EOS items,
  insert after a row, and reorder, so that the sequence matches the liturgy.
- **WEB-TATIB-US3:** As a content editor, I want item preview, so that I can
  check titles/text before service.

## Acceptance criteria (EARS)

### Pages and access

- **WEB-TATIB-AC1:** THE system SHALL serve `/tatib/tatibs` and
  `/tatib/tatibs/<id>` (redirect `/tatib/` → tatibs).
- **WEB-TATIB-AC2:** THE tatib content-admin pages SHALL be reachable without
  login (`API-ACCESS`).

### List filters (as-built UI)

- **WEB-TATIB-AC3:** WHEN the list page loads with the month calendar selected,
  THE UI SHALL request
  `GET /api/tatib/tatibs?is_active=true&has_date=true` (and SHALL NOT be
  required to send `month`/`year` even if a calendar is shown).
- **WEB-TATIB-AC4:** WHEN the operator toggles “General”, THE UI SHALL request
  tatibs with `has_date=false` (undated).
- **WEB-TATIB-AC5:** WHEN creating/editing a tatib, THE UI SHALL POST/PATCH
  `/api/tatib/tatibs` with optional date formatted `YYYY-M-D` when set.

### Items

- **WEB-TATIB-AC6:** WHEN opening a tatib, THE UI SHALL load the tatib and
  `GET /api/tatib/items?tatib=<id>&ordering=order_number`.
- **WEB-TATIB-AC7:** WHEN adding TEXT or EOS, THE UI SHALL POST
  `/api/tatib/items` with `item_type` `0` or `1`.
- **WEB-TATIB-AC8:** WHEN inserting after a row, THE UI SHALL pass
  `insert_after` set to that item’s `order_number`.
- **WEB-TATIB-AC9:** WHEN saving reorder mode, THE UI SHALL POST
  `/api/tatib/items/reorder` with 1-based `order_number`s; Discard SHALL reset
  local order without saving.
- **WEB-TATIB-AC10:** THE UI SHALL preview TEXT as title+text and show EOS as
  `--- END OF SECTION ---`.

## Out of scope

- API `insert_after` shift rules themselves (`API-TATIB`).
- OBS Tatib dock (`OBS-TATIB`).

## Constraints

- Honest as-built: month calendar UI does not currently send `month`/`year`.
- Related: `API-TATIB`, `API-ACCESS`, `WEB-SONGS`.

## Notes

- Vitest: `api-paths.test.js`, `…/tatib/items/reorder.test.js`.
