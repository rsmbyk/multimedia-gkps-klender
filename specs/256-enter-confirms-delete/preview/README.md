# Preview: Enter accepts a delete confirmation

**Spec**: `specs/256-enter-confirms-delete/spec.md`
**Shape**: `live` — the real reading application served from this slice's worktree. The behaviour
includes fetches and server-rendered records, which a static page cannot show.

**Open**: `http://127.0.0.1:8768/` — from the home URL, click through in-page as the owner does.

## Run

```sh
# from the slice worktree, with the project venv
.venv/bin/python specs/256-enter-confirms-delete/preview/serve.py   # background, port 8768
```

`serve.py` reads the Compose database credential at run time and seeds the isolated `gkps256`
database. It calls `collectstatic` on start; after any `static/` edit, restart it before probing.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| Stage entry confirm | Tata Ibadah rail → service → hover first entry → Delete | Press Enter with focus away; one `POST /editor/entry/<pk>/delete/`, dialog closes |
| Sidebar record confirm | Tata Ibadah rail → hover service row → Delete | Press Enter with focus away; one `POST /editor/<kind>/<pk>/delete/` |
| Verse confirm | Kidung rail → book → song → edit verse → Delete verse | Press Enter with focus away; one `POST /editor/verse/<pk>/delete/` |
| Media removal | Media Library rail → a file's Remove action → confirmation | Press Enter; Remove file activated once |
| Cancel focus | open any confirmation, Tab to Cancel, press Enter | Destructive action still runs |
| Disabled / hidden / modified | disabled Remove button, closed dialog, or Shift+Enter | No activation |
| Non-destructive confirm | Copy as template / Use template / screen-mode switch | Enter unchanged |

## Evidence

- `probe.py <tag>` writes `probe-results-<tag>.jsonl`: one observable row per surface.
- `probe-results-baseline.jsonl` — before the change: 0 POSTs and 0 Remove-file clicks.
- `probe-results-after-fixed.jsonl` — after: 1 POST on each of the three delete surfaces and 1
  Remove-file click; no extra requests from the probe's own watcher.
- `run-tests.py tests.e2e.test_enter_delete_confirm` — four targeted E2E pins, all green.
