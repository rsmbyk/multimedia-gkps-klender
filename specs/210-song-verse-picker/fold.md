# Fold: the song entry's pickers

**Date**: 2026-11-21
**Slice**: `specs/210-song-verse-picker`
**Capability touched**: `reading`

## Operations

| Requirement | Operation | Detail |
| --- | --- | --- |
| `reading/R30` | `modified` | Complete replacement block; the Verses section, label included, is hidden for no song and for a no-verses song instead of keeping a disabled trigger. The superseded wording is kept inline as a retraction. All seven original scenarios are retained with their outcomes updated. |
| `reading/R43` | `modified` | The summary now collapses consecutive numbers into ranges. IDs, `{id, number}` payload and the refusal are unchanged; the old comma-list wording is kept inline as superseded. |
| `reading/R48` | `added` | New block: live song search from the first frame, viewport-capped overlay that may pass the dialog edge, inline Verses section in a 1px-bordered rail-surface panel, five equal-width tiles with the helper/All/Clear row above the grid, drag preview in the summary line with commit on release, All/Clear end states, one-verse muting and the single reduced-motion-aware reveal. The verse widget gained its own templates so a server-rendered checklist (Edit, or an Add form returned by a refused save) is already that same five-across grid. Four scenarios. |

## Counts

- Rules before: 47 (`R1`–`R47`, including specs 209 and 212 folded after this slice was cut).
- Rules after: 48 (`R1`–`R48`); the number moved from R47 to R48 when spec 212's copy-confirmation
  block took R47 on `develop` first. No number reused.
- Scenarios: R30 7 → 7, R43 3 → 3, R48 0 → 4.
- Header: `last folded` 2026-11-19 → 2026-11-21; slice list prepended with `210-song-verse-picker`.

## Not folded

- `VERSION`, `CHANGELOG.md` and the board card are delivery bookkeeping (task T021), not capability
  facts: `VERSION` 1.35.4 (1.35.3 was taken by spec 212 before this branch merged `develop`), the
  changelog entry under `[Unreleased]`, and card `ITEM-227` closed in the same PR (renumbered from ITEM-225,
  which sat below `develop`'s highest card).
- The preview's sample songs, the `Slow` review control and tabs 2–4 are comparison artifacts; they
  describe no product behavior and are not folded.
