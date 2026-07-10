# BL-006 — Vitest for OBS display navigation and end-marker paths

| Field | Value |
|-------|--------|
| **ID** | `BL-006` |
| **Status** | `idea` |
| **Priority** | `P2` |
| **Size** | `M` |
| **Area** | `test` |
| **Owner** | |

## Problem / why

OBS live specs note thin or missing Vitest for display.js navigation / END
logic (songs), activate rules on tatib `item_type` / end markers, and related
paths that are easy to regress during dock refactors.

## Outcome

Isolatable tests for the highest-risk display navigation and end-marker
behaviors called out in `OBS-SONGS` / `OBS-TATIB` notes.

## Acceptance sketch

- Prioritize songs last-lyric / last-verse / refuse-activate-on-END and tatib
  EOS activate refusal / empty post behavior.
- Prefer unit-style tests over brittle full Semantic UI snapshots (`TEST-COV`).

## Links

| Kind | Ref |
|------|-----|
| Spec | `OBS-SONGS`, `OBS-TATIB`, `TEST-COV` |
| Related | `BL-005` |

## History

| Date | Note |
|------|------|
| 2026-07-10 | Seeded from OBS as-built Vitest gap notes |
