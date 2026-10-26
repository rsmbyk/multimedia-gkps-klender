# Data Model: Keep reading views current after sidebar edits

**Spec**: `specs/134-sidebar-save-freshness/spec.md`

## Entities

### Saved reading record

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| Existing model identity | Tata Ibadah, songbook, or song primary key | Existing Django model and server validation remain authoritative; no new fields | FR-001, FR-005 |
| Saved values | Existing model fields and derived labels | Read from the existing server-rendered route after a successful save | FR-001, FR-002, FR-003 |

**Relationships**: A song belongs to a songbook; a Tata Ibadah contains ordered service entries. These existing relationships supply the headings and content rendered by current routes.
**Validation**: Existing editor endpoints retain their current authorization and validation rules (FR-005).
**State transitions**: No persistent state transition is added. A successful edit changes the existing record; the reading shell then renders the persisted result.

### Reading shell view state

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| Current route and search query | URL path and query string | Retain the active result page and query through refresh | FR-003, FR-004 |
| Active section and selected record | Existing root data attributes and selected rows | Preserve an unrelated stage and the current selection when the record remains available | FR-002, FR-004 |
| Sidebar presentation | Open, mini, or closed state per existing pane | Save refresh does not select a new main-menu state | FR-004 |
| Operator position | Filter values, scroll offsets, and focus target | Preserve unless a row no longer matches an active filter or query | FR-004 |
| Visible representations | Existing rows, stage, title, search result groups | Reconciled from the server response; not stored independently | FR-001, FR-002, FR-003 |

**Relationships**: One saved record may have several simultaneous visible representations in the shared reading shell. One search result set belongs to the active query/history entry.
**Validation**: No new persisted fields or client-side source of record is introduced.
**State transitions**: The editor emits the existing save event after success; the shell fetches current server markup, reconciles applicable regions, reapplies active filters, and updates the current search snapshot when results are open.

## Invariants

- The saved server representation wins over any value that was only present in an editor form (FR-001, FR-005).
- A save refresh leaves unrelated stage content and the current route in place (FR-002).
- Search result membership, group counts, and the current tab-local snapshot agree with the existing query after refresh (FR-003).
- No database schema or persistent UI-state changes are required (FR-001–FR-006).

## Not modelled

- No changes to `TataIbadah`, songbook, song, or service-entry database schemas; the slice changes only how existing saved values are reconciled into the live reading shell.
- No queued offline editor writes or changes to the IndexedDB library generation; the accepted scope is successful online saves.
- No new management, admin, Media Library, projector, or OBS edit state; those surfaces are outside the shared sidebar save path.
