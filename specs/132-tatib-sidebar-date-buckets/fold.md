# Fold — the Tata Ibadah list groups by age

**Slice**: `specs/132-tatib-sidebar-date-buckets/`
**Folded**: 2026-10-25
**Capability touched**: `reading` (`docs/spec/reading.md`)

## Operations

| Operation | Requirement | What was written |
| --- | --- | --- |
| `added` | `R9` | The Tata Ibadah list groups by age, and today is marked — the four buckets, the boundary rule, the `Asia/Jakarta` day, the today-first order inside `Upcoming`, the `Today` badge, the dock's parity and the removal of its tints, the saved copy's parity, the `data-bucket` key, the filter across buckets, and template mode unchanged, with eight scenarios |

## Counts

- `reading`: 8 requirements → **9** (`R1`–`R9`); `R9` is new, nothing renamed, nothing removed.
- Slices recorded on the capability: 6 → 7.
- `last folded`: unchanged at 2026-10-25 (the previous fold and this one share the date).

## Not folded — accepted gaps

The saved-copy rows of `R9` are verified by browser suites that run at the push step (`analysis.md`
A-002). The behaviour is folded because it converged and the requirement is the approved behaviour; what
is deferred is the run, not the claim. `converge.md` records the same, and `tasks.md` T017/T020 name the
two suites.

## Refactor check

Not a refactor: the panel's grouping changed from month to age, the dock's tints were removed, and a badge
was added. The behaviour delta is the whole slice.
