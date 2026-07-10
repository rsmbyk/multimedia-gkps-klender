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
