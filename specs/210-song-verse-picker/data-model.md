# Data Model: the song entry's pickers

**Spec**: `specs/210-song-verse-picker/spec.md`

## Entities

No persistent field, model or migration changes. The existing records keep their contracts:

| Entity | Relevant fields | Constraint |
| --- | --- | --- |
| `Song` | `id`, `title`, `number`, `sub_number`, `book` | Existing search/order semantics unchanged (FR-003) |
| `Verse` | `id`, `number`, `song` | Picker answers `{id, number}`; IDs are submitted (FR-011) |
| `ServiceEntry` | `song`, `verses`, `kind` | Stored verse list stays a list of IDs |
| `VersePickerState` (ephemeral) | `selectedIds`, `lastTile`, `dragPreview` | Exists in the form only; discarded when the dialog closes |

**Relationships**: `Song` 1—n `Verse`; `ServiceEntry` n—n `Verse` through its stored ID list.
**Validation**: at least one verse for a song that has verses; no verse may be chosen for a
song with none (FR-014). Both guards already exist in the forms layer and are unchanged.
**State transitions**: `no song → song picked → verses chosen → saved`; the section is hidden
in the first state and for a zero-verse song, muted for a one-verse song (FR-014, FR-015).

## Invariants

- The hidden `name="verses"` inputs always carry IDs, never display numbers (FR-011).
- A drag preview changes paint and the readout only; form values change on release (FR-010).
- Result count never changes the dialog's height (SC-004).
- A fresh pick starts at verse 1; an edit starts with its saved IDs (FR-008).

## Not modelled

- The drag anchor is deliberately not persisted: the owner asked for no mark after release.
- The preview's sample songs and the `Slow` review control are preview-only and never land in
  the product data or UI.
