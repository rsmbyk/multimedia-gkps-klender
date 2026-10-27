# Research: on a small screen the sidebars are a drawer stack over the page

**Slice**: `specs/138-sidebar-overlay-stack` · **Date**: 2026-10-27
**Exit**: zero unknowns.

## D1 — The overlay is a media query, and the push is switched off by its own custom properties

**Decision.** At `≤1272px`, `--books-w`, `--ch-w-shown` and `--reserve-ch` go to `0` and the two
lists become fixed drawers at the rail's edge. No JavaScript decides the layout.

**Rationale.** The shell already owns the geometry as three custom properties: the stage's margin
and the second list's left edge both derive from them (`components.css:59–76`), which is what makes
the present push a single coordinated motion. Setting them to zero at one breakpoint turns the push
off everywhere at once, without a second layout or an inline style the script has to undo when the
window grows.

**Alternatives.** A `data-mode="overlay"` attribute written by the script — that is what the
prototype does, and it duplicates the width decision in JS. A separate parallel stylesheet — two
layouts to keep in step.

**Provenance.** `static/styles/design/components.css` (`:root[data-nav="open"] { --books-w: … }`,
`--panel-w`, `--ch-w-shown`), `static/styles/design/tokens.css:60–76`; the prototype's measurements
(`preview/probe_prototype.py`), where the same trick held the stage at 944/688/425px.

## D2 — Stacking is z-order and one transform; the rail is painted above the drawers

**Decision.** `.rail` takes `z-index: 50` at the overlay width; the panel is 40 and the second level
41, with a resting `transform: translateX(-100%)` from the rail's edge.

**Rationale.** A drawer at rest sits entirely to the left of its own left edge, which is behind the
rail; sliding right, its leading edge emerges from the rail's right edge. That is the owner's
"slide from under the main rail" with no clipping and no second animation: the effect comes from
paint order, which cannot fall out of step with the transform.

**Alternatives.** `clip-path` on the rail — an extra layer to animate and the tooltip's stacking
context (the rail's `::after` at z 30) would change. Translating from off-window — what the
prototype first did; the drawer then appeared from the window's edge, not from the rail.

**Provenance.** `components.css:92–145` (the rail's fixed box and its tooltip rule); the owner's
review of the prototype, 2026-10-27 (`## Clarifications` in the spec).

## D3 — The second level covers its parent; nothing is offset

**Decision.** `[data-ch="open"] .chapters` keeps the parent's `left` and `width`, one z-index higher.

**Rationale.** The owner's second reading of the stack: a parent edge showing behind the child read
as a third column, not as depth. Covering exactly also means the phone's drawers can be full width
without an arithmetic that has to know about insets.

**Alternatives.** The prototype's 44px offset, and the 12px phone inset — both retracted by the owner
after seeing them (`## Clarifications`).

**Provenance.** Owner, 2026-10-27; measured in the prototype after the change: both boxes at
`80 → 496`, `80 → 448`, `0 → 425`.

## D4 — The toolbar is markup in `base.html`; the rail's foot is *positioned* into it, not moved

**Decision.** A `.topbar` header is always in the document and hidden above 720px. At `≤720px`
`.rail__foot` is positioned into its right end with `position: fixed`, and `.rail__logo` is hidden.

**Rationale.** Moving a node between containers needs script, runs on every resize and risks losing
focus in the middle of an edit. Positioning keeps the buttons where they are in the DOM — same ids,
same handlers, same theme state — while placing them on screen where the owner asked. The toolbar
itself is markup so it exists before the first paint, with no flash of a page without a chrome.

**Alternatives.** Duplicating the theme control in the toolbar — two controls writing one state, and
two places to keep the three-state icon in step. Moving the foot with `appendChild` — the
prototype's approach, fine for a prototype, a resize handler in production.

**Provenance.** `base.html:41–108` (rail, logo, foot), `:103–108` (`#themeBtn`, `#mediaTransferRail`);
`components.css:145–200` (`.rail__btn` sizes, the theme's three glyphs).

## D5 — The phone's menu is the rail, re-laid out

**Decision.** No second menu: at `≤720px` the rail's `position: fixed` box becomes a full-width
drawer under the toolbar, its buttons become rows with their names, its logo and foot are hidden.

**Rationale.** The rail already holds exactly the five destinations the menu needs, each with an
icon, an `aria-label` and a tooltip carrying its name. Re-laying it out keeps one source of
destinations (the template's rail), and the names come from the attributes already there.

**Alternatives.** A separate `<nav>` menu — a second list to keep in step with the rail, and the
active-section logic duplicated. Keeping the icon strip — the owner's report: at 425px it costs a
tenth of the width and its glyphs are unlabelled.

**Provenance.** `base.html:41–108`; `components.css:92–166`; owner's screenshots (425×768).

## D6 — The state machine gains one attribute and one refusal

**Decision.** `data-rail` (`closed | open`) joins `data-nav` and `data-ch`; `openLevel2()` refuses
when the width is the phone's and the section is Tata Ibadah; `data-drawer-open` on `<html>` locks
the page's scroll; Escape calls `closeAll()`.

**Rationale.** The existing three states already describe the desktop; the only new level is the
phone's menu, which has no desktop equivalent. The Tata Ibadah refusal is the owner's finding that
its contents rows jump within the page already on screen — a level with nothing to open. The scroll
lock is one attribute the stylesheet reads, rather than a class on two elements.

**Alternatives.** Re-using `data-nav="mini"` for the menu — the mini state means a collapsed panel
and carries its own CSS. A per-page scroll listener — the document-level `overflow: hidden` is one
line and cannot drift.

**Provenance.** `static/web/reading.js:16–17` (the two breakpoint queries), `:1030–1075`
(`syncState`), `:1140–1260` (open/mini/close/rail handlers); owner's review, 2026-10-27.

## Unknowns

None. The breakpoints (≤1272 / ≤720), Escape's reach, the scroll lock and the fixed toolbar were all
settled by the owner at gate 1; everything else is decided above with a source or a measurement.
