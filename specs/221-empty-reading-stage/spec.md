# Feature Specification: An empty reading stage after deleting the open record

**Slice**: `specs/221-empty-reading-stage`
**Branch**: `fix/221-empty-reading-stage`
**Created**: 2026-11-22
**Status**: Draft
**Input**: "when you delete a song or service, and that song or service is being opened in reading page, it should not display the search page in reading page. instead, display an empty reading view"
**Demand**: `ITEM-236`
**Capability**: modifies `reading/R41` (the on-stage delete landing clause)

## User Scenarios & Testing

### US1 — Deleting the open song keeps a reading view (P1)

**Why this priority**: the reported defect. Confirming a delete of the song on stage currently lands on
the songbook list, which paints the search landing in the stage; the reader loses the reading surface
and the place they were working.

**Independent Test**: open a deletable song from its songbook, confirm its sidebar delete, and inspect
the shell state and the stage. The URL is the songbook list with the empty-stage flag, `data-read` stays
`on`, `data-home` stays `reading`, and the stage article holds a centred icon above the heading
"Nothing open." and the subtitle "Choose a song or service from the list."; the search landing is not
painted.

**Acceptance scenarios**

1. **Given** a non-hymn song open on the reading stage **When** its sidebar delete is confirmed
   **Then** the shell keeps `data-read="on"` and `data-home="reading"`, `.read` is the only visible
   stage surface, a 38px empty-screen icon sits above the heading "Nothing open." and the subtitle
   "Choose a song or service from the list.", in the empty-song view's centred block; there are no
   verses, actions or project control.
2. **Given** that song **When** the delete completes **Then** the stage shows no `#searchHome` and no
   search results, and the songbook's remaining songs are still listed in the second panel.
3. **Given** the empty stage after the delete **When** the page is reloaded **Then** the same empty
   reading view is painted; the URL, not an in-memory flag, carries the state.
4. **Given** the song's own page in the history **When** the delete replaces it **Then** Back does not
   return to the deleted song's URL.
5. **Given** a song whose delete the server refuses **When** the response arrives **Then** the stage is
   untouched and the existing failure message is shown.

### US2 — Deleting the open Tata Ibadah keeps a reading view (P1)

**Why this priority**: the same flow for the second record kind named in the request; a service is the
other thing routinely opened on the stage.

**Independent Test**: open a dated service (and, in a second pass, a template), confirm its sidebar
delete, and inspect the shell: reading state up, stage article empty, services list still beside it.

**Acceptance scenarios**

6. **Given** a service open on the reading stage **When** its delete is confirmed **Then** the reading
   state is kept with an empty stage and the dated services list remains in the first panel.
7. **Given** a template open on the reading stage **When** its delete is confirmed **Then** the same
   empty reading stage is shown with the templates list in the first panel and the `?mode=template`
   selection preserved.
8. **Given** a songbook open on the reading stage (its songs in the second panel) **When** the
   songbook's delete is confirmed **Then** the same empty reading stage is shown with the songbooks
   list in the first panel.

### US3 — Deleting a row that was not on stage changes nothing on stage (P2)

**Why this priority**: protects the common case — editing a list while reading something else — from
regressing with the on-stage fix.

**Independent Test**: open one song, delete a different song from its row, and confirm the opened song
and its verses stay on stage while only the list refreshes.

**Acceptance scenarios**

9. **Given** a song on stage and a different row's delete confirmed **When** the list refreshes
   **Then** the stage still shows the first song, unchanged, and its URL does not change.
10. **Given** any on-stage delete **When** the stage is replaced **Then** the rail, theme, panel
    filters, open/closed state of the two panels, and the existing focus/hover behaviour are unchanged
    from today's list refresh.

### Edge Cases

- **When** the deleted song was the last in its songbook **Then** the empty stage still holds, the
  song list shows its existing "No songs yet." empty state, and the landing is not painted.
- **When** the deleted service was the last dated service **Then** the empty stage still holds and the
  services panel shows its existing empty state.
- **When** an on-stage delete is confirmed twice by a double click **Then** the second submit is
  refused by the existing modal busy guard and the stage is not reloaded.
- **When** the empty-stage URL is opened with a rail section other than the one that owned the record
  **Then** the stage stays empty and the lists follow the URL as they do today.
