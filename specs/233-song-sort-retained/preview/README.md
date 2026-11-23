# Preview — spec 233

**Tier**: live. The change is in the client's post-fetch list reconciliation, so a static page
cannot show it; this is the real reading page running the worktree's own JavaScript.

**URL**: `http://127.0.0.1:8773/songs/book/1/`
**Server**: started from `multimedia-gkps-klender-233` with `manage.py runserver 0.0.0.0:8773 --noreload`,
against the dedicated preview database `gkps233`. The fix is applied in the worktree and uncommitted.

## States to drive by hand

| State | How to reach it | What to read |
| --- | --- | --- |
| Default order | open the URL | rows `Zebra`, `Alpha`; `#songSort` reads `data-order="m"` |
| Alphabetical | click the sort button beside "Filter songs…" | rows `Alpha`, `Zebra`; button reads `data-order="title"` |
| Create with sort retained | click `Add song`, type a title, save | the new row lands in its alphabetical slot; the button still reads `title`; the document does not reload |
| Create in default order | reload the page, then add a song | the new row leads the list; button still reads `m` |
| Edit refresh | toggle to alphabetical, edit a song's title, save | remaining rows stay alphabetical |
| Delete refresh | toggle to alphabetical, delete a song | remaining rows stay alphabetical |
| Row-click refresh | toggle to alphabetical, open the other song | child list stays alphabetical |
| Hymn book | open NKB from the panel | no sort control, number order unchanged |
| No song rows | collapse the songbook / open a book with no songs | nothing reordered |

Measured with a 1440×900 viewport, 2026-11-23:

- default `['Zebra', 'Alpha']` (`m`) → toggled `['Alpha', 'Zebra']` (`title`)
- base commit after creating `Beta`: `['Beta', 'Zebra', 'Alpha']` (`title`) — wrong
- this worktree after the same create: `['Alpha', 'Beta', 'Zebra']` (`title`) — retained
- `performance.timeOrigin` unchanged, in-page marker survived, path `/songs/<new id>/`
