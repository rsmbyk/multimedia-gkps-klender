# Feature Specification: entity versions and safe concurrent edits

**Slice**: `specs/254-entity-versioning`
**Branch**: `feat/254-entity-versioning`
**Created**: 2026-11-28
**Status**: Accepted
**Input**: The owner's request for entity-level version numbers on services, service entries, songs, songbooks and song verses, plus a deletion guard when a verse is in use; the live-surface behaviours belong to later slices.

## User Scenarios & Testing

### US1 — Every tracked object carries a version (P1)

**Why this priority**: Without a stored version there is nothing for a second editor to compare against, so every other rule in this slice has no foundation.
**Independent Test**: A fresh row of each of the six tracked models reads version 1; a stored row that changes reads version 2.

**Acceptance scenarios**

1. **Given** a new service, template, service entry, legacy item, songbook, song or verse **When** it is created **Then** its version is 1.
2. **Given** existing rows created before this slice **When** the migration completes **Then** each carries version 1 and no field besides the new column changes.
3. **Given** a tracked row **When** a write changes a stored value **Then** its version increases by exactly one.

### US2 — A no-op save leaves the version alone (P1)

**Why this priority**: The owner ruled that merely opening and saving a form is not a change; treating it as one would invalidate every other open page for no reason.
**Independent Test**: Saving a form whose values are identical to the stored ones leaves both the values and the version unchanged.

**Acceptance scenarios**

1. **Given** a service at version 5 **When** its edit form is saved with identical values **Then** it remains at version 5.
2. **Given** a song at version 3 **When** its title is saved unchanged **Then** it remains at version 3.
3. **Given** a verse order that is already in the requested order **When** reorder is posted **Then** the verse version is unchanged.

### US3 — A stale write is rejected (P1)

**Why this priority**: This is the race-condition guard: two editors who opened the same row at version 5 must not both succeed when the first write makes it version 6.
**Independent Test**: Two POSTs carrying version 5 against one row yield one 200 and one 409; the 409 leaves the row untouched.

**Acceptance scenarios**

1. **Given** a row at version 5 **When** a write carries expected version 5 **Then** the write is applied and the row becomes version 6.
2. **Given** a row at version 6 **When** a write carries expected version 5 **Then** the server answers 409 and writes nothing.
3. **Given** two concurrent writes that both carry version 5 **When** they are processed **Then** the version check and the write happen under one row lock, so only one wins.

### US4 — Service changes include their children (P1)

**Why this priority**: An operator watching a service needs that service's version to move when anything it displays changes, not only when its own fields change.
**Independent Test**: Editing, adding, deleting or reordering an entry inside a service increments that service's version.

**Acceptance scenarios**

1. **Given** a service at version 5 **When** an entry inside it is edited **Then** the service becomes version 6.
2. **Given** a service at version 5 **When** an entry is added, deleted or reordered **Then** the service becomes version 6.
3. **Given** a service at version 5 **When** a legacy text/note item inside it is saved, deleted or reordered **Then** the service becomes version 6.
4. **Given** a service at version 5 **When** a new entry is created inside it while the client carries the old service version **Then** the create is refused with 409.

### US5 — Song-side changes reach every service that uses the song (P1)

**Why this priority**: The owner ruled that any change to a song or its verses invalidates every service that projects it, including templates.
**Independent Test**: Changing a song title or a verse lyric bumps every dated service and template whose song entry names a verse of that song.

**Acceptance scenarios**

1. **Given** two services and a template that name verses of one song **When** the song's title changes **Then** all three versions increase by one.
2. **Given** a song whose verse lyric is edited **When** the save succeeds **Then** its own version increases and every referencing service's version increases.
3. **Given** the same verse order is posted again with no change **When** the request is processed **Then** no version increases anywhere.

### US6 — A referenced verse, song or songbook cannot be deleted (P1)

**Why this priority**: Deleting a target that a service still names leaves the service pointing at a retired record; the owner wants that prevented at the source.
**Independent Test**: A delete request for a song whose verse is named by a service entry is refused; one with no such reference succeeds.

**Acceptance scenarios**

1. **Given** a verse named by one song-kind service entry **When** verse delete is requested **Then** it is refused and the verse stays live.
2. **Given** a song with a live verse named by a service entry **When** song delete is requested **Then** it is refused and the song stays live.
3. **Given** a songbook containing such a song **When** songbook delete is requested **Then** it is refused and the book stays live.
4. **Given** no service names a live verse of the song or book **When** delete is requested **Then** the existing soft-delete behaviour proceeds.

### US7 — The refusal names how many Tata Ibadah are affected (P1)

