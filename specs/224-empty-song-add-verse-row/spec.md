# Feature Specification: An empty song paints one Add verse control

**Slice**: `specs/224-empty-song-add-verse-row`
**Branch**: `fix/224-empty-song-add-verse-row`
**Created**: 2026-11-23
**Status**: Draft
**Input**: "when a song has no verses, hide the 'Add verse' button that appears after the last verse in normal state"
**Demand**: `ITEM-239`
**Capability**: modifies `reading/R40`

## User Scenarios & Testing

### US1 — An empty song offers Add verse once (P1)

**Why this priority**: on a song with no verses the stage currently draws two identical
`Add verse` buttons — one in the normal after-the-last-verse row with no verse above it, and
one inside the empty invitation. A reader cannot tell which is the real action, and the stray
row sits between the song title and the invitation that already explains the empty state.

**Independent Test**: open `/songs/1731/` (an ordinary song with no live verses) and count the
`[data-add-verse]` buttons: exactly one, inside `.entry__empty`; there is no `.verse-add` row.

**Acceptance scenarios**

1. **Given** an ordinary editable song with no live verses **When** its page opens **Then**
   the stage shows exactly one `Add verse` button, the one inside the empty invitation, with
   no `.verse-add` row above it.
2. **Given** that empty song **When** the reader uses the invitation's button to save the
   first verse **Then** the verse is numbered `1`, the invitation goes away, and the single
   `.verse-add` row appears after it — all without a reload.
3. **Given** an ordinary song with verses **When** its page opens **Then** its one `.verse-add`
   row still follows the last verse at the same position and size, and no empty invitation
   is drawn.
4. **Given** a hymn song or a restricted reader **When** any song page opens **Then** no
   verse control is drawn in either state; this slice changes no permission rule.
5. **Given** a song whose only verses are soft-deleted **When** its page opens **Then** it
   reads as empty, shows the invitation's one button, and draws no after-the-last-verse row.

### US2 — The empty invitation sits at the Tata Ibadah empty-state height (P1)

**Why this priority**: the owner added it while reviewing gate 2. Once the stray row is hidden the
song invitation rises to y=153.9, further from the Tata Ibadah invitation at y=253.5 than before.
Both empty states should occupy the same vertical band of the reading area.

**Independent Test**: at 1440×900 open `/songs/1731/` and `/tatib/145/` and compare the top of
`.entry__empty-title` on each: 253.9px and 253.5px — a 0.4px difference.

**Acceptance scenarios**

1. **Given** an ordinary song with no verses **When** its page opens at 1440×900 **Then** the
   invitation's title top is within 1px of the Tata Ibadah empty title's top on the same viewport.
2. **Given** the same two pages at 900×700 **When** measured **Then** the same within-1px relation
   holds (199.0px against 198.6px).
3. **Given** a song with verses **When** its page opens **Then** nothing about its verse rows or
   after-the-last-verse row changes; the new placement applies only to the empty state.
4. **Given** the empty invitation at 390×844 **When** compared with Tata Ibadah **Then** it uses the
   same quarter-band mechanism, with a recorded 5.5px residual from the longer song title wrapping
   to a taller header (240.4px against 234.9px).

### Edge Cases

- `verse_rows` comes from `song.verse_set.filter(is_deleted=False)`, so "no verses" means no
  *live* verses, not an empty `verse_set`.
- The two controls are byte-identical markup with the same `data-song` pointer; only their
  container differs. Removing the stray row must not change the surviving button's box.
- The stray row's `margin: 14px 0 0` collapses through `.read__body`, so removing it also
  raises the invitation by the row's 38px plus that 14px; the invitation's own box is unchanged.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | `multimedia/web/templates/reading/song.html` SHALL draw the `.verse-add` row only when `can_edit_verses` and at least one live `verse_rows` entry exist. | `reading/R40` |
| FR-002 | A song with no live verses SHALL draw exactly one `Add verse` control, inside the unchanged `.entry__empty` invitation. | `reading/R40` |
| FR-003 | A song with live verses SHALL keep the existing `.verse-add` row after the last verse, with identical markup, geometry and behaviour. | `reading/R40` |
| FR-004 | The empty invitation's copy, its button box, the verse verbs, the write endpoints and the hymn/restriction guards SHALL be unchanged. | `reading/R40` |
| FR-005 | `reading/R40` SHALL state the new gate explicitly: one add control after the last verse only when a last verse exists. | `reading/R40` |
| FR-006 | An empty song page SHALL place `.entry__empty` in the same quarter-band arrangement as an empty Tata Ibadah page, by the same flex/grid mechanism, with the song invitation title's top within 1px of the Tata Ibadah title's top at 1440×900 and 900×700. | `reading/R40` |

