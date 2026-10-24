# Data Model: A saved hymn song page never shows the song sort control

**Spec**: `specs/125-saved-song-sort-parity/spec.md`

## Entities

`n/a — the slice adds, removes and changes no stored entity, field, relationship, migration or saved payload; the sort control is rendered markup only.`

## Invariants

- A Kidung page offers the song sort control exactly when its book is not a hymn book. (FR-001, FR-003)
- The saved render and the server render agree on that value for every song route. (FR-004, SC-002)
- No other rendered field on a Kidung route changes between the two renders. (FR-005)

## Not modelled

- The book's hymn flag — `Book.is_hymn_book`, already stored and already supplied to the saved renderer's
  songbook payload.
- The control's own ordering choice — client state in `reading.js` (`songSort`), already existing and
  unchanged.
