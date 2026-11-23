# Research: Add verse sits beside Project in the song header

**Spec**: `specs/231-add-verse-in-header/spec.md`
**Unknowns remaining**: 0

## D001 — Where the control belongs in the DOM

- **Decision**: inside `.read__project`, before the `Project` button, in `song.html`'s
  `read_actions` block.
- **Rationale**: `read__head-top` is `display:flex; justify-content:space-between`; the project
  group is its right-hand child with `justify-content:flex-end` and an 8px gap. A sibling of that
  group would be spread across the row rather than sitting next to Project; a child lands exactly
  left of it. The Tata Ibadah header already places several actions in one `.read__project` group.
- **Alternatives considered**: a new wrapper around both buttons (extra markup for no measured
  gain); keeping the dashed row and adding a second header control (contradicts "move" and leaves
  two add controls).
- **Provenance**: research

## D002 — Which class and height the moved control carries

- **Decision**: keep `.verse-add__btn` plus a scoped `.verse-add__btn--head`; set only
  `height:34px; padding:0 12px` inside `.read__project`.
- **Rationale**: the old control was 38px with a dashed border; Project is 34px with a solid
  border. Keeping the class preserves the button's identity, handler and focus rule; matching the
  height makes the shared row read as one set. The dashed border is the approved preview's look.
- **Alternatives considered**: reuse `.read__project-btn` (changes the button's identity and
  drops the dashed affordance the request said to move); leave 38px (visible 4px mismatch).
- **Provenance**: research

## D003 — The single `[data-add-verse]` invariant

- **Decision**: exactly one add control in each state — header for songs with verses, centre
  invitation for empty songs.
- **Rationale**: `songs_verse.js` uses `document.querySelector('[data-add-verse]')` to read
  `data-song` before persisting a verse reorder. A second node would make that lookup depend on DOM
  order. Keeping one node also preserves spec 224's one-control rule.
- **Alternatives considered**: add a second button and change the script to select all — out of
  scope and unnecessary for a move.
- **Provenance**: research

## Open

<!-- empty when Phase 0 is finished -->
