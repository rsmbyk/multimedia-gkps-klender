# Plan 007: OBS Songs dock and source

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `OBS-SONGS` from `specs/songs/obs-songs-live/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/songs/obs-songs-live/{spec,plan,tasks}.md` into `specs/007-obs-songs-live/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/songs/obs-songs-live/plan.md`)</summary>

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


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `OBS-SONGS` — intended; follow-up may update them.
