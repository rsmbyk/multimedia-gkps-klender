# Fold: a reading page's text wraps at its pane

**Slice**: `specs/137-reading-text-wrap` · **Date**: 2026-10-27

## Capabilities touched

- `reading` — one requirement added.

## Operations

| Operation | Requirement | Note |
| --- | --- | --- |
| `added` | `reading/R13` — A reading page's text wraps at its pane | full block with six scenarios |

## Counts

| | Before | After |
| --- | --- | --- |
| Live requirements in `reading` | 11 (`R1`, `R3`–`R12`; `R2` is retired in place) | 12 (`R1`, `R3`–`R13`) |
| Scenarios in `R13` | — | 6 |

`R1`–`R12` are untouched. The header's `last folded` moved to 2026-10-27 and
`137-reading-text-wrap` was prepended to the slice list.

## Not folded — accepted gaps

None. C2 in `converge.md` is a reading of FR-007's wording for the owner to confirm, not a
behaviour left out of the capability; the scenario it settles — *text that fits* — is folded.
