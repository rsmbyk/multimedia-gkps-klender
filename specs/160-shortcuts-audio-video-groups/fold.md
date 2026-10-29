# Fold: Audio and video name their play/pause key

**Capabilities touched**: `projector`
**File**: `docs/spec/projector.md`

## Operations

| Operation | Target | Detail |
| --- | --- | --- |
| added | `projector/R3` | *The shortcuts sheet names audio and video in groups of their own* — the two headings, one `Play/Pause` row on the Space chord each, the middle column, `Display`'s three remaining rows, the sheet's fixed height, and Space's unchanged meaning, with three scenarios (sheet opened, 1280×720 window, Space with media showing) |
| modified | header | `last folded` 2026-10-26 → 2026-10-29; `slices` prepended with `160-shortcuts-audio-video-groups` |

No requirement was removed or renamed, and `R1`/`R2` are untouched.

## Counts

| | Before | After |
| --- | --- | --- |
| requirements in `projector.md` | 2 | 3 |
| scenarios in the file | 6 | 9 |

## Not folded — accepted gap

- The keys' own behaviour (FR-006, US2, SC-004) is asserted by four E2E cases that this slice does not
  run; they are deferred to the push step. Nothing about that behaviour changed, and `R3` states what
  the sheet says about it.
