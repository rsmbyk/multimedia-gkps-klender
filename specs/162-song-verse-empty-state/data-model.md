# Data Model: A song with no verses is named, not mistaken for no song

**Spec**: `specs/162-song-verse-empty-state/spec.md`

## Entities

### Song

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `book` | FK `songs.Book` | required; a deleted book hides its songs from the picker | FR-001 |
| `number`, `sub_number`, `title` | number, char, char | the citation's parts | FR-001 |

**Relationships**: Song 1—n Verse — only live verses (`is_deleted=False`) count as the song's verses.
**Validation**: none added by this slice.
**State transitions**: a song with zero live verses is a normal song; nothing marks it.

### ServiceEntry (kind: song)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `song` | FK `songs.Song` | required for this kind | FR-004 |
| `verses` | JSON list of ints | non-empty; must name the song's own numbers | FR-004 |

**Relationships**: ServiceEntry n—1 Song; ServiceEntry n—1 TataIbadah.
**Validation**: `clean` refuses an entry with no song, and one that keeps no verse. This slice splits
the second refusal in two by cause: the song carries no live verses (`This song has no verses: pick
another song.`) versus the entry kept none of them (`Keep at least one verse in the service.`).
**State transitions**: unchanged — a song entry is created with at least one verse, edited, or deleted.

### The Verses field (view state, not a table)

| Field | Values | From |
| --- | --- | --- |
| summary line | `Pick a song first` · `All verses` · `Verses n, …` · `No verses: keep at least one` · `This song has no verses` | FR-001, FR-005 |
| trigger | enabled · disabled (no boxes, or no choice left) | FR-003 |
| boxes | one per live verse number of the picked song, checked per the entry's stored numbers | FR-005 |

**Relationships**: the field 1—1 picked Song; the field 1—n checkboxes.
**Validation**: the field itself accepts an empty selection (`required=False`); the model refuses it.
**State transitions**: no song → song with verses (all boxes checked) → some unchecked → none
checked → a different song; or no song → a song with no verses (the new line, no boxes).

## Invariants

- A song entry always keeps at least one verse when it is stored — enforced by the model, unchanged.
- The summary line never says `Pick a song first` for a picked song that has no verses — in the
  server's markup or after the script runs (FR-001, FR-002).
- With a song that has no verses the trigger is disabled, so its menu cannot open (FR-003).
- The trigger's box is 38px tall in every state, and 436px wide at 1440 / 338px at a 420 viewport
  (SC-003).

## Not modelled

- **A song's "has no verses" flag** — deliberately absent: the empty verse list is the fact, and a
  stored boolean would be a second source (D005).
- **A per-song warning in the picker's options** — out of scope by assumption; the field states it
  once the song is picked.
