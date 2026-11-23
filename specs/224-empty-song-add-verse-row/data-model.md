# Data model: Empty song paints one Add verse control

**Spec**: `specs/224-empty-song-add-verse-row/spec.md`

No entities are added, removed or migrated. The two inputs are already on the song page's context:

| Name | Source | Role in this slice |
| --- | --- | --- |
| `verse_rows` | `SongDetailView.get_context_data` — `song.verse_set.filter(is_deleted=False).order_by('number')` | Gate for the `.verse-add` row; empty means "no live verses". |
| `can_edit_verses` | same view — ordinary songbook and editors allowed | Gate for every verse control, unchanged. |
| `song.pk` | same view | The `data-song` pointer on the surviving button, unchanged. |

Layout states added by US2 (no new data): a song with `verse_rows` empty gets `.read[data-kind="song"]:has(.entry__empty)` flexed to the stage height, and its `.read__body:has(> .entry__empty)` becomes one 50% grid band that centres the block. With verses, no selector matches and the article/body keep their existing boxes.

States of `.read__body` on an editable ordinary song:

| `verse_rows` | Verse rows | `.verse-add` row | `.entry__empty` with its button | Total `[data-add-verse]` |
| --- | --- | --- | --- | --- |
| empty | 0 | absent | present | 1 |
| non-empty | 1…n | present after the last | absent | 1 |

A hymn book or a restricted reader has `can_edit_verses = false`: neither control is drawn in either row state.
