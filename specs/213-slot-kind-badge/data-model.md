# Data model: a slot states the kind it resolves to

**Spec**: `specs/213-slot-kind-badge/spec.md`

## n/a — no stored state changes

This slice reads a value the model already holds and draws it. No field, migration, constraint, index
or fixture changes.

| What | Where it already lives | What this slice does with it |
| --- | --- | --- |
| the slot's kind | `ServiceEntry.fill_kind` (`SlotKind`: `TEXT=0`, `SCRIPTURE=1`, `SONG=2`, `MEDIA=4`), `multimedia/tatib/models.py:143-149` | reads it |
| the row's resolved kind, lowercased | `views.py:1407-1409` → `item['slot_kind']`, already carried on the row as `data-slot` | passes it to the mark's include |

The template already receives `item.slot_kind`; the only new plumbing is one include argument
(`fill_kind=item.slot_kind`). A row whose `fill_kind` is `None` yields the empty string and draws no
badge — the legacy case FR-007 names.

## The value's shape

`slot_kind` is produced by `tatib_models.SlotKind(row.fill_kind).name.lower()`, so it is exactly one of
`text` · `scripture` · `song` · `media`, or `''`. The badge partial keys its four glyphs on those
strings and treats anything else as "no badge", so an unreadable kind cannot paint a broken glyph.
