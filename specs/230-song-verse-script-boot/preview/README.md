# Preview: A song opened from the sidebar can edit its verses

**Spec**: `specs/230-song-verse-script-boot/spec.md`
**Shape**: `live`
**Open**: `http://127.0.0.1:8771/` — click through Songs → Lagu → `Anggo Marhorja Tonduy In`

## Run

```sh
# from the slice worktree; the launcher resolves the compose DB itself
bash specs/230-song-verse-script-boot/preview/serve.sh
# the unmodified comparison server is already on http://127.0.0.1:63404/
.venv/bin/python specs/230-song-verse-script-boot/preview/probe.py
```

`probe.py` takes an optional before and after base URL so it survives a port change.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| home | open `/` | `Add verse` does not exist yet; the verse script is already in the document |
| after sidebar navigation | click Songs → *Lagu* → `/songs/1387/` | the page arrives with no reload; `Add verse` now opens `New verse` |
| edit | activate the pencil on verse 1 | dialog opens with `Edit verse 1` |
| direct load | navigate straight to `/songs/1387/` and reload | the dialog still opens; exactly one script include |
| before | repeat the path on port 63404 | both buttons are dead until the page is refreshed |

## Live or static

**Live** is served from the project: its own route, components and tokens, running.

**Static** is one or more HTML pages assembled from the project's real templates, class names, stylesheets, tokens and assets, opened directly. It is a preview, not a fallback — no reason sentence, and no server of its own.

**What a static page cannot show:** anything that fetches — server-rendered context, the API, uploaded media. This slice changes whether a script executes after a fetch-driven swap, so the preview is live.

## What is not a preview

A screenshot, a static image and a recording are not previews.
