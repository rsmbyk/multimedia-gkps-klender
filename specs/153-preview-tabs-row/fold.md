# Fold: the preview's verse tabs get their own row

**Spec**: `specs/153-preview-tabs-row/spec.md` · **Folded**: 2026-10-29

## Capabilities touched

| Capability | Operation | Requirement |
| --- | --- | --- |
| `reading` | added | `R27` — the preview's header gives a song's verse tabs a row of their own |

## Counts

- `docs/spec/reading.md`: 26 → 27 requirements.
- Header: `last folded` 2026-10-28 → 2026-10-29; `153-preview-tabs-row` prepended to the slice list.

## Notes

- The preview's identity header (spec 085) was never folded — it shipped before this file started at spec
  126 — so R27 states the header as a whole: the title band, the tab band, the single rule, and the focus.
  It supersedes nothing in this file.
- No behaviour changed outside `reading`; no other capability was read, and none was touched.
- Two behaviours were folded that the spec states as assumptions rather than as FRs: the titled band's
  rule falling under the tab band, and a pointer open painting no ring. Both are visible states of R27 and
  were accepted at gate 1.
