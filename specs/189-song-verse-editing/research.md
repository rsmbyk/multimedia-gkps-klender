# Research: song verse editing on the song page

**Spec**: `specs/189-song-verse-editing/spec.md`
**Unknowns remaining**: 0

## D001 — References hold IDs, not current numbers

- **Decision**: `ServiceEntry.verses` stores verse primary keys; display resolves each to the verse's current `number` (`pk__in`, ordered by `number`). Reorder renumbers rows, references do not move.
- **Rationale**: Live measurement on local library: 448 entries × ordinary songs, migration mapping each stored number to the same-number live verse covers all (0 rows with no live verse). Number-as-identity breaks the moment reorder renumbers.
- **Alternatives considered**: Keep numbers and refuse reorder for referenced verses; keep numbers and accept silent repointing. Both rejected — owner ruled the reference names a lyric, and reorder must remain usable.
- **Provenance**: Research measured on dev DB; owner decision 2026-11-05 recorded in spec Clarifications.

## D002 — One editor modal, `verse` as a fourth kind

- **Decision**: Reuse the spec 005 shared `<dialog>` with `verse` kind; one fetch-and-revalidate path, one toast, one focus restore.
- **Rationale**: The modal already handles hymn refusal, CSRF, toast and focus. A second modal duplicates every behaviour. Verified existing dialog is 480×352.3 at (480,273.9) in preview.
- **Alternatives considered**: New dedicated dialog (duplicate behaviour); inline editing (layout churn, lyric column moves). Rejected.
- **Provenance**: Research — read `entries.js` delete pattern and spec 133 large frame already used for Edit.

## D003 — Reorder feels like the service sidebar: ghost + frozen midpoints

- **Decision**: Port `static/web/reorder.js` shape: ghost clone rides the pointer 1:1, real row stays as tinted placeholder with hidden contents, others FLIP 160ms rest / 60ms mid-drag, frozen grab midpoints (`static/web/reorder.js` `placeRowAt`), 3px dead zone before the gesture starts.
- **Rationale**: Owner contrasted slotted card (discrete jumps that read snappy) with sidebar (continuous ghost). Frozen mids measured stall-free in sidebar; measured `indexFollowsTravel` 14/14, `reversals` 0, `seamsOk` true in static preview. Live-reflowed goalposts measured stalling ("one short of release").
- **Alternatives considered**: Parked card in slot (feels snappy); live re-measured midpoints (stall + seam drift); absolute-travel anchoring (origin-based, rejected 2026-11-09 as "moves on original position"). Live-cursor frozen-gap check retained: slot = first frozen middle the current cursor has not passed.
- **Provenance**: Owner decision 2026-11-09 for live cursor; owner decision 2026-11-09 for sidebar-feel (ghost + frozen).

## D004 — B grab-collapse beats A reorder mode

- **Decision**: Grab a grip anywhere collapses the 44px list for the gesture only, no header button, no mode. `Reorder verses` exists in preview only as the rejected A comparison.
- **Rationale**: Owner decision 2026-11-06: the mode asks the reader to leave the page to change it; a gesture that begins where verses are and ends by itself does not. Cost recorded: reading view changes under pointer.
- **Alternatives considered**: Mode A (button + hint stayed until Done). Built, measured, rejected.
- **Provenance**: Owner decision 2026-11-06; static preview comparison state bar.

## D005 — Migration shape and soft-delete interaction

- **Decision**: One data migration maps each stored number to the live verse with the same number; numbers naming no live verse dropped. Narrow `unique_together` on Verse to live rows (with partial index/condition or app-level unique check on live set) so renumbering into a soft-deleted number cannot clash.
- **Rationale**: `songs.Verse.unique_together = ['song','number']` covers deleted rows too (current `models.py`); renumber would collide with tombstones. Live data shows 1,655 ordinary verses named by ≥1 entry, 829 setlist items left untouched per owner.
- **Alternatives considered**: Delete tombstones; allow duplicates and dedupe by `is_deleted`. Tombstone deletion loses audit; duplicates break `unique_together`. Partial unique on live rows is simplest.
- **Provenance**: Research — read `songs/models.py`, `tatib/models.py`, entry picker at `entries.py:125-143`, `views.py` `number__in` sites.

## D006 — No keyboard handler for reorder, drag-only

- **Decision**: Pointer-only grip; no arrows, no mode, no keyboard move. Departure from Tata Ibadah grip grammar deliberate.
- **Rationale**: Owner decision in Clarify; spec 189 preference for gesture-only. Keyboard user cost recorded as assumption, not hidden.
- **Alternatives considered**: Reuse sidebar arrow-key grammar (`moveBy`). Owner rejected.
- **Provenance**: Owner decision in spec Clarifications.

## Open

