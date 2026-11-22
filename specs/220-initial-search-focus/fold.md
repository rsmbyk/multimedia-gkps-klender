# Fold: the empty search landing is ready for typing

**Slice**: `specs/220-initial-search-focus` · **Date**: 2026-11-22

## Capabilities touched

- `reading` — one requirement added (`R50`, four scenarios). `R15` unchanged, see C1.

## Operations

| Operation | Requirement | Note |
| --- | --- | --- |
| `added` | `reading/R50` — The empty search landing is ready for typing | full block with scenarios: the landing is a state rather than a route, focus changes neither value nor selection nor scroll, the existing focus ring, and the pages that must not take focus |

## C1 — `R15` was not modified, and the spec's capability line said it would be

Spec 220's capability line reads "modifies `reading/R15` (focus clause only) and adds `reading/R50`".
`R15` carries no focus clause to modify. `specs/139-home-search-center/fold.md` maps that slice's
FR-006 — "no transition, no scroll of the page itself, and no focus change on load" — onto `R15`'s
*"views that are not the landing"* geometry paragraph, so the focus half of that requirement never
entered the capability tree; it exists only in `specs/139-home-search-center/spec.md`.

Nothing in `R15` therefore needs superseding, and none of its sentences were touched: the centring,
the 96px logo, the one-window-tall rule, the phone paddings and the results/reading exclusions all
stand as folded on 2026-10-27. The behaviour is identical either way — the supersession was already
recorded against spec 139's own `spec.md` in `specs/220-initial-search-focus/spec.md`
§Clarifications.

Recorded here rather than corrected in the spec because a spec is `Draft` or `Accepted` and never
changes after Gate 1 (BRD-09). It is a bookkeeping discrepancy, not a behaviour change.

## Counts

| | Before | After |
| --- | --- | --- |
| Requirement blocks in `reading` | 49 (`R1`–`R49`) | 50 (`R1`–`R50`) |
| Live requirements | 48 (`R2` retired in place) | 49 |
| Scenarios in `R50` | — | 4 |

The header moves `last folded` to 2026-11-22 and `220-initial-search-focus` is prepended to the slice
list.

## Not folded — accepted gaps

None.