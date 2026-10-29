# Preview: A playing recording owns the projector screen until it pauses

**Spec**: `specs/155-audio-presentation-lock/spec.md`
**Shape**: `live`
**Open**: `/projector?service=144` — the local Tata Ibadah that carries an audio entry (screen 85)

## Run

```sh
# The media companion only answers the app origin it was started with, so the slice's
# server has to stand on that origin: stop the compose web and serve this worktree there.
cd ~/Projects/multimedia-gkps-klender && docker compose stop web
cd ~/Projects/multimedia-gkps-klender-155 && \
  DATABASE_URL=postgres://multimedia:multimedia@127.0.0.1:59075/multimedia \
  DJANGO_DEBUG=True DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
  ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput && \
  DATABASE_URL=postgres://multimedia:multimedia@127.0.0.1:59075/multimedia \
  DJANGO_DEBUG=True DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
  ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:63404 --noreload
```

The probe drives the same route and prints the readings the spec quotes:

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/155-audio-presentation-lock/preview/probe_lock.py --base http://127.0.0.1:63404
```

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| at rest | `Ctrl+→` until the audio screen shows | seek bar and `0:00 / 5:02`, corner cue in the lower left |
| playing (fullscreen) | `Space` | the screen fills with `#171613`; only the seek bar and times; no cue, no zones; keys and edge clicks do nothing |
| paused | `Space` again | the normal projector screen is back, cue and all, the recording held at the same time |
| ended | play to the end | fullscreen ends by itself, screen paused at `5:02` |
| fullscreen refused | a browser that denies `requestFullscreen` | the recording plays on the normal screen, keys and zones still do nothing until paused |
| idle | wait 3.5s while playing | seek bar dims to `.52`, times to `.4` — unchanged by this slice |

## Live or static

**Live** — this is the project's own projector route on the local database, playing a real
`/v1/files/<sha256>` recording through the media companion, because the behaviour under test is
precisely what the player does when the page's inputs arrive. A static page cannot show it.

## What is not a preview

A screenshot, a static image and a recording are not previews, so none is kept in this folder: the
evidence is the probe's own readout and the E2E cases.
