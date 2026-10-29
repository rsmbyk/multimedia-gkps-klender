# Preview: the Media Library list holds still while it refreshes

**Spec**: `specs/148-media-library-refresh-flicker/spec.md`
**Shape**: `live`
**Open**: `http://localhost:63404/media-library/` — the compose `web` service

## Run

```sh
# the route is already served by `docker compose up -d web`; nothing else to start
.venv/bin/python specs/148-media-library-refresh-flicker/preview/frame_sampler.py
```

The sampler drives one refresh from a click (a row's **Remove**, cancelled) and records every
`.media-library__file`'s top on every animation frame from the click to the settled list. It prints
each row's jolt in px and the number of frames that showed the `Service uses unavailable` placeholder.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| refresh from Remove | click a row's trash button, then cancel the dialog | the list jumps up 22px and back before the dialog is even answered |
| refresh from Settings | gear button, then **Save setting** | the same jump, without a dialog staying open |
| first load | reload the page | the list is drawn short and expands 68px within the first ~40ms |
| a transfer running | upload a file from a Tata Ibadah entry | the 2s poll re-draws the list and moves nothing |
| empty / disconnected | stop the `media` service, reload | the empty and disconnected copy are drawn in one pass |

## Live or static

**Live**: the defect is a fetch-then-draw sequence, and a static page cannot show what fetches.

## What is not a preview

A screenshot, a static image and a recording are not previews; the owner's screencast is evidence of
the symptom, not an approval surface.
