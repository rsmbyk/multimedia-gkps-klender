# Research: the live entry header's corners follow its pin state

**Spec**: `specs/208-dock-stuck-corner/spec.md`

## D001 — keep the corner toggle outside the band's motion guard

The band's 300 ms guard exists because reparenting its label mid-glide shifts layout. A corner
class paints no layout, so leaving `updateStuck()` outside the guard fixes the desync without
touching the band's own motion. Measured against the DOM: develop 328/328 pinned frames wrong,
slice 0/328.

## D002 — what "pinned" means

Measured: the header's top at the scrollport's top edge within 0.5 px **and** its block still
reaching below. A header whose whole block is above the edge is out of view and not pinned;
a clamped list must still agree with where the geometry lands.

## D003 — the bottom pin is a faithful clone in a list-level slot

The header node is the entry's first child; sticky can only pin it toward room below, which would
leave its `li` — forbidden. The Next band, the last child, can pin. So the pin is a `cloneNode(true)`
of the live `.entryrow` in a list-level sticky slot. A "LIVE · label" caption strip was tried and
rejected at live review ("can you not make it double? make it like the top pin"); the clone is the
header's own face, so one header is ever visible.

## D004 — the Next band is list-level and always visible

It used to be the live `li`'s last child — caged when the block was off screen, and dangling after
the last row when the whole list fit. It now lives in `li.nextband-slot` at the list's end, shown
whenever a next entry exists. `#entryList` is `min-height: 100%` and a flex column with the slots
at its flow bottom (`margin-top: auto`), and `#runBody` has no bottom padding, so the band lands
flush at the edge in both scroll and no-scroll states.

## D005 — clip at the band's top, not a row early

Staging a row early added a second header-height of chrome while the header was still clear
("it gets too tall", owner). The trigger is `row.bottom > bandRect.top`: at that boundary the
clone sits exactly over the real header (one header-height, bottom at the band's top) and takes
over with no added height.

## D006 — the pin's click is the centre act

The ruled act is re-centre the live row, keep the current screen, return to following — the centre
control's act (R15), never a different screen written to the display state.
