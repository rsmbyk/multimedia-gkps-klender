# Fold: a preview's play shortcut paints nothing on the dialog's edge

**Spec**: `specs/159-preview-body-ring/spec.md` · **Capabilities touched**: `reading` · **Date**: 2026-10-29

## Operations

| Operation | Capability | Requirement |
| --- | --- | --- |
| **added** | `reading` | `R31` — A preview's play shortcut leaves no focus ring on the dialog |

No requirement was modified, removed or renamed. R31 is new because no capability file covered the
Preview dialog's focus ring: spec 071, which introduced it, predates the capability tree (which starts
at spec 126), and this slice is the first to touch it since.

## Before / after

| | before | after |
| --- | --- | --- |
| requirements in `docs/spec/reading.md` | 30 (R1–R30) | 31 (R1–R31) |
| header `last folded` | 2026-10-29 | 2026-10-29 |
| header `slices` | 26 entries, first `162-song-verse-empty-state` | 27 entries, first `159-preview-body-ring` |

## Accepted gaps

None folded short: the two `manual` rows in `converge.md` (SC-001, SC-004) verify the shipped behaviour,
they do not change what R31 says, so R31 folds whole. Their result is recorded in the closing report
after the merge.

## Idempotence

Re-running this fold would find `R31` already present with the same text and the header already naming
`159-preview-body-ring`; it changes nothing.
