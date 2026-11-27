# Preview — spec 234

**Tier**: live. The change is in the client's `editor:saved` navigation path, so a static page
cannot show it; these are the real reading pages from two worktrees against one database.

| Server | Worktree | Port | Code |
| --- | --- | --- | --- |
| Before | `/home/rsmbyk/Projects/gkps234-base` (detached at `be9863d2`) | 8775 | unmodified `develop` head |
| After | `/home/rsmbyk/Projects/multimedia-gkps-klender-234` | 8774 | preview change in `static/web/reading.js`, uncommitted |

Both were started with `preview/serve.py` (which builds the local `DATABASE_URL` at run time,
runs `collectstatic` and serves with `--noreload`) against the dedicated `gkps234` database,
created and migrated by `preview/setup_db.py`. Confirm the process cwd with `ss -ltnp` and
`readlink /proc/<pid>/cwd` before trusting either port.

**URLs**: start at `http://127.0.0.1:8774/` (after) or `http://127.0.0.1:8775/` (before) and click
through the rail's Tata Ibadah entry; the probe uses the direct `/tatib/` and `/tatib/?mode=template`
routes.

```
<VENV>/python specs/234-open-created-template/preview/setup_db.py gkps234
<VENV>/python specs/234-open-created-template/preview/serve.py --port 8775 --worktree <base worktree>
<VENV>/python specs/234-open-created-template/preview/serve.py --port 8774 --worktree <slice worktree>
<VENV>/python specs/234-open-created-template/preview/clear_records.py
<VENV>/python specs/234-open-created-template/preview/probe.py http://127.0.0.1:8775 http://127.0.0.1:8774
<VENV>/python specs/234-open-created-template/preview/measure.py
```

## States to drive by hand

| State | How to reach it | Before | After |
| --- | --- | --- | --- |
| Template from dated list | open `/tatib/`, Add Tata Ibadah → **Template**, name, Save | URL stays `/tatib/`; stage empty | URL `/tatib/<id>/?mode=template`; stage names the template |
| Template from template list | open `/tatib/?mode=template`, Add → **Template**, Save | URL stays `/tatib/?mode=template`; stage empty | same stage as above, mode button still pressed |
| Dated service | open `/tatib/`, leave **Normal**, name, Save | `/tatib/<id>/` | `/tatib/<id>/` (unchanged) |
| Empty template stage | after the template opens | not reachable from create | invitation and add actions as on a hand-opened row |
| Refused create | clear the name and save | dialog stays, no stage | unchanged |
| Edit / delete / generate / copy | existing controls | unchanged | unchanged |

## Measured, 1440×900 dark, 2026-11-23

`preview/probe.py` (same database, real create form, 800 ms settle):

| Start | Case | After — base | After — slice |
| --- | --- | --- | --- |
| `/tatib/` | Template | path `/tatib/`, `#readName` `''`, `data-ch` `closed`, current row `null` | path `/tatib/8/?mode=template`, `#readName` `Probe after template 261883`, `data-ch` `open`, current row `8`, `#tatibMode` `aria-pressed=true` |
| `/tatib/?mode=template` | Template | path `/tatib/?mode=template`, no stage | path `/tatib/9/?mode=template`, `#readName` `Probe after template_from_template_list 263684`, current row `9` |
| `/tatib/` | Dated | path `/tatib/7/` | path `/tatib/10/` |

In both after cases: marker `window.__gkps234 = 'alive'` survived, `performance.timeOrigin` was
identical before and after, `data-nav` stayed `open`, and the focused row carried
`book row-flash focus-restore-quiet` with `data-name` equal to the new id. No page errors on either
server.

`preview/measure.py` on the opened template stage: `#readName` x976 y73 362×94, eyebrow x976 y43
127×27, empty invitation x1049 y257 253×26, current sidebar row x90 y164 395×38; `data-nav=open`,
`data-ch=open`, mode pressed `true`. No box changes — only the destination changes.
