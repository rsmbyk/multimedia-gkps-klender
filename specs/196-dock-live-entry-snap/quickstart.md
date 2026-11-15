# Quickstart — dock live entry snap

**Spec**: `specs/196-dock-live-entry-snap/spec.md` · **Plan**: `specs/196-dock-live-entry-snap/plan.md`

## Prerequisites

- Node / pnpm not required — the dock is server-rendered Django + vanilla JS, no build step.
- The venv is at the main checkout `/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python`.
- Playwright (Python) browsers must be installed (`playwright install chromium`). Tests are run with Django's `LiveServerTestCase`.
- A throwaway database so a concurrent run in another worktree cannot collide on the same `test_*` database; the compose service is on `127.0.0.1:59075`.

## Setup

```bash
export PY=/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python
export DATABASE_URL=postgres://multimedia:multimedia@127.0.0.1:59075/gkps196

$PY manage.py migrate --noinput
$PY manage.py collectstatic --noinput
```

## Run the E2E test suite

```bash
$PY manage.py test tests.e2e.test_obs_dock_snap --noinput
$PY manage.py test tests.e2e.test_obs_dock --noinput
```

## Run by hand

```bash
$PY manage.py runserver 0.0.0.0:8765 --noreload
```

Then open `http://127.0.0.1:8765/obs/` and:

1. **Off-top**: open a service with a long list (or shorten the window height), scroll the list until the live entry is entirely above the viewport, then press any transport key (ArrowRight) — the list glides up until the live entry's row sits flush at the scroller's top edge.
2. **Off-bottom**: scroll the list until the live entry is entirely below the viewport, then press ArrowRight — the list glides down until the live entry's foot rests just above the NEXT band; the band remains visible.
3. **Partly visible**: scroll until the live entry straddles either edge, then press any key — the list glides to the centred position, as before.
4. **Reduced motion**: in your browser/system preferences enable "reduce motion", repeat (1)–(3) — every move is a jump, not a glide.

## What to look for

| Check | Where |
| --- | --- |
| Live entry off-top snaps flush at the top edge of `#runBody` | DevTools → `#runBody` scrollTop equals `liveLi.offsetTop` ± 1 |
| Live entry off-bottom foot rests just above the NEXT band | DevTools → the entry's foot lands 10px below the scroller's bottom edge; the band sits bottom-flush at the edge; the band is not `hidden` |
| No next entry (last entry) snaps foot flush at bottom edge | Delete all entries after the live one; check scrollTop equals `liveLiBottom - runBody.clientHeight` |
| Wheel / pointerdown cancels a pending snap | Start a snap, wheel during it — the scroll stays where the gesture parked it |
| Reduced motion jumps, no frames | Emulate `prefers-reduced-motion: reduce` in DevTools — `scrollTop` changes synchronously |
| Picker, morph, band, baits unchanged | Open the picker, cross entries during a morph — no regression |

## Not yet runnable

None — everything above runs after `$PY manage.py collectstatic` and `runserver`.