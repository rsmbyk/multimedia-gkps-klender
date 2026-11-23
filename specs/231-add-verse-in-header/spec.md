# Feature Specification: Add verse sits beside Project in the song header

**Slice**: `specs/231-add-verse-in-header`
**Branch**: `fix/231-add-verse-top`
**Created**: 2026-11-23
**Status**: Accepted (Gate 1 2026-11-23)
**Input**: "i want to move the Add verse button to the top of the page, to the left of the project button (still follows the rule that only visible if there is at least one verse. otherwise still only the center add verse)"
**Demand**: `ITEM-246`
**Capability**: creates `reading/R56`

## User Scenarios & Testing

### US1 — The add control lives in the header while the song has verses (P1)

**Why this priority**: a song's Add verse control sat at the foot of the lyric column, below the
last verse, while the page's other action — Project — already lived in the header beside the
eyebrow. An operator editing verses had to scroll past the whole song to reach the add control.
Putting the two actions in one header row makes the page's editing actions findable in the same
place, and keeps them together as a set.

**Independent Test**: at 1440×900 on `/songs/1880/` (two verses, editable), the header action row
holds `Add verse` at x=1157, y=42, 111×34 immediately left of `Project` at x=1276, y=42, 96×34,
with an 8px gap; the dashed row under the last verse is gone and exactly one `[data-add-verse]` is
in the document.

**Acceptance scenarios**

1. **Given** a non-hymn song with at least one live verse **When** the reading page is painted
   **Then** its header actions show `Add verse` immediately to the left of `Project`, both 34px
   tall with an 8px gap.
2. **Given** that header **When** `Add verse` is clicked **Then** `#editorModal` opens with the
   title `New verse`, without a reload.
3. **Given** that song **When** the body is inspected **Then** no dashed `.verse-add` row remains
   beneath the last verse.
4. **Given** the same song at a narrow viewport (≤720px) **When** the page is painted **Then**
   `Add verse` stays in the header; `Project` is hidden by the pre-existing responsive rule, so
   the add control is the row's only action.
5. **Given** a hymn song, or a reader without edit permission **When** the page is painted
   **Then** no header `Add verse` is drawn; `Project` keeps its spec-193 `verse_rows` gate
   and is unchanged. **Correction:** an earlier draft of this criterion claimed Project was
   gated on edit permission too; the test disproved it against unmodified `develop`.

### US2 — An empty song keeps only its centre invitation (P2)

**Why this priority**: the empty song's invitation is the page's onboarding to verse editing. The
change must not add a second add control there, or hide the invitation when the header actions are
gated off by the absence of verses.

**Independent Test**: on `/songs/1909/` (no verses) the header contains only the eyebrow, the
document has exactly one `[data-add-verse]`, and it is the 112×38 button inside the centred
`.entry__empty` invitation.

**Acceptance scenarios**

1. **Given** a song with no live verses **When** it is painted **Then** the header row carries no
   `Add verse` and no `Project` button.
2. **Given** that song **When** the body is inspected **Then** exactly one `Add verse` button sits
   in the centred empty-state invitation, at its existing 112×38 box.
3. **Given** a song whose only verse is deleted **When** it is painted **Then** it takes the empty
   path, not the header path.

### Edge Cases

- A hymn songbook's songs never carry verse controls; the gate is unchanged.
- The verse script reads `document.querySelector('[data-add-verse]')` to find the song id for
  reorder persistence; each state must therefore carry exactly one such node.
- The header button inherits the product's existing `.verse-add__btn` hover, focus and dashed
  border; no new interaction state is introduced.
- A song opened through the shell's in-page navigation paints the same header as a direct load,
  because the markup is server-rendered in the swapped fragment.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | `reading/song.html` SHALL render `Add verse` in the `read_actions` block, inside the same `.read__project` group as `Project` and before it, gated on `can_edit_verses` and at least one live verse. | `reading/R56` |
