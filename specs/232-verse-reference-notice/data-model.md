# Data model: verse reference notice

No entity is added, removed or changed. The slice reads the value the editor context already computes.

| Name | Source | Use in this slice |
| --- | --- | --- |
| `named_service_count` | `multimedia/web/reading/views.py:176-186` — count of `ServiceEntry(kind=SONG)` rows for the verse's song whose `verses` JSON list contains `verse.pk` | printed in the note as `<count> Tata Ibadah`; unchanged |
| `verse_referenced` | same context, `bool(referenced)` | selects the note branch and the disabled button; unchanged |
| `ServiceEntry.verses` | JSON list of verse ids | untouched; the delete guard in `verses.py:116-129` still reads it |

The confirmation dialog (`songs_verse.js:264-268`), the service entry model and all endpoints are unchanged.
