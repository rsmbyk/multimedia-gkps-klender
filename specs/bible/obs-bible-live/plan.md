# Plan: OBS-BIBLE — OBS Bible dock and source

Spec: [`spec.md`](spec.md) (`OBS-BIBLE`)

## Approach

As-built dock tabs (Bible, Browse, Display, History) over `API-BIBLE` with
BroadcastChannel passage sync. Passage posts on every verse change even when
inactive.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Templates/JS | `multimedia/obs/templates/bible/`, `static/obs/bible/` |
| Domain | `multimedia/bible/models.py` via API |
| Tests | bible BC/hotkeys/history-storage Vitest |

## Contracts

- Channels in `OBS-BIBLE-AC2`.
- History key `OBS_BIBLE_HISTORY`, cap 25.
- Always-post-passage differs from songs/tatib gating.

## Risks and rollout

- Documentation-only; language cue is icon-based (`lang.id === 2`), not a
  separate language toggle control.

## Non-goals

- Web bible admin; changing BC channel names.