| FR-002 | `reading/song.html` SHALL NOT render the `.verse-add` row beneath the last verse when the song has verses. | `reading/R56` |
| FR-003 | An empty song SHALL keep its single centred `.entry__empty` invitation with one `Add verse`; no header action SHALL be drawn for it. | `reading/R56` |
| FR-004 | The header `Add verse` SHALL keep the existing `[data-add-verse]`/`data-song` wiring, so it opens `#editorModal` with `New verse` and supplies the song id used by the reorder write. | `reading/R56` |
| FR-005 | The header `Add verse` SHALL keep the dashed `.verse-add__btn` identity and SHALL be 34px tall in the header so it matches `Project`. | `reading/R56` |
| FR-006 | No model, endpoint, permission rule, token, font or animation SHALL change. | `reading/R56` |
| FR-007 | `reading/R56` SHALL state that the song page's add control lives in the header beside Project while verses exist, and falls back to the centre invitation only when there are none. | `reading/R56` |

### Key Entities

None. The change is one control moved between two blocks of a template and one scoped CSS rule;
no model, endpoint or context value is touched.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Add verse is in the header, left of Project. | Live 1440×900 probe: boxes `x=1157,w=111,h=34` then `x=1276,w=96,h=34`, 8px gap. |
| SC-002 | The bottom dashed row is gone. | `.verse-add` selector resolves to `null` on a song with verses. |
| SC-003 | Exactly one add control per state. | `[data-add-verse]` count is `1` on `/songs/1880/` and on `/songs/1909/`. |
| SC-004 | The empty song is unchanged. | Header `read_actions` contains no button; invitation button 112×38 in `.entry__empty`. |
| SC-005 | The relocated control still works. | Clicking it opens `#editorModal` with `New verse`. |
| SC-006 | No permission regression. | A hymn song paints no `Add verse` while `Project` remains, as on unmodified `develop`. |

## UI/UX

`live preview at http://127.0.0.1:8772/songs/1880/ and /songs/1909/` — this slice's own worktree
(`fix/231-add-verse-top`), served by `preview/serve.sh` against the compose Postgres. The change
is server-rendered markup, so a static page could not show the permission gates or the editor
dialog; the comparison baseline is unmodified `develop` at `http://127.0.0.1:63404/`.

- **Before (measured, live, 1440×900)**: `/songs/1880/` eyebrow `LAGU` at x=80, Project 96×34 at
  x=1276, y=42; dashed `.verse-add` row 1291×38 at x=80, y=846 with its button 112×38 at x=124,
  y=846. Two distinct action zones.
- **After (measured, live, 1440×900)**: header `.read__project` group 214×34 at x=1157, y=42:
  `Add verse` 111×34 at x=1157 then `Project` 96×34 at x=1276, gap 8px. No `.verse-add` row.
  Empty song `/songs/1909/`: header has only the eyebrow; one 112×38 add button at x=1058,
  y=350 inside the 366×128 invitation.
- **Layout / position**: Add verse precedes Project in the same right-aligned header group.
- **Size / spacing**: both actions 34px tall, 8px gap; Add verse keeps 9px radius and dashed
  `color-mix(in srgb, var(--focus) 42%, var(--divider))` border, with `padding: 0 12px` in the
  header only.
- **Colour / typography**: unchanged tokens — `var(--head-ink)` at rest, `var(--ink)` and
  `var(--focus)` on hover, `ui-sans-serif` 600 13px/1, 15px icon.
- **States**: hover, `:focus-visible` and active use the existing `.verse-add__btn` rules;
  empty state and hymn read-only path unchanged; at 560px the add control remains in the header
  while the pre-existing rule hides Project.
- **Motion**: none added or removed.
- **Responsive**: no new media query; the existing 480px `.verse-add` padding rule applies only
  to the invitation, not the header button.

## Assumptions

- "Move" was read as relocate, not duplicate: the dashed row under the verses is removed rather
  than kept alongside the new header control.
- The header control keeps its dashed identity because the request moves the button, not restyles
  it; its height alone is normalised to Project's 34px so the pair reads as one set. This was shown
  in the accepted preview.
- The visibility gate is `can_edit_verses and verse_rows`, matching the old dashed row; Project
  stays gated on `verse_rows` alone, as spec 193 defined.
- The gate-1 material was the live preview on the slice worktree (the real code path), so the
  template and CSS were applied before the pack was written. No commit exists yet: commits start
  at Fold per GIT-06.
- No owner question was needed: the wording names the destination and the fallback state, and the
  one judgment call — keeping the dashed style — was visible and accepted in the preview.

## Clarifications

### Session 2026-11-23

- Gate 1 accepted from the live preview and its measured before/after boxes; no questions raised.
  Zero `[NEEDS CLARIFICATION]` markers remain.
