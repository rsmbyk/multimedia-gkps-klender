# Preview: a media size reads in the unit that still shows its number

**Spec**: `specs/145-media-size-precision/spec.md`
**Shape**: `live` — the slice's own server
**Open**: `http://127.0.0.1:8821/tatib/149/` → **New media**

## Run

```sh
cd ~/Projects/multimedia-gkps-klender-145
DATABASE_URL="postgres://multimedia:multimedia@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8821 --noreload
```

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| card, small file | New media → choose a file under 50 KB | `Image · 12.3 KB` — where the old line read `0.0 MB` |
| card, sub-kilobyte file | choose a file under 1 KB | `Image · 512 B` |
| card, exactly 1 MB | choose a file of 1,000,000 bytes | `Image · 1 MB`, not `1.0 MB` |
| card, cap | choose a file of 200,000,000 bytes | `Image · 200 MB` |
| library row | same file, after saving; then the Media Library page | the same string the card showed |
| library Total | Media Library → status popup | the summed bytes formatted once, not a sum of labels |
| empty library | a library with no files | unchanged empty state; no label |
| error | a file over 200 MB | the existing "File too large" dialog, unchanged |

## Why live

What the label derives from is a companion payload (`/inspect`, `/files`) — a fact about this computer.
A static page could print the strings but not the path that produces them, so the preview is the real
modal on the real route.

## What is not a preview

A screenshot, a static image and a recording are not previews.
