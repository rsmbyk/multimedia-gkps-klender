# Fold: on a small screen the sidebars are a drawer stack over the page

**Slice**: `specs/138-sidebar-overlay-stack` · **Date**: 2026-10-27

## Capabilities touched

- `reading` — one requirement added.

## Operations

| Operation | Requirement | Note |
| --- | --- | --- |
| `added` | `reading/R14` — Below 1272px the sidebars are drawers over the page; below 720px a toolbar carries them | full block with seven scenarios |

## Counts

| | Before | After |
| --- | --- | --- |
| Live requirements in `reading` | 12 (`R1`, `R3`–`R13`; `R2` is retired in place) | 13 (`R1`, `R3`–`R14`) |
| Scenarios in `R14` | — | 7 |

`R1`–`R13` are untouched. The header's `last folded` stays at 2026-10-27 (the same day) and
`138-sidebar-overlay-stack` was prepended to the slice list.

## Not folded — accepted gaps

- The three inspection rows in `plan.md` — the search landing, an empty second level, and a modal
  above the stack — are checks, not requirements: nothing in `R14` promises them beyond "the shell
  keeps its other layers", which `R10`/`R11` already hold.
- `C2` in `converge.md` (the phone boots into the page rather than into a drawer) is worth its own
  sentence in the requirement one day; today it is the practical reading of "a drawer is an action",
  and the specification's US1–US5 do not state a boot state.
