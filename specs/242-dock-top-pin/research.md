# Research — spec 242

## D001 — trigger: the whole live block above the scrollport

**Decision**: show the pin when `liveLi.bottom <= runBody.top + 0.5` (and the header is at/above
the edge). Do not stage it while any of the block is still on screen.
**Rationale**: the native `position: sticky; top: -4px` already holds the header at the edge
while its `li` straddles the scrollport; a clone in that range would be a second header. The
block-above boundary is the exact range sticky cannot reach — the mirror of spec 208's bottom
pin, which starts as the header goes off the other edge.
**Alternatives**: trigger on header scroll-out only (never fires — sticky keeps it at the edge);
stage a row early (adds a second header-height of chrome, rejected by the owner in spec 208).
**Provenance**: `static/web/obs-dock.js:425-430`, probe_top.py measurements on develop and slice.

## D002 — the pin is a faithful list-level clone

**Decision**: `li.topband-slot` at the head of `#entryList`, sticky `top: -4px`, holds
`cloneNode(true)` of the live `.entryrow`; flat top / 9 px bottom, z-index above the native row.
**Rationale**: a sticky element cannot leave its containing block; the header is its block's
first child, so it cannot stay past the block. A list-level slot can. Faithfulness (number, name,
subtitle, chevron, selected face) is the owner's explicit bottom-pin ruling in spec 208 and was
confirmed for the top pin in the scope answer.
**Alternatives**: move the real header to the list (changes liveness and toggle semantics); a
short "LIVE" caption band (rejected in spec 208 as a second, separate-looking band).
**Provenance**: spec 208 US4 mechanism finding; `obs-dock.css` `.liveband-slot` rules.

## D006 — the slot must not take flow space

**Decision**: `.topband-slot` is `height: 0`, its cloned header absolutely positioned at the
slot's top; `[hidden]` still uses `display:none`.
**Rationale**: an in-flow 56 px slot disappears on hide and re-appears on show; hiding it pulled
the live block back above the edge, which re-showed the slot — a geometry feedback loop caught by
the per-frame E2E (slot visible at block bottom +14.6 px). A zero-height slot cannot shift the
list, so visibility is a pure function of the block's position.
**Alternatives**: reserve a permanent header-height gap at the list head (changes the resting
layout of every service); render the clone in an overlay outside the list (loses the list's
scrollport geometry and the sticky pin).
**Provenance**: E2E `test_the_top_pin_tracks_the_block_per_frame`, first red on the in-flow slot
and green after the zero-height change; 0 mismatched frames over 51 sampled frames.

## D003 — the click is the centre control's act

**Decision**: clicking either pinned strip calls `setFollowing(true)` and `centerRow(liveNode())`;
no screen write.
**Rationale**: spec 208 FR-010 sets this ruling for the bottom pin; the owner chose it over
"project the live entry again". Symmetry avoids a second interaction grammar.
**Alternatives**: re-project the live screen (writes state); do nothing (leaves the operator
stranded above their live entry).
**Provenance**: spec 208 FR-010 and `obs-dock.js` click handler.

## D004 — one reconciliation path for both pins

**Decision**: `updatePins()` calls `updateStuck()`, `updateLiveBand()` and `updateTopBand()`, and
is used by scroll frames, sync, glide frames, morph landings and resize.
**Rationale**: spec 208 moved the corner and bottom states out of the NEXT band's motion guard;
adding the top state to the same call keeps all three consistent on one curve and under reduced
motion, with no new event source.
**Alternatives**: a separate scroll-only listener (misses height-only changes and glides — the
root cause spec 208 fixed).
**Provenance**: spec 208 FR-002/FR-008; `updatePins()` call sites in `obs-dock.js`.

## D005 — reconcile at the head of a centring glide

**Decision**: call `updatePins()` synchronously at the start of `glideRow()`, before the first
eased frame.
**Rationale**: the probe's per-frame sampler found exactly one stale frame at the click boundary
(block still 3.7–4.7 px below the edge, clone still visible); the click/sync clamp can move the
list before the first rAF of the glide. One paint-only reconciliation removes it without
touching the 200 ms curve.
**Alternatives**: widen the geometry tolerance to ~8 px (shows the pin while the header is in
view — a visible duplicate); accept one stale frame (violates spec 208's per-frame precedent).
**Provenance**: `preview/probe_top.py` runs before and after the change: 1 mismatch / 50 frames
→ 0 mismatch / 50 frames.
