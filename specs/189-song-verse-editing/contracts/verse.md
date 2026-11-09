# Verse HTTP contracts (spec 189)

**Spec**: `specs/189-song-verse-editing/spec.md` · **Capability**: `reading/R40` (new)

All endpoints require authentication where editing restricted (`SIDEBAR_EDITORS_REQUIRE_LOGIN` on, anonymous → 403 without writing). Hymn-book songs → refused (FR-001).

## POST /editor/verse/new/save/

- **Body**: `song` (pk, ordinary book, live), `lyric` (non-blank).
- **Effect**: append verse, `number = max live number + 1`; live set stays 1…n (FR-003, FR-012).
- **Response**: success. Browser re-reads the song page without reload.
- **Failure**: blank lyric → field error, modal stays open, nothing written; stale/concurrent add → whole refusal + re-read.

## POST /editor/verse/<pk>/save/

- **Body**: `lyric` (non-blank).
- **Effect**: replaces only that verse's lyric. Number, title, book, same song's other verses untouched (FR-005).

## POST /editor/verse/<pk>/delete/

- **Guard**: refuses when any `ServiceEntry.verses` contains the verse id; modal disables beforehand and states count (FR-010).
- **Effect**: soft-delete, renumber remainder 1…n, re-read (FR-011).

## POST /editor/verse/reorder/

- **Body**: `song`, `ordered_ids` (full permutation of live verse IDs).
- **Effect**: renumber live rows 1…n in that order; page shows new numbers without reload (FR-007).
- **Failure**: membership mismatch (added/removed elsewhere) → whole refusal, nothing renumbered, re-read.

## GET /editor/entry/song/<pk>/verses/ (picker)

- **Returns**: per live verse: `value = id`, `label = current number`.
- **Consumers**: entry form, summary line (`Verses 1, 3` / `All verses`), stage `Bait …` line, projector — one reading of `verses` (FR-008, FR-016).

## Effective read (not a wire contract)

A service entry resolves to `Verse.objects.filter(pk__in=verses, is_deleted=False).order_by('number')`: body = each lyric, label = each current number. Unchanged lyric set across reorder is the acceptance check (SC-003).
