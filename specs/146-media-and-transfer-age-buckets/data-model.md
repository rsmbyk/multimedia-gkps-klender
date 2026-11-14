# Data model: the Media Library and the transfer history group by age

**Slice**: `specs/146-media-and-transfer-age-buckets` · **Phase 1**

Nothing here is stored. Both rules are functions of a row and the present instant, computed at draw time,
and the companion's schema does not move.

## Entities

### Age bucket

| field | type | notes |
| --- | --- | --- |
| `key` | string | `last-24-hours` · `last-7-days` · `last-30-days` · `earlier-this-year` · `older` |
| `label` | string | the heading's words, sentence case in the data, uppercase only in CSS |
| `rows` | array | the rows whose key matches, in the caller's order |

A bucket with no rows is never constructed — the renderer walks the ladder and skips empty keys.

### The two ladders

```js
FILE_BUCKETS      = [last-30-days, earlier-this-year, older]
TRANSFER_BUCKETS  = [last-24-hours, last-7-days, last-30-days, earlier-this-year, older]
```

Both are fixed arrays; the ladder's order is its index, and the renderers sort by that index where the
source order is not already monotonic in age (the transfers list, research D4).

### Row shapes read by the rules

| surface | row comes from | fields the rule reads |
| --- | --- | --- |
| Media Library list | `GET http://127.0.0.1:63174/v1/files` → `files[]` | `uploaded_at` (ISO 8601 with offset) |
| Transfers dialog | `GET http://127.0.0.1:63174/v1/transfers` → `transfers[]` | `started_at`, `ended_at`, `id`, `status` |

Everything else on a row (`name`, `family`, `size`, `bytes_done`, `direction`) is drawn unchanged.

### Present day and present instant

- `presentDay(nowMs)` → the Jakarta calendar day as an epoch-ms value at UTC midnight, so two days can be
  subtracted without daylight-saving noise.
- `now` is an argument to both rules, defaulting to `Date.now()`.

### Rendered headings

| surface | element | class | attribute |
| --- | --- | --- | --- |
| Media Library list | `h2` | `media-library__group` | `data-bucket="<key>"` |
| Transfers dialog | `h3` | `media-transfers__group` | `data-bucket="<key>"` |

The list's heading keeps the class it shipped with; the dialog's is new and takes the same numbers
(`components.css`).

## Bucket boundaries

| key | files (calendar days, Asia/Jakarta) | transfers (rolling from the draw) |
| --- | --- | --- |
| `last-24-hours` | — | `0 ≤ age < 24h` |
| `last-7-days` | — | `24h ≤ age < 7d` |
| `last-30-days` | `0 ≤ days ≤ 30` | `7d ≤ age < 30d` |
| `earlier-this-year` | `days > 30`, same Jakarta year | `age ≥ 30d`, same Jakarta year |
| `older` | different Jakarta year | different Jakarta year |

The year test is the Jakarta year of the row's own instant, compared with the present day's — not the UTC
year, which is why D2's `presentDay` exists.

## What does not change

`uploaded_at`, `started_at`, `ended_at`, the transfers table, the files table, the retention setting, the
`/v1/references` sync, the cloud-availability map, and every row's fields and controls.
