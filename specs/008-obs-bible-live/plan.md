# Plan 008: OBS Bible dock and source

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `OBS-BIBLE` from `specs/bible/obs-bible-live/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/bible/obs-bible-live/{spec,plan,tasks}.md` into `specs/008-obs-bible-live/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/bible/obs-bible-live/plan.md`)</summary>

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


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `OBS-BIBLE` — intended; follow-up may update them.
