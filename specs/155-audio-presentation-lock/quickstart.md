# Quickstart: a playing recording owns the projector screen until it pauses

**Spec**: `specs/155-audio-presentation-lock/spec.md`

## Run the tests

The two modules this slice touches, on a database of their own so a parallel session's run cannot
block them:

```sh
cd ~/Projects/multimedia-gkps-klender-155
DATABASE_URL=postgres://multimedia:multimedia@127.0.0.1:59075/gkps155 \
  ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_audio_display tests.e2e.test_video_display --keepdb
```

`test_audio_display` is the slice's own module; `test_video_display` is the unchanged neighbour whose
three fullscreen cases must stay green — the audio helpers must not move the video's behaviour.

## Drive the live projector

```sh
# the companion only answers the app origin it was started with
cd ~/Projects/multimedia-gkps-klender && docker compose stop web
cd ~/Projects/multimedia-gkps-klender-155 && \
  DATABASE_URL=postgres://multimedia:multimedia@127.0.0.1:59075/multimedia \
  DJANGO_DEBUG=True DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
  ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput && \
  DATABASE_URL=postgres://multimedia:multimedia@127.0.0.1:59075/multimedia \
  DJANGO_DEBUG=True DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
  ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:63404 --noreload
```

Then `/projector?service=144`, `Ctrl+→` to the audio screen (85), `Space` to play.

## Read the readings back

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/155-audio-presentation-lock/preview/probe_lock.py --base http://127.0.0.1:63404
```

Fourteen checks, each naming the requirement it reads; exit code 0 when the route behaves as the spec
says. The spec's own numbers (1440×900 takeover, the place kept at `0:02`) come from this run.

## Restore develop afterwards

```sh
cd ~/Projects/multimedia-gkps-klender && docker compose start web
```