**Why this priority**: The operator needs to know why Delete is unavailable, not just that it is.
**Independent Test**: The notice reads `Used in <count> Tata Ibadah — delete unavailable`, where `<count>` is the number of distinct Tata Ibadah records — dated services and templates — that name a live verse of the target.

**Acceptance scenarios**

1. **Given** one service with two entries naming two verses of one song **When** the song's delete confirmation opens **Then** the count reads 1.
2. **Given** a dated service and a template that both name the song **When** the songbook's delete confirmation opens **Then** the count reads 2.
3. **Given** a referenced verse **When** its edit modal opens **Then** it shows the same wording and its Delete is disabled with the note as `aria-describedby`.
4. **Given** an unreferenced song **When** its delete confirmation opens **Then** no notice appears and Delete works.

### US8 — The notice is present where the delete is offered (P2)

**Why this priority**: The server refusal alone would leave a confirmation dialog with a working-looking Delete button.
**Independent Test**: Opening the delete confirmation for a referenced song or songbook shows the notice and a disabled Delete; the verse modal keeps its existing note.

**Acceptance scenarios**

1. **Given** a referenced song **When** its sidebar delete control is clicked **Then** the confirmation shows the notice and its Delete is disabled.
2. **Given** a referenced songbook **When** its sidebar delete control is clicked **Then** the confirmation shows the notice and its Delete is disabled.
3. **Given** a referenced verse **When** its edit modal opens **Then** the existing note is unchanged in position and wording apart from the count's meaning.

### Edge Cases

- **When** a write carries no expected version **Then** it is refused rather than silently treated as current — every writer must name the version it opened.
- **When** a template is the only user of a song **Then** it still counts and still blocks deletion.
- **When** a legacy `TataIbadahItem` is the only changed row **Then** the owning service version still advances.
- **When** a song reference comes from a template's fill-in or choice option **Then** the option's own entry count is used for the distinct-service count.
- **When** a soft-deleted row is edited through an administrative path **Then** the same version rules apply.
- **When** a version would overflow its integer field **Then** the write is refused; no wrapping is permitted.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | `TataIbadah`, `TataIbadahItem`, `ServiceEntry`, `Book`, `Song` and `Verse` SHALL each carry an integer `version` starting at 1. | `versioning/R1` |
| FR-002 | A successful write that changes a stored field SHALL increase that row's version by exactly one; a write with identical values SHALL NOT increase it. | `versioning/R2` |
| FR-003 | Every write to an existing tracked row SHALL carry the version the writer opened; a mismatch SHALL return HTTP 409 and write nothing. | `versioning/R3` |
| FR-004 | The version comparison and the write SHALL be performed under a row lock inside one transaction. | `versioning/R4` |
| FR-005 | Creating a new tracked row SHALL NOT require an expected version for the new row, but a create inside a service SHALL check the parent service's version. | `versioning/R5` |
| FR-006 | A service's version SHALL increase when its own fields change, when an entry or legacy item inside it is created, edited, deleted or reordered, and when any referenced song or verse changes. | `reading/R64` |
| FR-007 | A song or verse change SHALL increase the version of every dated service and template whose song entry names a live verse of that song. | `versioning/R6` |
| FR-008 | A referenced verse SHALL NOT be deletable; this refusal stays authoritative at the server. | `reading/R40` |
| FR-009 | A songbook SHALL NOT be soft-deleted when any of its songs has a live verse named by a song-kind service entry. | `reading/R65` |
| FR-010 | A song SHALL NOT be soft-deleted when any of its live verses is named by a song-kind service entry. | `reading/R65` |
| FR-011 | The notice for all three refusals SHALL read `Used in <count> Tata Ibadah — delete unavailable`, where `<count>` is the number of **distinct** Tata Ibadah records, including templates, that name a live verse of the target. | `reading/R66` |
| FR-012 | The song and songbook delete confirmation dialogs SHALL show the notice and disable their Delete when the count is greater than zero; the verse edit modal SHALL keep its existing note and disabled Delete. | `reading/R66` |
| FR-013 | The conflict response body SHALL carry a stable machine-readable error and a human-readable message; presentation of that response is out of scope for this slice. | `versioning/R7` |
| FR-014 | Existing rows SHALL be migrated to version 1 without changing any other stored value. | `versioning/R1` |
| FR-015 | Every write path that touches a tracked row SHALL use the same version rule, including the legacy item endpoints and the service template generate/copy paths. | `versioning/R3` |

### Key Entities

