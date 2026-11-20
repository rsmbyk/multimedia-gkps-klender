# Research: The dock's bucket head owns the strip above its label

**Spec**: `specs/197-dock-bucket-head-pin/spec.md`
**Unknowns remaining**: 0

## D001 — Where the strip above the label comes from

- **Decision**: the picker's scroll body carries no top padding (`#pickBody { padding-top: 0 }`) and the
  bucket head's own padding-top grows from 10px to 14px, so the head's box starts at the scrollport's top edge
  and its background covers the strip.
- **Rationale**: measured on `/obs/dock` at 449×604 — the head pinned at 68.00px with the scrollport at
  64.00px, and `document.elementFromPoint(x, top+2)` returned `BUTTON.servicerow`: the 4px was the body's
  `padding-top`, not a designed gap. Moving the padding into the head keeps the label at 78.00px in both
  states (the invariant the owner asked for) and puts the strip inside the head's painted box.
- **Alternatives considered**: (a) `top: -4px` on the head — pins flush but moves the label from 78.00 to
  74.00px, i.e. the label jumps 4px when the scroll begins; retracted after the owner saw it in the preview.
  (b) keep `top: 0` and paint the strip with a shadow or a `::before` — the cover paints wherever the head is,
  so it nicks the bottom 4px of the previous group's last row at every offset, not only when pinned.
  (c) remove the body's padding for both scrollers — the runner's pinned entry and go-to strip compensate for
  that 4px with `top: -4px` and a shadow; removing it would push both 4px into the dock's head.
- **Provenance**: research — numbers from the running page (514-offset pixel scan, hit tests at 1,600
  offsets), plus the owner's correction of (a).

## D002 — Where the air between buckets lives

- **Decision**: `#pickBody section + section { padding-top: 12px }` (8px at gate 1; raised to 12px at the
  second review — see the spec's Clarifications).
- **Rationale**: the boundary had 10.00px on develop (the head's own padding) and 14.00px after D001. The
  extra 8px sits on the section, so it scrolls away with its group: the label of a pinned head is still
  14.00px below the divider and the first bucket's label is still 14.00px below it at rest. Measured boundary
  26.00px from the previous group's last row.
- **Alternatives considered**: a margin on the head — a sticky element's insets apply to its margin box, so a
  top margin would pin the head 8px lower and reopen the strip; more head padding — that would grow the sky
  above the first bucket too, which the owner did not ask for; a separator rule — no rule is drawn anywhere in
  this list, and the slice was asked for air, not a line.
- **Provenance**: research, with the owner's word ("increase the gap between the date groups slightly") for
  the direction and 8px as the starting value.

## D003 — How the strip is measured

- **Decision**: count non-background pixels in the strip at 4× and hit-test the element painted there, across
  every scroll offset where a head is at the top.
- **Rationale**: the strip and the head are both `--rail-bg`; a row's *padding* that crosses the strip is
  invisible to the eye and to a screenshot review, but it is the same defect as a row's glyphs crossing it.
  The pixel count catches both (up to 9,715 non-background pixels at `scrollTop` 98 on develop), and the hit
  test names which element owns the pixel.
- **Alternatives considered**: visual review only — the first preview proved it unreliable (the strip looked
  empty at one offset and showed "25 OKT 2026" at another); computed styles only — `top` reads `0px` on both
  branches, so the declaration says nothing about where the box lands.
- **Provenance**: research.

## D004 — Where the test lives

- **Decision**: a new module, `tests/e2e/test_dock_bucket_head.py`, on the same
  `StaticLiveServerTestCase` + Playwright harness the dock's existing suite uses.
- **Rationale**: `tests/e2e/test_obs_dock.py` is spec 119's suite for the display state and the go to; this
  slice is about the picker's geometry, and the repo already keeps per-slice E2E modules (e.g.
  `test_media_age_buckets.py`). The new module needs its own fixtures: two buckets are enough, so it creates a
  today-ish service and one older one rather than relying on the existing three.
- **Alternatives considered**: extending the spec-119 class — its fixtures and its subject are the display,
  not the list's boxes; a pure Django test — the behaviour is layout, which only a browser can answer.
- **Provenance**: research (repo layout, `docs/PROCESS.md`'s TDD repo block).

## D005 — The bump

- **Decision**: `bump: patch`.
- **Rationale**: a visible fix to a shipped surface plus a small look change on the same surface; no new
  capability, no breaking change (VER-10: a fix is a patch).
- **Alternatives considered**: `minor` — nothing new is offered to the user; `none` — the change is
  user-visible and belongs in the changelog (VER-05).
- **Provenance**: research.

## D006 — The scroll reserve

- **Decision**: `scroll-padding-top` stays 37px.
- **Rationale**: it reserves the pinned head's strip so a cursor-scrolled row is not hidden; the head's foot
  is still 100.52px, so the reserve is still right. `top: -4px` (the retracted shape) would have required 33px.
- **Alternatives considered**: deriving it from the head's height in JS — a second measurement to keep in
  step with a stylesheet number, for no gain; leaving it at 37px after a change of head height — would hide a
  row under the head by 4px.
- **Provenance**: research.

## Open

None.