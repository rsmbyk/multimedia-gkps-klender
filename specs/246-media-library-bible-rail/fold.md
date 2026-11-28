# Fold — spec 246

**Date**: 2026-11-27
**Slice**: `246-media-library-bible-rail`
**Branch**: `fix/246-media-library-bible-rail`
**Convergence**: pass 1, no accepted gaps

## Capabilities touched

| Capability | Operations | Requirement count |
| --- | --- | --- |
| `reading` | `added: R63` | 62 → 63 |

No requirement was modified, removed or renamed. `R62` keeps its rail-fetch pending-state rules.

## Header delta

- `last folded`: 2026-11-26 → 2026-11-27
- `slices`: `246-media-library-bible-rail` prepended

## Delivery state

- `VERSION`: 1.37.3 → 1.37.4; one `### Fixed` line under `## [Unreleased]`.
- `ITEM-263`: anchor issue #635; board row moved to `In progress` with the slice branch. No PR or
  push has been made — the card closes when the PR lands, on the owner's word.
- PR title and body prepared in `pr-body.md`; no remote branch update.

## Verification carried into the commit

- `tests.e2e.test_media_library_bible_rail` — 2 tests, red on the base view and green with the fix.
- `tests.e2e.test_navigation_pending` — 24 tests green in the same targeted run (26 total).
- `preview/probe.py` and `preview/manual_probes.py` — gate-1 numbers and manual states.
- Verification split from Plan: 9 test · 5 inspection · 4 manual; Converge pass 1 covered 18/18 rows.
