# Feature Specification: the old bookmarks stand as services

**Slice**: `specs/188-legacy-bookmarks-to-services`
**Branch**: `feat/188-legacy-bookmarks-to-services`
**Created**: 2026-11-05
**Status**: Draft
**Bump**: minor
**Input**: *"i want the old bookmarks to be converted as the new services in a migration. use entry of
kind songs to create the service. the old bookmark data still be preserved for the old dock to work."* —
the owner's selection rule, asked and answered at the start of the slice: *only active bookmarks that
are dated and hold at least one song*.

## What exists today

Two records describe the same thing. A **bookmark** (`bookmarks.SongBookmark` with ordered
`SongBookmarkItem` rows) is a dated list of songs and the verse numbers to sing; the legacy OBS dock
(`/obs/songs/…`, `multimedia/obs/`) reads it from the REST API. A **service** (`tatib.TataIbadah` with
`ServiceEntry` rows) is the same idea in the newer model, read by the reading pane, the operator dock
and the projector.

The database the team actually runs holds 360 bookmarks back to 2022 — 157 of them active, dated and
carrying songs, and 3134 items in all. None of them reach any of the new surfaces: the dock's service
list only draws `TataIbadah` rows.

## User Scenarios & Testing

### US1 — the team's past services are in the dock (P1)

**Why this priority**: the old dock is the only place the historical song sets can be reached; every
one of them has to be openable from the new dock and the reading pane, with the same songs in the same
order and the same verses.

**Independent Test**: after the migration, the operator dock lists a 2026-10-11 service carrying the
nine songs its bookmark held, and opening it shows those verses.

**Acceptance scenarios**

1. **Given** an active bookmark dated 2026-10-11 with nine items, **When** the migration has run,
   **Then** a dated service of that name exists carrying nine song entries in the bookmark's order,
   each with the same verse numbers.
2. **Given** a bookmark that was deleted, has no date, or holds no songs, **When** the migration has
   run, **Then** no service was created for it.
3. **Given** a service already standing under the same name and date, **When** the migration runs,
   **Then** the bookmark still becomes its own service beside it, carrying that same name and date.
4. **Given** a service already under that name and date, empty or filled by the team, **When** the
   migration runs, **Then** it is left exactly as it was — not read, not reused, not renamed.
5. **Given** any bookmark, **When** the migration has run, **Then** the bookmark and its items are
   byte-for-byte as they were, so the legacy dock still lists, opens and restores them.

### Edge Cases

- **When** a bookmark's order numbers hold gaps (rows deleted over the years) **Then** the service is
  numbered from one in the bookmark's own order.
- **When** a bookmark's verse string holds parts that are not numbers **Then** those parts are dropped
  and the rest are kept as integers.
- **When** two services end up carrying the same name and date **Then** both are listed; the migration
  never merges, renames or hides either of them.
- **When** the migration is run a second time **Then** it converts again — there is no exists-guard, by
  the owner's rule, so a second run is a deliberate duplicate rather than a no-op.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The migration SHALL create one dated service, of kind song entry, for every bookmark that is active, dated, and holds at least one item. | `new: reading` |
| FR-002 | It SHALL NOT create a service for a bookmark that is inactive, undated, or holds no items. | `new: reading` |
| FR-003 | A service already standing under the same name and date SHALL NOT stop the conversion: the bookmark SHALL become its own service beside it, keeping that name and date, and the standing service SHALL NOT be read or written. The comparison is case-sensitive. | `new: reading` |
| FR-004 | The migration SHALL NOT write to `SongBookmark` or `SongBookmarkItem`. | `new: reading` |

### Key Entities

- **SongBookmark / SongBookmarkItem** — read only. `name` (≤32), `date` (nullable), `is_active`;
  items hold `song`, `verse` (comma-separated integers) and `order_number`.
- **TataIbadah** — written. `name` copied, `kind` = service, `date` copied, `is_active` = true. The
  type constraint in `tatib/0012` requires a date for a service, which is why undated bookmarks
  cannot convert.
- **ServiceEntry** — written. `kind` = song, `song` copied, `verses` parsed from the item's `verse`,
  `order_number` renumbered from one.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Every qualifying bookmark is reachable as a service | 157 services carry the name and date of the 157 qualifying bookmarks in the local copy |
| SC-002 | No song is lost or invented | every qualifying bookmark's item count equals the entry count of a service under its name and date (0 mismatches), and a sampled service's verses equal its bookmark's |
| SC-003 | The old dock is unharmed | 360 bookmarks and 3134 items unchanged after the migration |
| SC-004 | An existing service never blocks a conversion | 157 services created beside 138 existing ones; 18 name and date pairs carry two services, and the 61 existing entries are untouched |

## UI/UX

`n/a — data only.` The migration draws nothing; the services it creates appear in the service lists the
reading pane and the operator dock already render, and in the projector, with no new markup, style or
state.

## Assumptions

- **Selection**: active, dated, with at least one item (the owner's answer). Deleted bookmarks stay
  deleted, undated ones cannot satisfy the service/date constraint, empty ones carry nothing.
- **Duplicate name and date**: allowed and deliberate (the owner's rule). A service already under the
  same name and date is left alone and the bookmark gets a service of its own beside it; the name
  comparison is case-sensitive.
- **Name**: copied verbatim, placeholders (`_`) included. The migration never invents or tidies a name.
- **Order**: the bookmark's item order, renumbered from one.
- **Undated bookmarks** stay bookmark-only. They are rehearsal sets (`Doding Galangan`,
  `Lagu Doa Persembahan`), not services, and the legacy dock keeps them.
- **Reverse**: none. The bookmarks remain the source of truth and a reverse would have to guess which
  of two identical services it created; the migration is forward-only.
- **No marker column**: two services may share a name and date, so no pair identifies a conversion —
  and this slice adds no link back to the legacy app it is retiring.

## Revision

- **2026-11-05 — the same-name-and-date rule was retracted before delivery.** The first implementation
  reused an empty service under the same name and date and skipped a filled one, and that is what the
  first copy-of-the-database check measured (139 created, 18 filled). The owner replaced it: a service
  already standing under the same name (case-sensitive) and date must not stop the conversion — a
  second service of that name and date is created. FR-003, SC-004, the edge cases and the migration
  now say so, the reuse guard is gone, and the second run is no longer a no-op.
