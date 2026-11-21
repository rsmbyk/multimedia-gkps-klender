# Fold: a contents row marks its entry's kind

**Date**: 2026-11-21
**Slice**: `specs/214-sidebar-entry-kind-marks`

## Capabilities touched

| Capability | Operation | Requirement |
| --- | --- | --- |
| `reading` | added | R49 — A contents row states its entry's kind in a column after the number |

## Operations

- **added**: R49 with four scenarios, folded from FR-001…FR-008, SC-001…SC-006 and the two owner
  decisions (layout B; the slot kind modifier).
- No requirement was modified or removed. Spec 144 FR-008 and spec 213's sidebar exclusion are
  reversed for `#chList` only; neither was folded as a requirement, because neither capability file
  carried that exclusion — R25 speaks of the stage, R35 of a template's slot mark.
- The break row's skipped question is recorded as an assumption in the spec and as a negated clause in
  R49; nothing is left ambiguous.

## Counts

| | before | after |
| --- | --- | --- |
| `reading` requirements | 48 (R1–R48) | 49 (R1–R49) |
| `reading` scenarios | — | +4 |
| slices listed in `docs/spec/reading.md` | 43 | 44 |

## Not folded — pre-existing known red

- Two `test_text_wrap` assertions (ITEM-184), three slot-endpoint unit tests and the legacy tatib
  payload, image/video projection, rendered-voices and shortcuts-sheet tests (ITEM-217), and the
  untagged companion-page E2E class. Each fails identically on unmodified `origin/develop`; none is
  a behaviour change from this slice.

## Board

- ITEM-230 (renumbered from ITEM-229 after spec 215 took that id; anchor issue #565 retitled) moves
  from `Speccing` to `In progress`. It moves to `In review` on the push, and to `Done` before the merge.
