# Research — the rail's marks and the stage's own

**Spec**: `specs/151-rail-icons/spec.md` · **Date**: 2026-10-29

## What the product draws today

| Idea | Drawn as | Where |
| --- | --- | --- |
| the Bible | open book, rounded covers (`M12 6.6S10.1 4.2 …`) | rail, panel empty state |
| a passage | open book, square covers (`M12 6.6C10.3 5.2 …`) | stage kind mark, Add Passage tile |
| a song | single flagged note | stage kind mark |
| a song, elsewhere | beamed pair | rail, Add Song tile, panel/chapter empty states |
| an audio file | beamed pair (`M9 18V5l11-2v13` + 3px heads) | `gkpsMediaIcon('audio')` — stage chip, library list, service-media dialog, upload preview |
| a service order | rounded page + three rule lines | rail, panel empty state |
| a PDF | page with a folded corner + rules | `gkpsMediaIcon('pdf')` |

Two drawings of an open book across four places, two drawings of a song, and one audio mark that is a
copy of the song's — the report is that picture, read by a person in a rail.

## Decisions

### R1 — one mark per kind, at every size

**Decision**: a kind's mark is one path; the rail, the kind mark and the empty stage's tile all draw
it, at the size their own box already gives them (24px rail, 24px tile, 20px kind mark).

**Rationale**: the owner's answer — *"also use the same icon for passage entry"* — states the rule for
the Bible; the song already had it in the rail and the tile, and spec 144 had left the row out. Making
it a rule retires three open books and two notes.

**Alternatives rejected**: keep the rail's mark separate from the stage's (the status quo, which the
report rejects); unify by giving the stage the rail's *size* as well (a 24px kind mark takes 4px off
the title's clearance and changes a spec-144 contract nobody asked to move).

**Provenance**: owner decision, gate 1 answer, 2026-10-29.

### R2 — the Bible is an open book with a Latin cross above it

**Decision**: `<path d="M12 9.6c-1.6-1.3-3.8-1.9-6.9-1.7v10.4c3.1-.2 5.3.4 6.9 1.7 1.6-1.3 3.8-1.9 6.9-1.7V7.9c-3.1-.2-5.3.4-6.9 1.7z"/><path d="M12 9.6v10.4"/><path d="M12 2.6v4.6M10.1 4.5h3.8"/>`

**Rationale**: an open book keeps the shape the passage mark already had — so the row changes by a
cross, not by a redesign — while the cross is the one cue that says *Bible* rather than *book*.

**Alternatives measured in the preview**:

| Candidate | 24px rail | 20px row | verdict |
| --- | --- | --- | --- |
| open book + cross above | reads as a book, the cross adds the Bible cue | the cross survives (4 countable arms at 4×) | **chosen** (owner) |
| closed book + Latin cross on the cover | reads as a Bible; the cross can read as a "plus" without a Latin stem | n/a — a closed book cannot also be the open one the row needs | rejected: the owner wants one drawing for both |
| closed book + cross + fore-edge line | the extra line reads as a second stroke, not a page block | n/a | rejected: too busy at 24px |
| closed book + cross + ribbon | the ribbon competes with the cross at 24px | n/a | rejected: too busy at 24px |

**Provenance**: owner decision (open + cross) at gate 1; the shape measurements are `build_preview.py`
renders at 1:1 and 4×.

### R3 — the cross is a Latin cross, not a plus

**Decision**: bar 3.8 units wide at `y = 4.5`, stem 4.6 units from `y = 2.6` to `7.2` — 1.9 above the
bar, 2.7 below.

**Rationale**: an equal-armed cross at 24px is a plus sign; the equal-arm version was drawn and read as
"a book with a plus" in the first contact sheet. The longer lower arm is what makes it a cross.

**Provenance**: contact-sheet comparison of equal-arm vs Latin (2026-10-29); no owner question needed —
the asked-for meaning decides it.

### R4 — a service order is a clipboard

**Decision**: board `4.6,3.4 → 19.4,20.6` (r 2), clip `8.6,1.9 → 15.4,5.3` (r 1.4), rules at `y = 9.6`,
`13`, `16.4`.

**Rationale**: the report is "it looks like a file document". A clip above the board is the one
silhouette difference from a page; the three rules keep it an agenda rather than a folder (the Media
Library's own mark).

**Alternatives**: an ordered-steps list (vertical line, three dots, three bars) — also stops reading as
a file, but at 24px it reads as a menu; the owner left this slot on the proposal, so the clipboard
stands and the alternative stays in the preview.

**Provenance**: owner left the slot unanswered at gate 1 (recorded assumption); both candidates are
rendered in the preview's top bar.

### R5 — an audio file is a waveform of five bars

**Decision**: `M3.6 10.2v3.6M7.2 7.2v9.6M10.8 4.4v15.2M14.4 7.2v9.6M18 10.2v3.6`.

**Rationale**: it is the only mark in the set made of vertical bars, so it cannot be confused with a
note; and at 23px it fills the 42px chip the way the other four families do, which a narrower waveform
did not (the first draft spanned 57% of the box and read as a secondary mark).

**Alternatives measured at 42px/23px in the family row**: a narrower waveform (too light), a waveform
inside a rounded square (too busy at 23px), a speaker with two arcs (reads as a volume control, not a
file). The owner chose the waveform at gate 1.

**Provenance**: owner decision; the three-candidate chip comparison is a 2026-10-29 render.

### R6 — the marks keep their authored stroke widths

**Decision**: the path is shared; `stroke-width` stays as each surface authors it — rail 1.7, kind mark
1.8, add tiles 1.6, panel empty state 1.5, media chips 1.8.

**Rationale**: an icon shrunk to 20px needs a heavier relative stroke to hold its weight; that is why
the product already varies it. Forcing one value would either thicken the rail or lighten the row.

**Provenance**: existing declarations (`components.css:166`, `:2024`, `:554`, `:624`, `:2824`,
`tatib.html:200`).

## Unknowns

**0.** The four shapes, the sizes and the stroke widths are decided; the one open slot (Tata Ibadah)
is recorded as an assumption with its alternative still reachable in the preview.