- **When** a user picks a song or service from a list while the stage is empty **Then** normal
  navigation replaces the empty stage with the chosen record.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | When a confirmed sidebar delete removes the record currently on the reading stage — a song, songbook, service or template — the shell SHALL keep `data-read="on"` and `data-home="reading"` and SHALL paint a reading stage with nothing open in it: the `.read` article SHALL carry a centred `.entry__empty` block with a generic empty-screen icon above the heading "Nothing open." and the subtitle "Choose a song or service from the list.", and SHALL carry no verses, actions or project control. Neither `#searchHome` nor `.search-results` SHALL be visible. | `modifies reading/R41` |
| FR-002 | After such a delete the two side panels SHALL remain on the deleted record's parent list: a deleted song keeps its songbook's song list, a deleted songbook keeps the songbooks list, a deleted service keeps the dated services list, and a deleted template keeps the templates list with its `mode` choice. | `modifies reading/R41` |
| FR-003 | The empty reading stage SHALL be carried by the parent list's URL with an explicit empty-stage flag, so a full reload paints the same state. The delete SHALL replace the current history entry, so Back does not revisit the deleted record's URL; picking a record from a list SHALL clear the flag through the existing navigation. | `modifies reading/R41` |
| FR-004 | A confirmed delete of a record that was not on stage SHALL keep today's behaviour: only its list refreshes, a neighbour takes focus where one exists, and the stage and its URL are untouched. | `modifies reading/R41` |
| FR-005 | The rail, panels, filters, theme, open/closed geometry, hover and focus behaviour, and every existing empty list state SHALL be unchanged. The stage copy SHALL use the empty song view's `.entry__empty`, `.entry__empty-title` and `.entry__empty-hint` treatments; the only new CSS SHALL be one `.entry__empty-icon` rule sizing the 38px empty-screen glyph. No new control, token or font SHALL be introduced. | `modifies reading/R41` |
| FR-006 | A refused, restricted, or already-deleted record SHALL NOT reach the empty stage; the existing 403/404 or failure message SHALL be shown and the current stage SHALL remain. | `modifies reading/R41` |
| FR-007 | This slice supersedes only R41's final clause "the shell swaps to the parent list" for the on-stage case. The row removal, neighbour focus for off-stage deletes, guarded endpoints and history replacement remain in force. | `modifies reading/R41` |

### Key Entities

None. The empty stage is a render state derived from the URL flag and the existing shell; it adds no
stored record, field, migration or API payload.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Deleting the open song leaves a reading stage that says nothing is open, with no search surface. | Playwright E2E: `document.documentElement.dataset.read === 'on'`, `home === 'reading'`, `#searchHome` hidden, `.read` visible, `.entry__empty-title` text `Nothing open.`, `.entry__empty-hint` text present, `.entry__empty-icon svg` 38px, and no search input in the stage. |
| SC-002 | The stage state survives a reload and respects history. | Playwright E2E: reload the resulting URL and re-check SC-001; `history.length` does not grow on delete and Back does not return to the song URL. |
| SC-003 | The same holds for the open service, template and songbook. | Playwright E2E over the three kinds: same shell assertions, plus the right list and mode visible in the first panel. |
| SC-004 | Off-stage deletes are unchanged. | Playwright E2E: delete another row while a song is open; the stage's `.read` text, URL and shell datasets are byte-identical before and after. |
| SC-005 | The empty stage paints with the existing shell geometry and no overflow at both widths. | Playwright E2E: at 1440×900 the stage box is 648×900 at x=792, `.read` 520×148 at x=856, y=48, icon 38px at x=1097, y=396, title 140×26 at y=444, subtitle 287×24 at y=480, the 108px block centred in the 900px stage; at 390×844 the stage is 390×844 and the block is centred at y=368, icon y=368, title y=416, subtitle y=452; `scrollWidth === innerWidth` in both. |

## UI/UX

`static preview at specs/221-empty-reading-stage/preview/index.html` — the real rendered reading shell,
with **Before (today)** showing the search landing that the delete currently lands on and **After
(proposed)** showing the same shell with the stage kept in reading mode and a short nothing-open message.

The stage is not blank: it reuses the empty song view's centred block — a 38px generic empty-screen icon above
the 20px heading "Nothing open." and the 16px subtitle "Choose a song or service from the list."
(owner revisions at Gate 1 and Gate 2).

- **Layout / position**: the shell geometry is unchanged except that this one state centres its block
  in the whole stage. At 1440×900 the rail is 80px, the first panel 296px at x=80, the second 416px
  at x=376, and the stage 648px at x=792; the 648×108 nothing-open block is centred in the 900px
  stage at y=396 (its centre at 450), with the icon at x=1097, y=396, the title 140×26 at y=444 and
  the subtitle 287×24 at y=480. At 390×844 the stage is 390×844 and the same block is centred at
  y=368 (centre 422), icon x=176, title y=416, subtitle y=452. Both axes are centred: the icon and
  text share the stage centre line x=1116 / x=195. No horizontal overflow (`scrollWidth ===
  innerWidth`) at 390, 720, 1440 or 1920.
