# Fold: Audio and video name their play/pause key

**Capabilities touched**: `projector`
**File**: `docs/spec/projector.md`

## Operations

| Operation | Target | Detail |
| --- | --- | --- |
| added | `projector/R12` | *The shortcuts sheet names audio and video in groups of their own* — the two headings, one `Play/Pause` row on the Space chord each, the middle column's end, `Display`'s three remaining rows, the sheet's fixed height, and Space's unchanged meaning, with three scenarios (sheet opened, 1280×720 window, Space with media showing) |
| modified | header | `last folded` 2026-10-26 → 2026-10-29; `slices` prepended with `160-shortcuts-audio-video-groups` |

No requirement was removed or renamed, and `R1`–`R11` are untouched.

**Identifier note.** The requirement was planned and accepted as `projector/R3`. The rebase onto develop
1.25.0 found `R3`–`R11` claimed by later slices (`R3` is the image placeholder, spec 157), so the
requirement is folded as **`R12`**; every artifact carries the new ID, and `converge.md` pass 2 records
the rename.

## Counts

| | Before | After |
| --- | --- | --- |
| requirements in `projector.md` | 11 | 12 |
| scenarios in the file | 39 | 42 |

Counted on the file as develop holds it at the rebase: `R1`–`R11` before this fold.

## Not folded

- The keys' own behaviour (FR-006, US2, SC-004) was an accepted gap because its four E2E cases were
  deferred to the push step. **The gap closed there**: the four cases ran green on the rebased tree
  (converge pass 2, 2026-10-30). Nothing about that behaviour changed, and `R12` states what the
  sheet says about it.
