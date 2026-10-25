# Data model: the date bucket

**Slice**: `specs/132-tatib-sidebar-date-buckets`
**Persisted entities: none.** The bucket is derived per render and never written.

## Date bucket (computed)

| Field | Type | Source |
| --- | --- | --- |
| `key` | one of `upcoming`, `last-30-days`, `earlier-this-year`, `older` | `bucket_key(service.date, today)` |
| `label` | `Upcoming` · `Last 30 days` · `Earlier this year` · `Older` | the fixed table in `date_buckets.py` |
| `services` | the bucket's rows, in the panel's order | the query, then the today-first stable sort for `upcoming` |

## The rule

Given a service date `d` and the present day `t` (both `datetime.date`, `t` taken in `Asia/Jakarta`):

| Condition | Key |
| --- | --- |
| `d >= t` | `upcoming` |
| `0 < (t - d).days <= 30` | `last-30-days` |
| `d.year == t.year` (and older than thirty days) | `earlier-this-year` |
| otherwise | `older` |

Boundaries, stated as tests: `d == t` → `upcoming`; `d == t - 1 day` → `last-30-days`;
`d == t - 30 days` → `last-30-days`; `d == t - 31 days`, same year → `earlier-this-year`;
`d == t - 31 days`, earlier year → `older`; `d == t + 400 days` → `upcoming`.

## Ordering

| Bucket | Order |
| --- | --- |
| `upcoming` | rows dated `t` first (creation time, newest first), then the later dates, farthest first |
| `last-30-days`, `earlier-this-year`, `older` | date, newest first; ties break on creation time, newest first |

## Where the derived data goes

| Surface | Context key | Row shape |
| --- | --- | --- |
| Reading sidebar (`_tatib_groups`) | `tatib_groups` | `{key, label, services: [{id, name, date, date_display, today, current}]}` |
| Operator dock (`obs_dock`) | `groups` | `{key, label, services: [TataIbadah with short_date, long_date, is_today]}` |
| Saved renderer (`servicePanel`) | — | the same `{key, label, rows}` written to markup in the browser |

## What is removed

- the month key (`YYYY-MM`) and the month heading (`Oktober 2026`) on the dated list of both sides;
- the `data-month` attribute on a group section.
