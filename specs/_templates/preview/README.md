# Preview: <short title>

**Spec**: `specs/NNN-slug/spec.md`
**Shape**: `live` or `static`
**Open**: `/<url path>` for a live preview, or `specs/NNN-slug/preview/<file>.html` opened directly

## Run

```sh
<the command that serves a live preview, from the repo root — or "none: open the file directly" for a static one>
```

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| default | open the route | |
| empty | <fixture or action> | |
| error | <fixture or action> | |
| loading | <throttle or fixture> | |
| responsive | resize to <breakpoint> | |

## Live or static

**Live** is served from the project: its own route, components and tokens, running.

**Static** is one or more HTML pages assembled from the project's real templates, class names, stylesheets, tokens and assets, opened directly. It is a preview, not a fallback — no reason sentence, and no server of its own.

**What a static page cannot show:** anything that fetches — server-rendered context, the API, uploaded media. A slice that changes one of those is previewed live.

## What is not a preview

A screenshot, a static image and a recording are not previews.
