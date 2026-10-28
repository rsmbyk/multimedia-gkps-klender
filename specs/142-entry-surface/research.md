# Research: a service entry draws no box until it is pointed at

**Slice**: `specs/142-entry-surface` · **Unknowns remaining: 0**

## D1 — Remove the resting surface rather than restyle it

**Decision**: `.tatib__item--acts` and `.tatib__eos` keep their box and lose every bit of paint;
hover, deliberate focus and modal-origin keep filling the row with `--icon-hover-bg`.

**Rationale**: the shipped surface is two things that do not agree. The fill composites to
`rgb(244, 242, 238)` on the canvas — three of 255 levels, 1.027 : 1 — while the ring sits at
1.166 : 1. So the ring carries the whole signal, every entry is boxed, and the page reads as a
wireframe in which the section break's 2px rule means no more than the 23 rings around it. The
project's own design defaults call this *boxed near-white panels* and list it among the dated tells.

**Alternatives considered**: (a) keep the ring, drop the fill — removes the pretence but leaves the
wireframe; (b) raise the fill to 4% and drop the ring — a real surface (9 of 255), demonstrated as
candidate **D · Felt**; (c) a hairline between entries — demonstrated as **B · Rules**, rejected
because the section break already owns the one rule that means something; (d) a hanging
`L :` / `J :` gutter — demonstrated as **C · Gutter**, rejected because the entries' left margin was
not where the problem was. All four are in `preview/preview.html` over stylesheets frozen at
`ca71c850`.

**Provenance**: owner decision, 2026-10-28 — "try bare as default, then filled when being hovered".

## D2 — Delete the two tokens instead of zeroing them

**Decision**: `--tatib-entry-fill` and `--tatib-entry-outline` are removed from both theme blocks;
the two tests that read them are rewritten to assert the canvas.

**Rationale**: a token that resolves to nothing keeps a concept alive in the palette and invites the
next reader to think a resting fill is still part of the design. Only two readers existed outside
the surface rule: the token test and `_resting_background` in `test_tatib_hover.py`.

**Alternative**: leave the tokens at `transparent` / `none` — fewer lines changed, but the palette
would claim a surface the stylesheet no longer paints.

**Provenance**: agent decision recorded at gate 1; the spec's Assumptions carry it.

## D3 — No separate surface for media rows

**Decision**: media rows lose the resting paint like every other kind.

**Rationale**: shown on `/tatib/144/`, which holds all five kinds: a media row is identified by its
42px icon tile, its filename and its `Type · Local library unavailable` line, not by the box around
it. The alternative — a fill for media only — was built and shown (3.5% ink, radius 12).

**Provenance**: owner decision, 2026-10-28 — "leave all kinds bare — media reads fine up close".

## D4 — The preview tier is live

**Decision**: the preview is the branch's own server (`/tatib/142/`, `/tatib/144/`), with the static
comparison kept as the record of the four candidates.

**Rationale**: SDD-06 makes a live preview the stronger tier and this change is CSS on a page the
server renders — a click hits the real code path. The static page had to freeze the stylesheets
precisely so its "Now" column could keep showing the retired box.

**Provenance**: SDD-06; the owner reviewed the live pages throughout.

## D5 — Leave the vertical rhythm alone in this slice

**Decision**: the gap between entries, the add rows and the section break's own margins are not
touched here.

**Rationale**: spec 068's box was carrying separation that spacing owed, but changing the rhythm and
the paint in one slice would make neither reviewable. The gap work is slice 143's, stacked on this
branch as `951afa6f` and out of scope.

**Provenance**: agent decision at Plan; the owner's later gap requests were answered there, not here.
