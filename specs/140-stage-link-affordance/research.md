# Research: The stage's entry links read as text until hovered

**Spec**: `specs/140-stage-link-affordance/spec.md`
**Unknowns remaining**: 0

## D001 — The rule targets `.entry__jump`, not the anchor element

- **Decision**: change only the stage entry-title link's rule in `components.css`; no global
  `a { … }` selector.
- **Rationale**: the request's screenshot shows the Tata Ibadah stage's song and passage titles, and
  spec 056 already rejected a global anchor rule when it introduced the colour. Every other link in
  the product has its own treatment — search results underline on row hover, the media library's
  "used by" links wear `--link`, sidebar rows are rows — and a global rule would silently restyle
  them all.
- **Alternatives considered**: a base `a` rule with per-component opt-outs, which trades one visible
  change for an audit of every anchor in the templates; rejected as unrequested work with a wider
  blast radius.
- **Provenance**: research.

## D002 — The resting colour is `inherit`, not a new token

- **Decision**: `.entry__jump { color: inherit; }`.
- **Rationale**: the link sits inside `.read[data-kind="tatib"] .read__sec`, which already sets
  `color: var(--ink)`; inheriting keeps the title identical to its heading by construction, in both
  themes, and adds no token to maintain. Measured: `rgb(31,31,29)` light, `rgb(245,243,238)` dark,
  15.16:1 and 16.76:1 on the canvas.
- **Alternatives considered**: a `--stage-link-ink` token duplicating `--ink` — a second source of
  truth for the same value; or `color: var(--ink)` directly on the rule — also correct but it would
  override a future heading colour instead of following it.
- **Provenance**: research.

## D003 — The underline is the state, on pointer and keyboard alike

- **Decision**: `text-decoration: underline; text-underline-offset: 3px;` on `:hover` and
  `:focus-visible`; `text-decoration: none` at rest.
- **Rationale**: with no colour and no resting line, the underline is the only cue that the text is a
  link, so it must appear for both input methods or the link is invisible to a keyboard user.
  `:focus-visible` — not `:focus` — keeps a mouse click from leaving a line behind, which is the
  same reason the repository uses it elsewhere. The 3px offset is the value
  `.result-row:hover .result-row__title` already uses, so two hover cues in the product agree.
- **Alternatives considered**: `:focus` (draws after a mouse click and reads as a stuck state);
  a colour change on hover (the request names the underline as the change); an animated underline
  (motion the request did not ask for).
- **Provenance**: research, with the owner's request fixing the underline as the only state change.

## D004 — `--link` survives, with an honest comment

- **Decision**: keep `--link` in both theme blocks and its `('--link', '--canvas')` pair in
  `tests/test_design_tokens.py`; update the two comments from "stage entry links (spec 056)" to the
  media library's usage.
- **Rationale**: `.media-library__uses a` still reads `var(--link)`, so the token is live and its
  AA pair still guards a real surface. Deleting it would break that rule; leaving the comment would
  document a use that no longer exists.
- **Alternatives considered**: removing the token and repainting the media library links — an
  unrequested change to another surface.
- **Provenance**: research.

## D005 — The existing E2E test is rewritten, not duplicated

- **Decision**: replace `test_tatib_stage_entry_links_follow_the_theme` in
  `tests/e2e/test_reading.py` with a test of the new behaviour, in the same class and fixture.
- **Rationale**: the old test asserts the retired colour; a second test beside it would assert the
  opposite of the first. TDD-07 allows deleting/rewriting a test when the behaviour it names is gone
  — here the behaviour is deliberately replaced, and the test name changes with it.
- **Alternatives considered**: adding a new module for one test — the surrounding class already owns
  the reading-page theme assertions.
- **Provenance**: research.

## D006 — The controls hold a column of their own; icons while the pane is narrow

- **Decision**: `.read__body` is a named inline-size container (`stage-pane`);
  `.tatib__item--acts` reserves 264px of column from 700px of pane and 106px below it. The labels
  collapse to icons under 700px and stay in the accessibility tree by being visually hidden rather
  than removed. Each control's word is wrapped in `.entry__ctrl-label` in `tatib.html` so one rule can
  collapse it.
- **Rationale**: the owner's direction — labels wherever there is room, icons where there is not —
  and the measurement of what "room" means. The first attempt keyed on the window (labels from 721px),
  which measured badly: at a 1440px window with both sidebars open the reading pane is 400px, so
  reserving the labels' 264px left 144px for the title and every entry on `/tatib/144/` wrapped
  (`Kisah Para / Rasul 1:1`, `images.jp / eg`, `Receipt- / 2773- / 9204.png`, six lines for the long
  title). A container query asks the pane itself, which is the width the words actually get. After the
  change: 1440px window, pane 400px — icons, 27px buttons, 106px column, the title on one line, ending
  at 1153px with the controls at 1281px; 1920px window, pane 880px — labels, 252px of buttons, 264px
  column, title ends 1153px, controls begin 1606px; 390px phone — icons, title 20–176px, controls
  277–374px.
- **Alternatives considered**: window media queries at 721px (the first attempt — it reserves 60% of
  a real 400px pane and wraps every title); icons at every width (the owner rejected it: the labels
  are clearer where there is room); no reservation with the underline triggered by the row's hover
  (keeps labels everywhere, but the labels still sit over the title's end while shown, and the cue
  fires from the whole row rather than the link).
- **Provenance**: owner decision, 2026-10-27; threshold and figures measured on the slice.
