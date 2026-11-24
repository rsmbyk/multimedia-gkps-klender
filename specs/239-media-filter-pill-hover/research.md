# Research: Media Library filter-pill hover

**Spec**: `specs/239-media-filter-pill-hover/spec.md`
**Unknowns remaining**: 0

## D001 — Selector and cascade position

- **Decision**: add `.media-library__chips button:not([aria-pressed="true"]):hover` with
  `border-color: var(--focus); background: var(--icon-hover-bg);` beside the base and
  pressed pill rules in `static/styles/design/components.css`.
- **Rationale**: the base rule is specificity 0-1-1 and the pressed rule 0-2-1. A bare
  `button:hover` would also be 0-2-1 and, placed after the pressed rule, would paint a
  pressed pill with the hover fill; the `:not()` guard raises it to 0-3-1 and limits it
  to unpressed pills regardless of order. The measured live values are the gate-1
  numbers in `spec.md §UI/UX`.
- **Alternatives considered**: a global button hover would change the sort and dialog
  buttons; adding a new class to the template would touch markup for a style-only
  change; putting the declarations on the pressed rule would need an override anyway.
- **Provenance**: `components.css:636-637` in the slice worktree; gate-1 probe
  `preview/probe.py`, which reads the shipped selector from the same-origin stylesheet.

## D002 — The hover pair is already the app's control hover

- **Decision**: reuse `--focus` for the border and `--icon-hover-bg` for the fill.
- **Rationale**: the Media Library's sort trigger and head icon buttons use exactly that
  pair (`components.css:607`), as do the OBS dock's chip, bait and nav controls
  (`obs-dock.css:769`, `:815`, `:837`). Both tokens already resolve in light and dark
  themes, so no new token or theme branch is needed.
- **Alternatives considered**: a tinted `color-mix()` like the old spec-103 preview
  would introduce a second chip vocabulary; an underline would not match any other
  pill in the app.
- **Provenance**: token definitions in `static/styles/design/tokens.css:25,29,40,92,93,107`;
  measured hover values in `spec.md §UI/UX`.

## D003 — No transition

- **Decision**: swap the two colours directly; do not add `transition` or an animation.
- **Rationale**: the neighbouring sort and icon buttons swap on hover without a
  transition, and spec 109 explicitly added no new animation to this filter row.
  Nothing is introduced for reduced-motion mode to suppress.
- **Alternatives considered**: a 120ms ease would make one pill behave differently from
  the buttons beside it and need a reduced-motion override.
- **Provenance**: `components.css:607`, spec 109 §UI details; gate-1 assumption in
  `spec.md §Assumptions`.

## D004 — Verification depth before the push step

- **Decision**: write one targeted E2E module; run it and the full browser suite at the
  push step, not between pushes.
- **Rationale**: a two-declaration CSS change has a narrow blast radius, and the owner's
  standing preference defers heavy browser suites to the push step. The gate-1 probe
  supplies the in-between evidence without a suite run.
- **Alternatives considered**: running the whole E2E suite now would repeat unrelated
  base failures and add no evidence for this rule.
- **Provenance**: owner decision; research inconclusive.

## D005 — Live preview and control measurement

- **Decision**: keep the live worktree page as the preview; the probe deletes only the
  new rule from a second page's CSSOM to obtain the before numbers.
- **Rationale**: the page's markup and theme tokens are server-rendered, and the hover
  must be produced by a real pointer on the real pills; a copied stylesheet could drift
  from the shipped rule. The control page reads the same shipped selector before its
  CSSOM deletion, as recorded by the probe.
- **Alternatives considered**: a static page would duplicate the filter row and its
  tokens; a screenshot cannot show a hover state; injecting a fix into an otherwise
  broken page would misrepresent what is shipped.
- **Provenance**: live preview at `127.0.0.1:8767`, `preview/README.md`, gate-1 probe
  output in `spec.md §UI/UX`.

## Open

None.
