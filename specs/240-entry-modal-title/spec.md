# Feature Specification: restore the title band on the large entry dialogs

**Slice**: `specs/240-entry-modal-title`
**Branch**: `fix/240-entry-modal-title`
**Created**: 2026-11-24
**Status**: Draft — Gate 1 pending
**Input**: "the new/edit text and new/edit media entries modal's title is broken"
**Demand**: `ITEM-255` (new card, re-check before delivery)
**Capability**: `reading/R10` (modified — restoration of what R10 already requires)
**Preview**: live preview at `http://127.0.0.1:8790/tatib/149/` — from `/`, click the
**Tata Ibadah** rail, then the service named `hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh` (pk 149).
Start with `python3 ~/.hermes/cache/scratch/gkps240/run.py runserver 0.0.0.0:8790 --noreload`
from `~/Projects/multimedia-gkps-klender-240` if the server is down.

Spec 226 moved the large frame's title inset and divider from `.editor__title` to
`.editor__head` so a verse editor header draws a single rule. The text Create/Edit and
media Create forms render their title *directly* in `#editorContent` — `_entry_form.html`
has no `.editor__head` — so those three dialogs lost the whole band: the title text now
starts at the dialog's own top-left corner with no 26px/20px inset and no divider.
The media Edit form is compact and keeps its own 22px-padded title; it is named in the
report but is not one of the broken frames.

The change gives the headerless large frame its own inset and one rule. No markup,
script, translation, frame size, field geometry or behaviour changes.

## User Scenarios & Testing

### US1 — The large entry dialogs have their title band back (P1)

**Why this priority**: this is the reported surface; without the inset the title
touches the dialog edge and the form no longer matches the media frame R10 pins.

**Independent Test**: at 1440×900, open `+ Text`, `+ Media` and a text row's Edit and
read the title text's offset from the dialog and the divider under the band.

**Acceptance scenarios**

1. **Given** a service at 1440×900 **When** `+ Text`, `+ Media` or a text entry's Edit
   opens **Then** the title text starts 26px from the dialog's left and 21px from its
   top, the band is 72.5px tall, and one 1px divider sits at its bottom.
2. **Given** the same dialogs **When** their fields are measured **Then** the New text
   form's first field moves with the band from 133.5px to 174.5px below the dialog
   top, stays 788px wide, and the action row still ends at the dialog's bottom edge;
   the frame stays 840×760.

### US2 — The header-bearing editor is untouched (P2)

**Why this priority**: spec 226 fixed a double rule in the verse editor by moving the
inset to `.editor__head`; that fix must survive.

**Independent Test**: open a verse editor, inspect its `.editor__head`, and run the
verse-header test module.

**Acceptance scenarios**

1. **Given** a verse Create or Edit dialog **When** its header is measured **Then** the
   head keeps `20px 26px 14px`, the title keeps zero padding and zero border, and
   exactly one rule paints across the head.
2. **Given** a passage, song, media-Edit or old-item form **When** it opens **Then** its
   compact dialog and its own 18px-padded, divided title are unchanged.

### US3 — Narrow windows keep the small gutters (P2)

**Why this priority**: R10 pins a separate `16px 18px` title band below 650px; a
broader selector must not outrank it and put the wide inset back on a phone.

**Independent Test**: at 390×844, open `+ Text` and read the title text offset, band
height and divider.

**Acceptance scenarios**

1. **Given** a 390px window **When** `+ Text` opens **Then** the title text starts 18px
   from the dialog's left and 17px from its top, the band is 64.5px tall and the 1px
   divider remains.
2. **Given** that narrow dialog **When** its fields are measured **Then** they stay
   inset 18px and the page behind still gains no scrollbar.

## Edge Cases

- The delete confirmation's screen-reader-only `#editorTitle` is not a visible band;
  it must not gain padding or a rule.
- The loading state (`Add Text` / `Add Media` with `.editor__body--loading`) paints a
  22px-padded generic dialog; the new selector requires `[data-editor-size="large"]`,
  which only the loaded fragment carries, so loading is unchanged.
- Dark theme uses the same `var(--divider)` colour as every other editor rule; no
  separate theme rule is needed.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A large entry form rendered without `.editor__head` SHALL pad its title `20px 26px` and draw one 1px bottom divider, giving a 72.5px band at 21px type. | `reading/R10` |
| FR-002 | Below a 650px window that same title SHALL pad `16px 18px` and keep the 1px divider. | `reading/R10` |
| FR-003 | Editors that render `.editor__head` SHALL keep spec 226's zero-padding title and single head rule. | `reading/R10` |
| FR-004 | Compact dialogs, loading states, screen-reader titles, frame dimensions, fields, action row and all form behaviour SHALL NOT change. | `reading/R10` |

### Key Entities

- **`.editor__title`** — the `#editorTitle` heading inside the fetched form fragment.
- **`.editor__head`** — the header row the verse and record editors wrap their title
  in; absent from `_entry_form.html`.
- **`[data-editor-size="large"]`** — the marker on the fetched form that selects the
  840×760 frame, carried by text Create/Edit and media Create only.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Large entry titles are inset and divided | text x 26px, y 21px, band 72.5px, border 1px in all three large dialogs |
| SC-002 | The verse header still has one rule | head padding `20px 26px 14px`, title border `0px`, ruled descendants 0 |
| SC-003 | Narrow band is 16px 18px | text x 18px, y 17px, band 64.5px, border 1px at 390px |
| SC-004 | No geometry or behaviour drift | existing `test_entry_modal_frame` and `test_verse_modal_header` modules stay green |

## UI/UX

Live numbers from the slice server, 1440×900 and 390×844, dark and light read identically:

| Surface | Before (broken) | After |
| --- | --- | --- |
| New text / Edit text / New media title | text at 0px/0px from dialog; padding `0px`; border `0px`; band 31.5px | text at 26px/21px; padding `20px 26px`; border `1px`; band 72.5px |
| Same at 390px | padding `0px`; border `0px`; band 31.5px | padding `16px 18px`; border `1px`; text 18px/17px; band 64.5px |
| New media frame | 814.8×737.2 during its 190ms entrance, then 840×760 | unchanged |
| Edit media (compact) | title inset 21.3px, padding `0px 34px 14px 0px`, border `1px`, 18px type | unchanged |
| Verse editor header | head `20px 26px 14px`, title padding/border `0px`, one rule | unchanged |

A screenshot is not the preview: the change is applied to the served CSS in the slice
worktree, and `preview/probe.py` reads these numbers from the live page. Its "before"
readout injects a local override into the browser only; the served code keeps the fix.

## Assumptions

- "new/edit text and new/edit media" names the large-frame entry forms; the compact
  media Edit title is healthy and is deliberately left alone.
- The user-visible target is the pre-226 band already written in R10, not a new design.
- No new requirement ID is needed: R10 already states this behaviour, so the fold is a
  *modified* block with a regression note, not an addition.
- Card `ITEM-255`, spec `240` and patch `1.36.26` are claimed against the refs visible
  at drafting; parallel slices may take them first, so each is rechecked at delivery.
- The full browser suite stays deferred to the push step; only the two directly
  affected modules are run here.