- **Tracked object** — any `TataIbadah`, `TataIbadahItem`, `ServiceEntry`, `Book`, `Song` or `Verse` row, identified by its existing primary key and carrying an integer `version`.
- **Expected version** — the version a client read when it opened the object, supplied with every write to that object.
- **Referencing service** — a distinct `TataIbadah` record, dated service or template, that has a song-kind `ServiceEntry` whose `verses` list names a live verse of the target.
- **Delete refusal notice** — the presentation of a non-zero referencing-service count beside a disabled Delete action.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A stale write never changes a stored row | One 200 and one 409 for two version-5 writes; the row equals its pre-409 state |
| SC-002 | No-op saves do not invalidate other editors | Identical-value save leaves the version byte-identical |
| SC-003 | Service versions reflect every covered child change | One increment per accepted entry, legacy item, song or verse change |
| SC-004 | The refusal count is distinct services, not entries | A service with two qualifying entries counts once; a template counts too |
| SC-005 | Deletion of a referenced verse, song or songbook is impossible through the product endpoints | Each delete attempt returns a refusal and the row stays live |
| SC-006 | All six models carry versions after migration | Migration test reads every model's version as 1 |

## UI/UX

Static preview: `specs/254-entity-versioning/preview/index.html` (states and measurements in `preview/README.md`).

- **Layout / position**: at 1440×900 the delete confirmation is 560×157 at (440, 372); the verse modal is the product's 840×760 frame at (300, 70). The note is the first child of `.editor__actions` and is the disabled Delete's `aria-describedby`.
- **Size / spacing**: note `12px / 18px`, one line 265×18 in both frames; action buttons 38px high. At 520px the song notice still wraps; 540px fits the song but not the songbook.
- **Colour / typography**: note `rgb(100, 99, 87)` in light and `rgb(156, 154, 145)` in dark — the existing `--head-ink` token; no new tint or border.
- **States**: referenced song/songbook (note + disabled Delete), referenced verse (existing note + disabled Delete), unreferenced control (no note, enabled Delete), light · dark.
- **Motion**: none; the existing dialog opening behaviour is unchanged.
- **Responsive**: the confirmation is `min(560px, calc(100vw - 32px))`, so it narrows below 560px and the existing `@media (max-width: 650px)` rule gives the note its own row; the verse frame stays 840×760.
- **Candidate rule**: delete confirmations use `min(560px, calc(100vw - 32px))` — the minimum width at which both notices stay on one line with the default buttons.

## Assumptions

- Existing rows receive version 1 at migration — no stored history exists to derive a higher number.
- "Tata Ibadah" in the notice includes both dated services and templates — the owner confirmed both are counted.
- Any change to a song or its verses bumps referencing services — this supersedes the earlier "only reordering" scope, which the owner retracted.
- No-op saves are detected by comparing stored values to submitted values before writing — the owner ruled that identical saves are not changes.
- The 409 conflict response is server-side only here; page invalidation and the notification badge are ITEM-272.
- Anonymous editors remain subject to the version check — public writes are a standing product decision, not a bypass.
- The notice keeps the existing wording and glyph from the verse modal; only the count's meaning changes.

## Clarifications

### Session 2026-11-28

- Q: Which block should be defined first? → A: Song-entry deletion states, later replaced by the deletion guard when the owner withdrew cases 1–4.
- Q: Should deleted verse IDs stay checked in the song entry edit modal? → A: No; the owner withdrew cases 1–4 entirely, so this rule does not ship.
- Q: Where should the deletion notice appear? → A: In the delete confirmation dialog for songs and songbooks; the verse edit modal keeps its note.
- Q: What does the count mean? → A: Distinct Tata Ibadah records, for verse, song and songbook notices alike. The earlier entry-count behaviour in `reading/R40` is modified by this slice.
- Q: Do templates count? → A: Yes, dated services and templates both count.
- Q: Which song-side changes bump referencing services? → A: Any change to a song or its verses. The earlier "only reordering" answer was retracted by the owner.
- Q: Does a no-op save bump the version? → A: No.
- Q: Which objects get versions? → A: The five named by the owner plus the legacy `TataIbadahItem`, because it is still editable and renders in a service.
- Q: How should the projector detect a behind version? → A: Both a 10 s version poll and the immediate same-browser update message; implementation belongs to ITEM-274.
- Q: What does "previous applicable entry" mean? → A: The previous entry that can actually be projected, skipping dividers and unfilled slots; implementation belongs to ITEM-274/275.
- Q: How should a title-only edit be distinguished from a content edit? → A: Browser compares old and new entry payloads field by field; implementation belongs to ITEM-274/275.
- Q: Is a field-by-field compare too expensive? → A: No. Measured: the largest local service has 60 entries and 120 screens in ~26 KB of JSON; 1,000 full compares took 18.3 ms.
- Q: How should the design be split? → A: Foundational versioning + deletion guard is this slice; the four live-surface behaviours become separate cards.
- Q: Do the proposed test seams match expectations? → A: Yes — endpoint tests for the rules, existing Playwright E2E for the notice.
