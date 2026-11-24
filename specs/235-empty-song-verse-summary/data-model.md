# Data Model: An empty song names itself in the Verses section

## Entities

No model, migration, form field or endpoint changes. The slice reuses:

| Existing thing | Role here |
| --- | --- |
| `ServiceEntry.kind = SONG` with `song` and `verses` | The entry being edited; unchanged. |
| `SongEntryForm.song_has_no_verses` (`reading/entries.py:183-191`) | Server-side flag: a song is picked and its `verses` field has no choices. |
| `data-verse-panel` element (`_entry_form.html:201`) | The section; gains `data-empty="true"` for the picked-but-empty state. |
| `{id, number}` verse JSON and `name="verses"` checkboxes | Unchanged value carriers. |

## State matrix

| State | `panel.hidden` | `data-empty` | Label | Summary text | Body rows |
| --- | --- | --- | --- | --- | --- |
| No song picked | `true` | absent | hidden by `:has()` rule | `Pick a song first` | hidden |
| Picked, no live verses | `false` | `true` | visible | `This song has no verses` | hidden |
| Picked, verses exist | `false` | absent | visible | `Bait …` / `No verses: keep at least one` | visible |
| One verse | `false` | absent | visible | `Bait 1` | visible, muted via `data-muted="true"` |

The server renders the first three rows directly. `verseSummary()` re-derives `hidden` and
`data-empty` on every pick, tile change and All/Clear press, so a script-driven state always
agrees with the fragment's.

## Invariants

- `data-empty="true"` implies zero verse checkboxes; the inverse need not hold (a song whose
  fetch failed can also have zero boxes, and must show the failure notice, not the empty line).
- The save refusal strings stay byte-identical: `This song has no verses: pick another song.`
  and `Keep at least one verse in the service.`
- A stored entry with verse IDs for a song that now has no live verses keeps those IDs and
  shows the full picker, as it does today (`test_an_edit_form_keeps_the_verses_an_entry_stored`).
