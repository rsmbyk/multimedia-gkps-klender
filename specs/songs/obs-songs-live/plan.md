# Plan: OBS-SONGS — OBS Songs dock and source

Spec: [`spec.md`](spec.md) (`OBS-SONGS`)

## Approach

As-built ES-module dock/source under `multimedia/obs` with Rx subjects bridged
to BroadcastChannel. Bookmarks and search call product APIs; display settings
use prefixed localStorage.

## Touch points

| Area | Files / modules |
|------|-----------------|
| URLs/templates | `multimedia/obs/` songs dock/source templates |
| JS | `multimedia/obs/static/obs/songs/` |
| Shared | `multimedia/obs/static/obs/common/` |
| Tests | songs BC/hotkeys/bookmark-storage Vitest |

## Contracts

- Status boolean `true`/`false` (sources compare `=== true`).
- Content posts gated on active (except force on activate).
- Channels listed in `OBS-SONGS-AC2`.

## Risks and rollout

- OBS caches browser sources aggressively — hard-refresh after deploys
  (README).
- Some display navigation paths lack Vitest coverage today.

## Non-goals

- Reworking BC channel names; project multi-listen (see `OBS-PROJECT`).
