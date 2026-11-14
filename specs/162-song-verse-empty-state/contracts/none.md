# Contracts: A song with no verses is named, not mistaken for no song

**Spec**: `specs/162-song-verse-empty-state/spec.md`

## Interfaces exposed by this slice

`none` — the slice adds no HTTP endpoint and no JavaScript API. `GET /editor/entry/song/<pk>/verses/`
keeps its shape (`{"verses": [ints], "title": str}`) and its status codes; the entry form's POST
payload is unchanged (`song`, `verses`); the modal's markup keeps every id and data attribute it has,
so the script's handles (`#id_song`, `#entry-verses`, `[data-verses-trigger]`,
`[data-verses-summary]`) keep working.

Two internal things change and are not contracts:

- **`SongEntryForm.song_has_no_verses`** — a Python property read by `_entry_form.html`. It is not a
  context variable the view supplies, and nothing outside the template reads it.
- **The two refusal sentences** — `ServiceEntry.clean`'s message split by cause. The refusal itself
  (a `ValidationError` keyed `verses`) is the existing contract with the form and the view, and it is
  unchanged; only the text differs.

## Not exposed

- Which line the summary carries is the page's own state; nothing announces it to an API.
- The verses endpoint's ordering and soft-delete handling (`is_deleted=False`) — unchanged.
