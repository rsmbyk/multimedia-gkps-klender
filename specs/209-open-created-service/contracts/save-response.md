# Contract: editor save response (spec 209)

`POST /editor/<kind>/new/save/` and `POST /editor/<kind>/<pk>/save/` keep their current answers
(400 re-rendered form, 403 restriction, 200 JSON). The 200 JSON object gains:

| Field | Type | When | Meaning |
| --- | --- | --- | --- |
| `created` | bool | every successful save | the form had no saved instance before this request |
| `record_kind` | int | successful `tatib` saves only | the chosen `TataIbadahKind` value (`0` Normal, `1` Template) |

Existing fields (`ok`, `id`, `kind`) stay byte-for-byte as they are. A client that ignores the new
fields behaves exactly as before. The stage opens only for `kind == 'tatib'`, `created == true`,
`record_kind == 0`.
