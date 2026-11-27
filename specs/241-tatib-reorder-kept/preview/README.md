# Preview — spec 241

**Tier**: live. Both faults are in the client's gesture and post-fetch reconciliation, so a static
page cannot show them; this is the real reading page running this worktree's own JavaScript.

**URL**: `http://127.0.0.1:8791/tatib/322/`
**Server**: started from `multimedia-gkps-klender-241` with `manage.py runserver 127.0.0.1:8791
--noreload`, against the development database. The fix is applied in the worktree and uncommitted.

## States to drive by hand

| State | How to reach it | What to read |
| --- | --- | --- |
| Contents order | open the URL | `#chList` rows are in the server's order; the sorter has no song rows to touch |
| After an edit | edit any entry's text and save | the break divider stays where the server put it; no row jumps to the end |
| Drag a row to the top | grab the last grip and drop it above the first row | the row leads both the sidebar and the stage; one "Entry order saved" report |
| Reload | reload the URL | the same order is still painted in both lists |
| Cancel | start a drag and press Escape | sidebar and stage return to the pre-drag order; no write is posted |
| Song list | open a songbook, toggle `#songSort`, create a song | the chosen sort still survives the refresh (spec 233) |

Measured at 1440×900 with the worktree's code, on the scratch service 322 (one break row has no
`section[data-entry-pk]`, so the pane list is one shorter than the sidebar list):

| Moment | Sidebar rows | Stage sections |
| --- | --- | --- |
| base, after add | `1945, 1946, 1944, …` | `1946, 1944, …` (break at the top) |
| base, after dragging `1934` to the top | `1934, 1945, 1946, 1944, …` | `1934, 1946, 1944, …` |
| this worktree, after the same drop | `1934, 1945, 1946, 1944, …` | `1934, 1946, 1944, …`, and a reload keeps it |

The four-entry E2E fixture gives the cleaner before/after: on the base commit an edit painted
`[4, 1, 2, 3]` while the server held `[1, 2, 3, 4]`; after this fix both lists read
`[1, 2, 3, 4]`, and a drag of entry 3 to the top paints `[3, 1, 2, 4]` on the sidebar and
`[3, 1, 2]` on the stage, with the same order after reload.
