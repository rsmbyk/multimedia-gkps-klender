# Fold — the computer's own fonts reach the converter

**Date**: 2026-11-01
**Slice**: `182-host-font-detection`

## Capabilities touched

- `local-stack` — **created** (the startup assumptions and the host font sources)
- `media-library` — **modified** (`R2` which face is drawn, `R4` which sources are read)

## Operations

### `local-stack`

- `added` **R1 — The stack starts on an operator's computer**: no compose default may rely on a
  variable a platform does not define; a font directory the machine lacks must not stop the services;
  a machine with none starts as before. Three scenarios.
- `added` **R2 — The stack reads the fonts the computer already has**: the launcher mounts the
  machine's own font directories read-only; the converter draws a family so mounted; the image keeps
  only free substitutes and nothing is copied; a directory the daemon cannot read is skipped and named.
  Three scenarios.

### `media-library`

- `modified` **R2 — A converted deck keeps the deck's own layout**: the mapping is now the fallback,
  not an override — a family installed on the computer that converts is drawn in that family. One
  scenario added.
- `modified` **R4 — The converter draws the faces the computer has, and the folder an operator adds**:
  two sources (the computer's directories under `/usr/share/fonts/host`, the operator's directory at
  `/usr/share/fonts/operator`, default `.fonts/`), the operator's copy winning a same-family clash, and
  an unreadable source skipped rather than mounted empty. Renamed; `R4` preserved. Two scenarios added.

## Before / after

| Capability | Requirements | Scenarios |
| --- | --- | --- |
| `local-stack` | 0 → 2 | 0 → 6 |
| `media-library` | 4 → 4 | 11 → 14 |

## Not folded

Nothing. The Converge pass's accepted partial (the media image not rebuilt on this machine) is a
verification gap, not an unfolded behaviour.
