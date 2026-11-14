# Preview — the Tata Ibadah list groups by age

**What to look at**: the reading sidebar (`/tatib/`) and the operator dock (`/obs/dock`), in
both themes, against a demo dataset that puts a row in every bucket and two rows on today.

## The branch, on its own data

```
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/132-tatib-sidebar-date-buckets/preview/probe_date_buckets.py \
    http://127.0.0.1:8766/tatib/ /tmp/tatib-132-panel.png
```

`probe_date_buckets.py` prints each group's bucket key, heading, row count and first/last row, checks
the drawn form of the heading (uppercase, 11.5px, sticky) and measures the `2px`/`10px`/`10px`
divider between two groups. It writes a 1440×900 screenshot.

## A demo dataset (a throwaway SQLite database, never the project's)

The real local data has no services after today, so the `Upcoming` pin and the `Last 30 days` edge
cannot be seen there. A separate instance with its own database shows all four buckets:

```
cd /home/rsmbyk/Projects/multimedia-gkps-klender-132
export DJANGO_DEVELOPMENT_MODE=true            # settings then use ./db.sqlite3
unset DATABASE_URL
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py migrate --noinput
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py shell -c \
    "exec(open('specs/132-tatib-sidebar-date-buckets/preview/seed_demo_data.py').read())"
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8767 --noreload
```

`seed_demo_data.py` writes today ×2, +6 days, +60 days, −8, −30 (the edge), −45, −100, one in
January, −320 and −400 days — one row per boundary — and **deletes every existing service in that
database first**, which is why it must only ever run against the throwaway SQLite file.

## What the preview must show

| Look for | Expected |
| --- | --- |
| Headings, top to bottom | `UPCOMING`, `LAST 30 DAYS`, `EARLIER THIS YEAR`, `OLDER` |
| `Upcoming` order | today's rows first, then the future **farthest** date first (+60 before +6) |
| Today's rows | a solid `TODAY` pill between the name and the date; no row tint |
| The −30-day row | in `Last 30 days` (`Bulan Oikumene`, 25 Sep) |
| The −31-or-older, same-year rows | in `Earlier this year` |
| Last year's rows | in `Older` |
| The dock | the same four headings, the same pill, no tints |
| Both themes | pill green-on-white in light, navy-on-periwinkle in dark |
| Template mode (`?mode=template`) | unchanged: one `Templates` heading |

The badge's treatment (solid pill on `--active-bg`) was chosen by the owner from three rendered
options — outlined chip, solid pill, dot-plus-text — in both themes on both surfaces.