### Key Entities

None. The change is one template gate over `verse_rows` and `can_edit_verses`, two context
values already supplied by `SongDetailView`.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | An empty song page has one `[data-add-verse]` button and no `.verse-add` row. | Playwright count on `/songs/1731/`: `1` and `0`. |
| SC-002 | A song with verses keeps one add row in the same box. | Playwright box on `/songs/1387/`: 520×38 at x=856, y=681.3, button 111.8×38 at x=900. |
| SC-003 | The surviving empty-state button does not move. | Playwright box before/after: 111.8×38 at x=1060.1 in both states; only its y follows the invitation's raised box. |
| SC-004 | The first-save path still works from the invitation. | Existing verse write tests plus one browser save from the empty state. |
| SC-005 | The empty titles share a vertical position. | Playwright at 1440×900: song title top 253.9px, Tata Ibadah 253.5px, Δ0.4px; at 900×700 Δ0.4px; at 390×844 Δ5.5px recorded, not held to 1px. |

## UI/UX

`static preview at specs/224-empty-song-add-verse-row/preview/index.html` — the live song
page's real markup and stylesheet, with four captured states on one switcher: **empty — placed
(proposed, default)**, **empty — gate only**, **empty — before (current)** and **three verses
(unchanged)**. The gate-only state is the current empty fragment with exactly the `.verse-add`
row removed; the placed state adds the candidate quarter-band CSS that the Tata Ibadah empty state
already uses. Live comparisons: `http://127.0.0.1:8770/songs/1731/`, `/songs/1387/` and
`/tatib/145/`; harnesses are `preview/serve.sh`, `preview/build.py` and `preview/probe.py`. The
static page cannot exercise server rendering or the save verbs; those are checked live.

- **Before (measured, live, 1440×900)**: 2 `[data-add-verse]` buttons. Stray `.verse-add` row
  520×38 at x=856, y=167.9, its button 111.8×38 at x=900, y=167.9. Empty invitation 520×128
  at x=856, y=205.9, its button 111.8×38 at x=1060.1, y=295.9; title top y=205.9.
- **Gate only (measured, static preview)**: 1 `[data-add-verse]` button, 111.8×38 at x=1060.1,
  y=243.9, inside the same 520×128 invitation, now at x=856, y=153.9 — raised 52px by the
  removed row and its collapsed 14px top margin; title top y=153.9.
- **Placed (proposed, measured in the static preview and in a live CSS probe)**: 1 button,
  title top y=254.0 in the preview / y=253.9 in the live probe, against the Tata Ibadah title's
  y=253.5 on `/tatib/145/` — a 0.4px gap. The mechanism mirrors
  `components.css:2503-2522` on `.read[data-kind="song"]:has(.entry__empty)`: flex the article
  to the stage height, grid the body in one 50% band, centre the block in it, and set
  `padding-top: 0` for this state.
- **With verses (unchanged, live)**: 1 button, `.verse-add` row 520×38 at x=856, y=681.3,
  button at x=900, y=681.3; three `p.v` rows above it.
- **States**: empty and with-verses; hover and focus styles of the surviving button are the
  product's existing `.verse-add__btn` rules, untouched.
- **Colour / typography / motion**: unchanged — no token, font or transition is added.
- **Responsive**: at 900×700 the two empty titles land at y=199.0 and y=198.6 (Δ0.4px); at
  390×844 they land at y=240.4 and y=234.9 (Δ5.5px) because the longer song title wraps to a
  taller header. The row's existing 420px rule is untouched; the gate does not depend on width.

## Assumptions

- The invitation's button is the one to keep: it sits with the explanation of the empty state,
  while the after-the-last-verse row has no verse to follow. The request names only the row.
- No Clarify question was needed for the duplicate row: the request pinpointed one control and the
  alternative is already in the page's own empty-state copy. The placement request came while gate 2
  was open; the owner chose to add it as US2 in this slice, so gate 1 re-opens on the revised preview.
- Exact sub-pixel equality is claimed only at 1440×900 and 900×700 (within 1px); the 390×844 residual
  of 5.5px is recorded, not held as a criterion, because the song's longer title wraps to a taller
  header than the Tata Ibadah page's.
- The preview is static because the visible differences are markup and CSS the server already
  fetched; the live routes supply the before measurement and the post-implementation readout.