- **Size / spacing**: the nothing-open `.read` and its block are 648×108 (1440×900) and 390×108
  (390×844), centred by a grid on the stage with its 40px top padding removed for this state; the
  body drops its 8px top and 40px bottom margins here. The icon is 38×38, the title 140×26 (20px/1.3)
  and the subtitle 287×24 (16px), with the block's existing 10px grid gap and 16px horizontal
  padding. The reading header is suppressed. The `#searchHome` it replaces measured 520×796 at
  x=856, y=40 (desktop) and 354×704 at x=18, y=76 (narrow).
- **Colour / typography**: the icon uses `--head-ink`, the title the existing `.entry__empty-title`
  (600 20px/1.3 ui-sans-serif), and the subtitle the existing `.entry__empty-hint`. The only new
  rules size `.entry__empty-icon` to 38px and centre the block in the stage for this state; no token
  or face is introduced.
- **States**: after an on-stage delete the reading stage shows the icon + heading + subtitle; the two
  lists keep their own normal, filtered and empty states. Before/after, dark theme and narrow width
  are all reachable in the preview. Hover, focus, active, error and loading states elsewhere are
  unchanged.
- **Motion**: the swap uses the shell's existing in-page navigation path; no new transition, entrance
  or fade is added to the empty stage.
- **Responsive**: the same state and geometry rule holds from 320px through 1920px, including the
  1272px and 720px layout boundaries.

## Assumptions

- "Empty reading view" means the reading stage stays visible with nothing open in it, carrying the
  empty-song-style icon, heading and subtitle; the side panels carry the way forward. The exact copy
  was chosen from the recommended option after the Gate 1 revision (a question offering alternatives
  was cancelled); the icon is a generic empty screen (a blank monitor with a dash), chosen by the owner from two
  sets of options so the state serves songs, services and any future page. Both are assumptions the owner can revise.
- The empty stage is only the destination of an on-stage delete. Opening a section index directly still
  paints the search landing, as specified by spec 220; this slice does not change that.
- The scope covers the four record kinds the sidebar can delete (song, songbook, service, template)
  whenever the deleted record is the one on stage, because all four share the branch this fixes.
- The parent list is the current destination for each kind, including the template list's `mode=template`
  choice; this slice changes the stage, not which list is shown.
- The URL flag is an internal shell state, not a user-facing route documented for deep links; a fresh
  load of a parent list without the flag keeps the search landing.
- The record's own page is no longer reachable after deletion (the server already answers 404), so the
  URL after the delete is the parent list, as today.
- No migration, API change, new permission or new server endpoint is needed; the existing delete
  endpoints and the existing in-page navigation are reused.
- The before/after numbers were measured on the served app at 1440×900 and 390×844 with the songbook
  and Kidung rail open; the preview draws the same markup and stylesheets.

## Clarifications

Nothing is open from Specify; the one open item came from the owner at Gate 1.

### Session 2026-11-22 — Gate 1 revision

- Q: Accept the spec pack at Gate 1? → A: "not literally 'empty' put something there" — revision, not
  acceptance. The stage must carry content, not be a blank article.
- Follow-up question offering three exact title/hint wordings was cancelled by the owner. Per SDD-08 the
  recommended option is recorded as an assumption: "Nothing open." / "Choose a song or service from
  the list.", using existing read and empty-list treatments. The revision re-entered Specify (SDD-25),
  and the preview was rebuilt from the same real shell with that copy; no plan or code existed yet.

### Session 2026-11-22 — Gate 2 revision

- Q: Accept the plan at Gate 2? → A: "make it kind of like the empty song view (heading, subtitle),
  also add some icon above it" — revision, not acceptance. The stage uses the existing
  `.entry__empty` block with icon above, not a serif reading title; the header is suppressed in this
  state and one 38px icon rule is added. Two follow-up revisions replaced the song-specific note with a  generic icon, ending at the empty-screen glyph the owner selected, then centred the block in the
  stage on both axes. Both revisions re-enter Specify; the preview
  was rebuilt and re-measured on the same real shell. The plan's bump and split are unchanged.

No `[NEEDS CLARIFICATION]` markers remain.
