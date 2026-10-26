# Fold — Keep reading views current after sidebar edits

**Slice**: `specs/134-sidebar-save-freshness/`
**Folded**: 2026-10-26
**Capability touched**: `reading` (`docs/spec/reading.md`)

## Operations

| Operation | Requirement | What was written |
| --- | --- | --- |
| `added` | `R11` | A sidebar edit keeps every visible reading view current — the successful save of a Tata Ibadah, songbook or song refreshes its row, the stage that shows it and any open search results and group counts in place, on the same route; the query, selection, pane states, filters, scroll and focus survive; an unrelated stage keeps its content and route; the tab stays the title the refreshed route renders (`R1`, `R3`); a rejected save changes nothing and an entry save keeps its in-place refresh — with eight scenarios |

## Counts

- `reading`: 10 requirements → **11** (`R1`–`R11`); `R11` is new, nothing renamed, nothing removed.
- Slices recorded on the capability: 8 → 9 (`134-sidebar-save-freshness` prepended).
- `last folded`: 2026-10-25 → **2026-10-26**.

## Not folded — accepted gaps

None. Pass 1 converged with no `missing`, `partial` or `unrequested` gap. The single `contradicts` was
spec-side — US1/AC2 asked for a saved song title in the tab against `R1` — and the owner settled it by
keeping `R1` and amending the scenario; `converge.md` records the decision.

## Refactor check

A behaviour change, not a refactor: the shared save refresh now reconciles both sidebar columns and the
stage from one server response instead of rebuilding only the stage, and search refreshes re-request the
current query. The offline saved-copy paint reuses that same branch and was given
`backgroundRefresh: true` so it still leaves the operator's shell alone; the delete path keeps its own
focus hand-off through `deferFocus`.

## Idempotence

Re-applying this fold (the header move and the `R11` block, guarded on the block's title) leaves the file
byte-identical: `sha256 bfd48ca296200ab0e0a1aedfdca506c83a220c4004ff5be7f33308884449d325` before and after.
