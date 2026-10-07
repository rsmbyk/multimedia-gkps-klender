# Plan 010: Combined OBS projection

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `OBS-PROJECT` from `specs/project/obs-project-projection/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/project/obs-project-projection/{spec,plan,tasks}.md` into `specs/010-obs-project-projection/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/project/obs-project-projection/plan.md`)</summary>

# Plan: OBS-PROJECT — Combined OBS project projection

Spec: [`spec.md`](spec.md) (`OBS-PROJECT`)

## Approach

As-built project source subscribes to all three app BC triples, formats
payloads, auto-fits fonts, and mutually excludes active status across apps.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Templates/JS | `multimedia/obs/templates/project/`, `static/obs/project/` |
| Tests | format + settings-storage Vitest |

## Contracts

- Format rules in `OBS-PROJECT-AC3`.
- Mutual mute via status posts with `source: 'source'` + `skipUpdateSubject`.
- Colour key names and defaults in `OBS-PROJECT-AC11`.

## Risks and rollout

- Documentation-only; hotkey/mutual-mute paths are thinly tested.

## Non-goals

- Replacing per-app sources; scene management inside OBS itself.


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `OBS-PROJECT` — intended; follow-up may update them.
