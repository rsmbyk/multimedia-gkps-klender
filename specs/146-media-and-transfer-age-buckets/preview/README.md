# Preview: the Media Library and the transfer history group by age

**Spec**: `specs/146-media-and-transfer-age-buckets/spec.md`
**Shape**: `static` — `preview.html`, opened directly, no server of its own.
**Open**: `specs/146-media-and-transfer-age-buckets/preview/preview.html`

## Why static, and what it cannot show

The change is a grouping rule over rows the page has already fetched: no route, no serializer, no
companion endpoint moves. So the page is assembled from the Media Library's own markup, class names, icon
set and its untouched stylesheets — `assets/*.css` are `static/styles/design/*.css` frozen at `05379336`,
the commit this branch was cut from — and the buckets are computed in the page's own script.

What it cannot show is the fetch: the two surfaces draw their rows from the loopback companion
(`http://127.0.0.1:63174/v1`), which allows exactly `http://localhost:63404` and `http://127.0.0.1:63404`
— not a `file://` page. Both data sets are therefore in the page: **Fixtures** (a hand-dated set that
reaches every bucket) and **Real snapshot** (the companion's actual eight files and nine transfers, read
at 2026-10-28 21:40 WIB). The rows are built by the same class anatomy the real scripts build them with.

## What the real snapshot shows

| list | buckets today |
| --- | --- |
| Media Library, 8 files | one only — `Last 30 days` (uploads on 28, 25, 19 and 17 Oct) |
| Transfers, 9 rows | `Last 24 hours` · `Last 30 days` (eight uploads today, one on 18 Oct) |

That is the point of the change on real data: the current list draws four per-day headings for those
eight files (28, 25, 19 and 17 Oct), and the dialog draws nine undated rows.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| three buckets | **Fixtures**, upload-date sort | `LAST 30 DAYS`, `EARLIER THIS YEAR`, `OLDER` — one heading per bucket, never one per day |
| the ladder | **Fixtures**, transfers | `TODAY`, `LAST WEEK`, `LAST 30 DAYS`, `EARLIER THIS YEAR`, `OLDER`, each over its own rows |
| the labels | **Today · Last week** / **Last 24 hours · Last 7 days** | the two new rungs, in place, at real size — the open question of FR-016 |
| an active row | **Fixtures**, transfers | the running upload draws first, inside its own bucket, with its percentage |
| the real thing | **Real snapshot** | today's eight uploads under one heading; the nine transfers under two |
| dark | **Dark** | `--head-ink` headings over `--canvas`, same numbers |

Not reachable here, and therefore checked on the served page at implement time: a bucket emptied by the
type chips, the `Unused` chip's effect on a heading, the size sort drawing no headings, and the rail's
progress flyout.
