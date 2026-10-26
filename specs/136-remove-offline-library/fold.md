# Fold — remove the offline library; the projector fetches on selection

**Slice**: `specs/136-remove-offline-library` · **Date**: 2026-10-26 · **Capabilities touched**:
`reading` (removals and one modification), `projector` (created)

## `reading`

| Operation | Requirement | Before | After |
| --- | --- | --- | --- |
| `removed` | R2 — A saved reading page shows its server route's header and title | 1 statement, 3 scenarios | heading kept, marked removed 2026-10-26 with its reason |
| `modified` | R3 — The tab names the site | 4 scenarios, one of them the saved copy | 3 scenarios; the saved-copy scenario is gone |
| `removed` | R5 — A saved Kidung panel draws the same two groups | 1 statement, 1 scenario | heading kept, marked removed 2026-10-26 with its reason |
| `modified` | file description | "…and what the saved copy of a page must show before the online update replaces it" | "Every page is painted from its own server response; the saved-copy requirements … are retired" |
| `modified` | header `slices` | 10 slice ids | `136-remove-offline-library` prepended |

`R2` and `R5` keep their numbers: a requirement number is never reused, and a removal stays visible
with its reason.

## `projector` (created)

| Operation | Requirement |
| --- | --- |
| `added` | R1 — The Go To searches a page-memory index and fetches the content it paints (5 scenarios) |
| `added` | R2 — The projector page renders from its own response alone (2 scenarios) |

The capability did not exist before this slice: the projector's behaviour (specs 006, 091, 119)
shipped before the capability tree began, and the Go To's search rules were never written down. The
two requirements above record what this slice established; earlier projector behaviour folds as a
later slice touches it.

## Counts

- `reading`: 12 requirements before, 12 after — 2 marked removed, 1 modified, 0 added.
- `projector`: 0 → 2.
- No behaviour changed without a delta; the two files' bodies were written from the spec's
  requirements and the converged code.
