# Research: The landing search field sits on the window's middle

**Slice**: `specs/139-home-search-center` · **Date**: 2026-10-27
**Exit**: zero unknowns.

## D1 — Three grid rows, not a compensating padding

**Decision.** `.search-home__inner` becomes `display: grid` with
`grid-template-rows: 1fr auto 1fr`; the logo takes row 1 aligned to its end, the form row 2, row 3 stays
empty. The form's own box is then the section's middle by construction.

**Rationale.** A grid's `auto` row is positioned by the free space around it, so the middle row lands on
the container's middle whatever the logo measures. Today's flex `align-items: center` centres the
*block*, which is what puts the field 61px low — half of the 96px logo plus its 26px gap.

**Alternatives.** (a) `padding-bottom: calc(96px + 26px)` on the inner so the flex-centred block's
middle coincides with the form's — works, but hardcodes the logo's height twice (the logo rule and the
padding) and silently breaks the day the logo is resized; the design already carries the logo size in
one place. (b) `position: absolute` on the form with `top: 50%` — removes it from flow, so the shadow's
box and the focus ring stop being the layout's business and a short window clips the logo before the
form would move. (c) `transform: translateY(-61px)` — paints the field off its own layout position, so
hit-testing, the caret and `getBoundingClientRect` disagree with the paint. (d) Making the field the
section's only flex child and taking the logo out of flow — loses the 26px gap's relationship to the
form and makes the logo overlap the top of a short window.

**Provenance.** Measured on the rendered landing page (Chromium, `preview/probe_preview.py`): today's
field centre 499 at 1440×900 (window 450); with the three rows, 450 at all eight widths tested.

## D2 — The section measures the stage's real paddings, via two tokens

**Decision.** `.stage` declares `--stage-pad-top: var(--pad-top)` and `--stage-pad-bottom: 64px` and
uses them in its own `padding`; the phone block sets `--stage-pad-top: calc(var(--topbar-h) + 18px)`.
`.search-home` computes `min-height: calc(100svh - var(--stage-pad-top) - var(--stage-pad-bottom))`.

**Rationale.** The section can only centre on the window if it exactly fills the box the stage leaves
it, and that box is the stage's own paddings. Today the section repeats the literal `--pad-top` in its
`min-height` while the phone layout pads `--topbar-h + 18px` (76px) — so below 720px the section is 36px
taller than its space, and its middle sits 24px low before the logo block's own 61px is counted. That is
the second half of the phone's +85px.

**Alternatives.** `min-height: 100%` — resolves against the stage's content box only while the stage's
height is definite (it is a stretched flex item, so Chromium agrees), and depends on a percentage
resolving against a flex item in every engine the team uses; the `svh` calculation states the
relationship instead of relying on it. A JS measure-on-load — a layout number that needs a script is a
number that is wrong before the script runs and again on every resize.

**Provenance.** `static/styles/design/components.css`: `.search-home` (line 956, `min-height:
calc(100svh - var(--pad-top) - 64px)`), `.stage` (line 1694), the phone block (line 2897,
`padding-top: calc(var(--topbar-h) + 18px)`). Measured: 390×844 today, the section is 740px tall in a
704px space and its middle is 446 against the window's 422.

## D3 — A signed margin cancels the stage's asymmetry; padding cannot

**Decision.** `[data-home="landing"] .search-home__inner { margin-top:
calc(var(--stage-pad-bottom) - var(--stage-pad-top)) }` — +24px at desktop (top 40, bottom 64), −12px
under 720px (top 76, bottom 64).

**Rationale.** Even with a correctly sized section, its middle is the content box's middle, which sits
`(bottom − top) / 2` above the window's. On a stretched grid item a margin moves the box's edges, so
half the margin lands on the middle row's position: +24 shifts the form down 12, −12 shifts it up 6.
A margin is the only one of the box properties that takes a negative value, which is exactly what the
phone layout needs.

**Alternatives.** Padding on the section (positive only): fine at desktop, wrong at ≤720px where the
correction is upward — the phone would stay 6px high. A hardcoded `margin-top: 24px`: correct until a
layout moves the top padding, which the phone block already does. `align-content` on the section: shifts
the whole grid, not the middle row, and takes no negative.

**Provenance.** Measured after each variant on the rendered page and on the static preview: the margin
form reads 0.0px at all eleven widths; `min-height: 100%` + the same margin reads the same, and is kept
only as the rejected alternative in D2.

## D4 — Scoped to the landing state

**Decision.** The margin rule is qualified by `[data-home="landing"]`; the base `.search-home` rules
apply in every state.

**Rationale.** The same section draws the compact bar above a results list, where `[data-home="results"]
.search-home { min-height: 0; padding: 6px 0 26px }` makes the box auto-height. In that state the grid's
free rows collapse and the margin would add its 24px to the bar's height — a results bar 24px taller,
with the list pushed down by the same amount. Qualifying the one rule keeps the results view exactly
where spec 004 put it.

**Alternatives.** `[data-home="results"] .search-home__inner { margin-top: 0 }` — an override of a rule
that should not apply; the guard is clearer stated on the rule itself. Moving the margin onto
`.search-home__form` — a margin on a grid item in a fixed row does not move the row.

**Provenance.** Measured: at 1440×900 the results bar is 88px tall, field top 46, results top 128, both
before and after; unqualified, the bar measures 112px and the list moves to 152.

## D5 — Verification is geometry at eleven widths

**Decision.** A new E2E module measures `getBoundingClientRect()` centres against `innerHeight / 2`, the
document's `scrollHeight`/`scrollWidth` against the window's, and the logo's gap, at 1920×1000, 1440×900,
1280×800, 1272×800, 1024×768, 834×1112, 721×900, 720×900, 600×800, 390×844 and 320×568 — plus the
results and reading views' invariants.

**Rationale.** "Centred" is a relationship between two boxes, and this slice's defect is three offsets
that compose; only numbers show which one moved. The widths straddle both layout switches (1272, 720) so
the phone overhang of D2 cannot hide behind the drawer breakpoint, and 721/720 is the pair that proves
the boundary.

**Alternatives.** A style assertion (`min-height` equals …) — proves the declaration, not the centring.
A screenshot comparison — the pixel tools in this repository are for painted glyphs, and this is a
position, which a rect measures exactly.

**Provenance.** `preview/probe_preview.py` (already run: same numbers at all widths), and the repository's
existing E2E geometry patterns (`tests/e2e/test_text_wrap.py`, `tests/e2e/test_drawer_shell.py`).

## Unknowns

None. Which element is centred, how the section measures its space, how the asymmetry is cancelled, how
the results state is kept, and how the claim is verified are all decided above with a source or a
measurement.
