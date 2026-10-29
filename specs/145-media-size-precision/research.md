# Research: a media size reads in the unit that still shows its number

**Spec**: `specs/145-media-size-precision/spec.md`
**Unknowns remaining**: 0

## D001 — Which unit base

- **Decision**: decimal — `1 KB = 1,000 B`, `1 MB = 1,000 KB`, `1 GB = 1,000 MB`.
- **Rationale**: the product already counts this way — the upload cap is written `200 MB` against
  `file.size > 200000000`, `media-entry.js` divides by 1,000,000, and the companion reports
  `byte_count`. A binary base would relabel every existing file by 4.9% for no user-visible gain.
- **Alternatives considered**: binary (KiB/MiB) — rejected as an inconsistent relabelling of a cap that is
  already decimal; both bases displayed — rejected as noise in a 12px line.
- **Provenance**: research (the shipped constants).

## D002 — How precise one label is

- **Decision**: round to one decimal; print the decimal only when it is not `.0`.
- **Rationale**: one decimal is what the shipped card already shows, so nothing about the line's rhythm
  changes; trimming `.0` keeps `2 KB` from reading as falsely precise. Three decimals would make the line
  `12.346 KB` — more digits than an operator needs before saving.
- **Alternatives considered**: fixed one decimal (`2.0 KB`) — owner chose the trimmed form at Clarify;
  significant figures (3 s.f.) — rejected, it prints `1.23 KB` and `999 B`, two rules in one line.
- **Provenance**: owner decision (Clarify, 2026-10-28); option recorded in `spec.md`.

## D003 — What stops the `1000` case

- **Decision**: after rounding, a value that reaches 1000 is promoted to the next unit (`999,999 B → 1 MB`).
- **Rationale**: `Math.round(999.999)` per mille is `1000 KB`, which is worse than the bug being fixed: a
  unit that has run out of room. The rule is one comparison, and it also keeps `GB` reachable.
- **Alternatives considered**: truncate instead of round (`999 KB`) — rejected, it understates a file at
  the cap boundary; per-unit thresholds hand-written (`< 999500 → KB`) — rejected as the same rule with
  more places to drift.
- **Provenance**: research.

## D004 — One function or three

- **Decision**: one `window.gkpsFormatSize` in a new `static/web/media-size.js`, loaded before the three
  media scripts in `reading/base.html`; the two live call sites delegate, the dead one is deleted.
- **Rationale**: measured — the two live formulas already disagree on the same file (`0.0 MB` vs `12 KB`),
  which is what a copied formula produces over time. A shared function is also what an E2E test can hold
  to one string on every surface.
- **Alternatives considered**: patching each formula in place — rejected, three copies of a rounding rule
  is how the disagreement happened; a Python-side label (`format_bytes` filter) — rejected, two of the
  three surfaces are painted client-side from companion payloads.
- **Provenance**: research.

## Open

<!-- empty when Phase 0 is finished; anything here blocks Phase 1 -->
