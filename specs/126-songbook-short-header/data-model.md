# Data model: A song page cites its songbook by its short name

**Spec**: `specs/126-songbook-short-header/spec.md`

`n/a — no entity, field, relationship, constraint, migration or payload changes.` The slice reads two
existing fields and one existing flag.

## Entities read (unchanged)

| Entity | Fields the header reads | Notes |
| --- | --- | --- |
| **Songbook** (`songs.Book`) | `name` (unique full name), `short_name` (≤ 8 chars, optional, unique among the non-blank), `is_hymn_book` | the slice chooses between `short_name` and `name`; it writes neither |
| **Song** (`songs.Song`) | `book`, `number`, `sub_number` | `number is None` is a legal state and is handled (D005) |

## Derived value

The header text is a pure function of the two rows:

| Songbook | Song | Header |
| --- | --- | --- |
| hymn, `short_name='PKJ'` | `number=4` | `PKJ 4` |
| hymn, `short_name='KJ'` | `number=24`, `sub_number='a'` | `KJ 24A` |
| hymn, `short_name=''` | `number=4` | `<name> 4` |
| hymn, either short name | `number=None` | `short_name or name` |
| ordinary | any | `<name>` |

Nothing is persisted: the value is computed per request by the view and per render by the browser.
