# Plan: OBS-TATIB — OBS Tatib dock and source

Spec: [`spec.md`](spec.md) (`OBS-TATIB`)

## Approach

As-built two-tab dock (list + display) over `API-TATIB`. Item order is
API-owned; OBS focuses on activate/step/paste/project.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Templates/JS | `multimedia/obs/templates/tatib/`, `static/obs/tatib/` |
| Tests | tatib BC/hotkeys/storage Vitest |

## Contracts

- Channels in `OBS-TATIB-AC2`.
- item_type 0/1 + synthetic `--- END ---` marker.
- As-built double-post on end markers documented in AC11.

## Risks and rollout

- Documentation-only; end-marker posting quirk is intentional as-built.

## Non-goals

- Adding OBS reorder; changing item_type enum.
