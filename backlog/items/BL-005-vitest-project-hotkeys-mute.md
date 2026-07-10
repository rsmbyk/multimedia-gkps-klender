# BL-005 — Vitest for project hotkeys 1/2/3 and mutual mute

| Field | Value |
|-------|--------|
| **ID** | `BL-005` |
| **Status** | `ready` |
| **Priority** | `P2` |
| **Size** | `S` |
| **Area** | `test` |
| **Owner** | |

## Problem / why

`OBS-PROJECT` notes that controls `1`/`2`/`3` and mutual-mute status behavior
lack Vitest coverage today, while format and colour storage are covered.

## Outcome

Isolatable Vitest coverage for last-active control posting, keys 1/2/3
rebroadcast, and forcing other apps inactive when one becomes active.

## Acceptance sketch

- Cover `OBS-PROJECT-AC4`, `AC7`–`AC9` as far as isolatable without full OBS.
- Follow TDD; keep mocks consistent with existing project tests.

## Links

| Kind | Ref |
|------|-----|
| Spec | `OBS-PROJECT`, `TEST-COV-AC20` |
| Notes | Called out in `OBS-PROJECT` Notes |

## History

| Date | Note |
|------|------|
| 2026-07-10 | Seeded from `OBS-PROJECT` Vitest gaps |
