# Research: the song entry's pickers

**Spec**: `specs/210-song-verse-picker/spec.md`
**Unknowns remaining**: 0

## D001 — Song search is live from the first frame, in a fixed overlay

- **Decision**: Focus the Song search input when the form renders; keep the existing
  viewport-capped fixed menu (`placeMenu`) as the results surface, with no 268px dialog-bound cap.
- **Rationale**: the owner asked to "directly type to search the song as the song entry modal
  opens", and asked that results be allowed past the modal height. The approved preview measured
  a constant 516px dialog with 11, 3 and 0 results; the overlay reached y=892 against the
  dialog's y=885 at 960×900.
- **Alternatives considered**: in-flow results under the field (measured 790/662/572px dialog
  heights — rejected); a full value-help dialog (SAP Fiori recommends it above 200 items, but
  this picker is already capped at 200 and lives inside an editor modal); a typed-only command
  field (loses browsing).
- **Provenance**: owner decision; research (`W3C ARIA listbox`, `SAP value help`,
  `ogblocks multi-select comparison`) confirms the keyboard model and the chip/token pattern.

## D002 — Verse numbers become five-across tiles with native values underneath

- **Decision**: Replace the verse checkbox dropdown with a 40px tile grid, five per row, and
  keep hidden `input[name=verses]` elements carrying verse IDs.
- **Rationale**: the owner named the checklist a hassle; the tile grid makes a single verse a
  large target while the hidden inputs preserve the storage contract of `reading/R43`.
- **Alternatives considered**: From/To chips and typed `1-3,5` notation (preview tabs 2 and 3 —
  fast for power users but a new syntax), enlarged checkboxes (tab 4 — smallest change but
  still a dropdown of small targets). All three stay in the preview as comparison only.
- **Provenance**: owner decision from the preview review; `reading/R43`, specs 189 and 195.

## D003 — Range extension is a held drag that previews until release

- **Decision**: A plain click ticks one tile; holding on a tile and dragging across others
  tints the whole stretch and reads `Preview: verses a–b · release to keep`. Nothing is written
  to the form until pointer release, and no anchor mark persists afterwards.
- **Rationale**: the owner explicitly asked not to finalize before release and said the mark
  is no longer needed once the range is final.
- **Alternatives considered**: Shift+click (the first preview) and keyboard Shift+Arrow (kept
  only as the pointerless equivalent, never the advertised gesture).
- **Provenance**: owner decision; pointer events keep touch parity.

## D004 — No-verses hides the section; one verse mutes it

- **Decision**: With no song, or a song with zero live verses, the whole Verses section
  collapses to 0px in the server-rendered fragment. A one-verse song shows one inert tile at
  0.45 opacity.
- **Rationale**: the owner asked twice, first to remove the tick boxes and then to hide the
  section outright; an empty control cannot act.
- **Alternatives considered**: keeping the disabled trigger with `This song has no verses`
  (`reading/R30`'s current wording) — modified by this slice and recorded as such.
- **Provenance**: owner decision; supersedes the disabled-field clause of `reading/R30`.

## D005 — Numbering

- **Decision**: spec 210 / branch `feat/210-song-verse-picker`; capability requirement
  `reading/R48`; `reading/R30` and `reading/R43` are modified, not duplicated.
- **Rationale**: branch names, worktree spec folders and every `docs/spec/reading.md` were
  checked; 209 holds R46 and 210 was free across all worktrees and branches.
- **Alternatives considered**: reusing 209 or an unclaimed 211 — rejected because 209 belongs
  to another slice and consecutive numbers are required.
- **Provenance**: repository inspection.

## D006 — Backend stays byte-identical

- **Decision**: No change to `entry_song_options`, `entry_song_verses`, query grammar, ordering,
  labels, 200 cap, forms or models.
- **Rationale**: the accepted search specs 042/050/051 and the verse-ID contract of 189/195
  already govern these; the owner's complaint is about the picker's surface and gesture only.
- **Alternatives considered**: rewriting the query for the new surface — rejected as an
  unrequested behavior change with a large regression surface.
- **Provenance**: repository inspection; existing accepted specs.

## Open

<!-- empty when Phase 0 is finished; anything here blocks Phase 1 -->
