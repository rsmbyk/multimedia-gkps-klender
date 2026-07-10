# Spec: OBS-TATIB — OBS Tatib dock and source

| Field | Value |
|-------|--------|
| **Spec ID** | `OBS-TATIB` |
| **Area** | `tatib` |
| **Status** | `as-built` |
| **Folder** | `specs/tatib/obs-tatib-live/` |

## Problem / goal

Operators select a tata ibadah in an OBS dock, step through TEXT and
END_OF_SECTION items, paste quick text, and project the active item on an OBS
source.

## User stories

- **OBS-TATIB-US1:** As an OBS operator, I want to activate a tatib and step
  items, so that the liturgy order is projected live.
- **OBS-TATIB-US2:** As an operator, I want TEXT vs END_OF_SECTION handled
  distinctly, so that section breaks clear the projection appropriately.
- **OBS-TATIB-US3:** As a projectionist, I want the source to follow item and
  status posts, so that the screen stays in sync.

## Acceptance criteria (EARS)

### Surfaces and channels

- **OBS-TATIB-AC1:** THE system SHALL serve `/obs/tatib/dock` and
  `/obs/tatib/source`.
- **OBS-TATIB-AC2:** THE tatib app SHALL use BroadcastChannels
  `OBS-TATIB-TATIB-ITEM`, `OBS-TATIB-STATUS`, and `OBS-TATIB-CONTROL`.
- **OBS-TATIB-AC3:** WHEN the dock gains/loses focus, THE focus indicator SHALL
  use the tatib colour class (`red`).

### List / activate

- **OBS-TATIB-AC4:** THE Tata Ibadah tab SHALL support month calendar vs
  general (`date === null`) filtering patterns for choosing a tatib.
- **OBS-TATIB-AC5:** WHEN Activate runs, THE dock SHALL load the tatib and items
  ordered by `order_number` from the API.
- **OBS-TATIB-AC6:** THE OBS dock SHALL NOT provide item reorder UI; order
  comes from the API (reorder lives in `WEB-TATIB`).
- **OBS-TATIB-AC7:** Detail modal SHALL be a read-only list showing title or
  `--- END OF SECTION ---`.

### TEXT vs END_OF_SECTION

- **OBS-TATIB-AC8:** `item_type === 0` SHALL be TEXT (show `title`);
  `item_type === 1` SHALL be END OF SECTION (label `--- END OF SECTION ---`).
- **OBS-TATIB-AC9:** WHEN items load, Display SHALL append a synthetic end
  marker `{ item_type: 0, text: '--- END ---' }`.
- **OBS-TATIB-AC10:** IF the active item is `item_type === 1` OR the last
  index, THEN status SHALL go inactive and activate SHALL be refused.
- **OBS-TATIB-AC11:** WHEN posting WHILE active: IF end-of-section or last
  index, THE dock SHALL post empty title/text (as-built may double-post current
  then empty).
- **OBS-TATIB-AC12:** WHEN on end-of-section AND the next item is TEXT and not
  near absolute end, THE UI SHALL show Next+Activate; else normal Next.

### Hotkeys, paste, source, settings

- **OBS-TATIB-AC13:** WHILE `tab-display`, Left → prev; Right → Next+Activate
  if visible else Next; Space → status.
- **OBS-TATIB-AC14:** WHEN paste provides non-empty text, THE dock SHALL
  deactivate then activate a `$QUICK_PASTE$` single TEXT item; reopen SHALL
  prefill if that quick paste is active.
- **OBS-TATIB-AC15:** WHEN the source loads, it SHALL post inactive status with
  `source: 'source'`.
- **OBS-TATIB-AC16:** WHEN item/status arrive, THE source SHALL update
  title/text and fade the segment.
- **OBS-TATIB-AC17:** Shared settings SHALL use prefix `OBS_TATIB`.

## Out of scope

- Web reorder / insert_after UX (`WEB-TATIB`, `API-TATIB`).
- Project combined view (`OBS-PROJECT`).

## Constraints

- Related: `API-TATIB`, `WEB-TATIB`, `OBS-PROJECT`, `API-ACCESS`.

## Notes

- Vitest: `tatib/common/bc.test.js`, `display/hotkeys.test.js`,
  `tatib-storage.test.js`.
