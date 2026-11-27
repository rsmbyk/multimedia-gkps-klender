# Contract: editor save response (spec 225)

`POST /editor/<kind>/new/save/` keeps its current answers (400 re-rendered form, 403 restriction,
200 JSON). The 200 JSON object already carries `ok`, `id`, `kind` and `created`; this slice adds
no field and changes no status code.

| Field | Type | When | Used here for |
| --- | --- | --- | --- |
| `id` | int | every successful save | the destination URL |
| `kind` | str | every successful save | `songbook` → `lists`, `song` → `song` |
| `created` | bool | every successful save | gate: only `true` opens a record |

A client that ignores the branch behaves exactly as before. The open runs only for
`kind in ('songbook', 'song')` with `created === true`; all other saves take the existing list
refresh, including the created Normal service of spec 209.
