# Data model: a contents row marks its entry's kind

**Spec**: `specs/214-sidebar-entry-kind-marks/spec.md`

## n/a — no stored state changes

The slice reads kinds the models already hold and draws them. No field, migration, constraint, index
or fixture changes.

| What | Where it already lives | What this slice does with it |
| --- | --- | --- |
| an entry's kind | `ServiceEntry.kind` (`ServiceEntryKind`: `TEXT=0`, `SCRIPTURE=1`, `SONG=2`, `SECTION_BREAK=3`, `MEDIA=4`, `FILL_IN=5`, `CHOICE=6`), `multimedia/tatib/models.py:133-149` | mapped to a mark key in `_tatib_stage()` |
| a legacy row's shape | `TataIbadahItem.item_type` (`TEXT=0`, `END_OF_SECTION=1`), `models.py:65-83` | TEXT → `text`; END_OF_SECTION takes no mark |
| a slot's resolved kind | `SlotKind(row.fill_kind).name.lower()` in `views.py:1407-1409` | carried as `mark_kind` for the badge |
| the order and numbering | `_ordered_service_rows()` and `text_count` in `views.py:1350-1576` | untouched |

## The new row payload keys

`_tatib_stage()` adds two keys to the `toc` rows it already builds:

| Row | `mark` | `mark_kind` |
| --- | --- | --- |
| legacy text (`views.py:1393`) | `text` | — |
| legacy EOS (`:1381`) | — (row is `eos`) | — |
| fill-in / choice (`:1474`) | `fill_in` / `choice` | `slot_kind` (`text` · `scripture` · `song` · `media`, or `''`) |
| section-break entry (`:1486`) | — (row is `eos`) | — |
| ordinary entry (`:1554`) | `kind_key` — `text`, `scripture`, `song` or `media` | — |

The template keys its glyphs on these strings and treats anything else as "no mark", so an
unrecognised value degrades to today's unmarked row rather than a broken glyph. A slot with an empty
`mark_kind` draws the dashed frame without a badge — spec 213 FR-007's legacy case.
