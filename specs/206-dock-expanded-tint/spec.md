# Spec 206: A whisper of a tint on an open entry header

- **ID:** 206
- **Status:** Accepted — gate 1, 2026-11-19, at 4 % (the four strengths were shown as static panes of the real dock at 400 px; 3 % and 6 % declined)
- **Item:** ITEM-214
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

An entry header in the OBS dock carries one mark of its open state: a 15 px chevron at the trailing
end of the row. The owner asked the header itself to say so as well — a background wash on the
expanded header that is "really soft as to not actually noticeable by the operator but clearly show
that the entry is being expanded".

The wash is **4 % of the ink colour mixed into the rail**. In the light theme the generic hover face
is the same ink at 8 %, so the pointer lands exactly twice as far from the rail as the wash does; in
dark the face is 9 % white and the wash 4 % near-white, slightly under half. Either way the pointer
stays the loudest state on a row, the live entry keeps its selected fill, and a list of closed headers
still reads as bare rail. The tint is a state, not a transition: it belongs to a header for as long as
its block is open.

## Scope

### In scope

- One rule in `static/styles/design/obs-dock.css` for `.entryrow[aria-expanded="true"]`.
- The capability rule and its scenario in `docs/spec/dock.md` R14 (at Fold).
- E2E coverage of the open tint, its hover replacement and the live row's exemption, in
  `tests/e2e/test_obs_dock.py` beside the spec 198 state tests.

### Out of scope

- The block's own content surface (`.entryinner`, its body and screen rows) — the request names the
  header, and the block already reads as the opened thing.
- The chevron's stroke, size, rotation or placement (spec 198, FR-003/FR-010).
- Any hover, focus, current or pressed tone that already exists — none is adjusted.
- The reading page's sidebars and the projector: `.entryrow` exists only in the dock.
- JavaScript: `aria-expanded` is already kept truthful by spec 198's `paintEntry`, so no state is
  added, cached or mirrored.

## Domain rules

- **The tint is 4 % ink in the rail.** `color-mix(in srgb, var(--rail-bg) 96%, var(--ink))` — the
  same expression the sheet uses for the Next band's hover, one step softer
  (`docs/spec/dock.md` R14 modified).
- **Hover is stronger, and replaces rather than adds.** The open rule sits before `.entryrow:hover`;
  both weigh (0,2,0), so an open header under the pointer shows the generic hover face and nothing
  else.
- **The live row is never tinted.** It always carries `aria-expanded="true"` while its block is open,
  so its `aria-current="true"` rule sits after the open rule and keeps
  `--sidebar-selected-bg`, with its own hover tone on top.
- **The state is the attribute, not a class.** The rule reads `aria-expanded`, the same attribute the
  chevron rotates on and the row already exposes to assistive technology.
- **No new transition.** The tint rides `.entryrow`'s existing `background var(--ease)` and adds no
  motion of its own; reduced motion is unchanged.
- **The whole line carries it.** The chevron lives inside the row, so it sits on the tinted face
  exactly as it already sits on the hover face — no new element, padding or radius.
- **R14 keeps its other clauses.** The header's toggle, its chevron and its live-row fill all stand
  unchanged; this slice adds one clause to the header's painted state, it does not rewrite the rule.

## User Scenarios & Testing

### US1 — The open blocks are readable at a glance (P1)

**Why this priority**: it is the whole request. The chevron asks the eye to travel to the row's far
end and read a 15 px angle; a wash on the header makes an open block read as one object from across
the panel without the operator aiming at anything.

**Independent Test**: a dock with two entries open and the rest closed, at rest, in both themes —
the two open headers carry the tint, every closed header carries none, and the pointer's face is
still visibly stronger than the tint.

**Acceptance scenarios**

1. **Given** a collapsed header **When** its block is opened **Then** the header's background settles
   to the open tint over the row's 200 ms ease and holds it for as long as the block stays open.
2. **Given** an open header at rest **When** the operator reads the list **Then** the header is a
   flat, full-line wash that is softer than the hover face and distinguishable from bare rail in
   both themes.
3. **Given** an open header at rest **When** the block is closed **Then** the tint leaves on the same
   200 ms ease and the header is bare rail again.
4. **Given** the live entry with its block open **When** the list is read or the pointer crosses it
   **Then** the header keeps `--sidebar-selected-bg` at rest and its selected hover tone under the
   pointer, and never paints the open tint.

### US2 — The pointer stays the loudest state on a row (P2)

**Why this priority**: the tint is permanent while a block is open; the pointer is transient and
must not be mistaken for it. If the two tones were close, the operator would lose hover feedback on
every open header — which is most of them, in a service being worked through.

**Independent Test**: with an entry open, hover its header and a closed header side by side; both
paint the identical hover face, and that face is a visibly larger step from the rail than the tint.

**Acceptance scenarios**

1. **Given** an open header **When** the pointer enters it **Then** the background becomes the
   generic hover face, not a blend of the tint and the hover face.
2. **Given** the pointer leaves an open header **Then** the background returns to the open tint, not
   to bare rail.
3. **Given** the live entry, open or closed **When** the pointer enters it **Then** the header shows
   its own selected hover tone, and never the generic face or the open tint.

### Edge Cases

- **When** a section-break row or an entry with an empty block is displayed **Then** it carries no
  `aria-expanded` (spec 198, FR-010) and paints no tint — no guard is needed in this slice.
- **When** a live-entry crossing swaps which block is open **Then** the two headers' attributes flip
  with the crossing and their washes follow on the row's own ease; the 230 ms morph is not given a
  new tint rule of its own.
- **When** the theme is switched **Then** the tint re-derives from the new `--rail-bg` and `--ink`
  through the existing 380 ms theme-morph transition on `.entryrow`.
- **When** the dock is viewed in dark mode **Then** the wash is the same 4 % of the near-white ink
  over the dark rail, not the light theme's literal colour.
- **When** the page runs under `prefers-reduced-motion: reduce` **Then** the tint behaves as the
  row's background already does — this slice adds no transition, so no new reduce rule is owed.

## Functional requirements

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | An entry header whose `aria-expanded` is `true` SHALL paint `color-mix(in srgb, var(--rail-bg) 96%, var(--ink))` as its background at rest | `dock/R14` modified |
| FR-002 | A header that is not expanded SHALL paint no background of its own — the row's `background: none` base stands | `dock/R14` modified |
| FR-003 | The open rule SHALL precede `.entryrow:hover` and `.entryrow[aria-current="true"]` in source order, and introduce no selector weight above (0,2,0), so the pointer and the live state each outrank the tint | `dock/R14` modified |
| FR-004 | An open header under the pointer SHALL paint the generic hover face (`--icon-hover-bg`) alone — the tint SHALL NOT be composited with it | `dock/R14` modified |
| FR-005 | The live entry's header SHALL keep `--sidebar-selected-bg` at rest and its selected hover tone under the pointer, whether or not its block is open | `dock/R14` modified |
| FR-006 | The tint SHALL cover the header's full painted line, chevron included, by inheriting the row's background — no new element, no change to padding, radius or height | `dock/R14` modified |
| FR-007 | The tint SHALL add no transition or animation of its own; it SHALL ride the row's existing `background var(--ease)` | `dock/R14` modified |
| FR-008 | The rule SHALL key on `aria-expanded` only — no class, data attribute or JavaScript state is added, so a header that cannot open can never be tinted | `dock/R14` modified |

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | At rest, an open header's computed background is exactly the 4 % rail-and-ink mix in both themes, and a closed header's is the row base | E2E: computed-style equality against a probe built from the same expression, light and dark |
| SC-002 | An open header under the pointer computes to `--icon-hover-bg`, exactly as a closed one does | E2E: hover each, compare both computed values to the token |
| SC-003 | The live entry's header, open and under the pointer, computes to its selected hover tone and never to the open tint or the generic face | E2E: the existing spec 198 live-row assertions extended |
| SC-004 | No other dock state changes: closed headers, break rows, empty entries, sticky behaviour and the chevron's transform all read as before | E2E: the spec 198 suites stay green with no assertion edited |
| SC-005 | The tint is a smaller step from the rail than the hover face, in both themes | E2E: the channel deltas of the two computed values, compared in both themes (the 8-level vs 16-level step) |

## UI/UX

- **Base surface.** `.entryrow` sits directly on `.dock`'s `--rail-bg`: `#EDEAE3` light, `#232019`
  dark (`static/styles/design/tokens.css`).
- **Open tint.** `color-mix(in srgb, var(--rail-bg) 96%, var(--ink))`:
  - light — `#E5E2DB`, an 8-level step from the rail on each channel;
  - dark — `#2B2822`, an 8–9-level step.
- **Hover face, for reference.** `--icon-hover-bg` = `rgba(31, 31, 29, .08)` light / `rgba(255, 255,
  255, .09)` dark:
  - light — `#DDDAD3`, a 16-level step, exactly twice the tint's;
  - dark — `#37342E`, a 20-level step.
- **Live row.** `--sidebar-selected-bg` `#B9D7C9` light / `#393F4F` dark — untouched, and it is a
  family change, not a step, so it outranks both.
- **Alternatives offered at gate 1.** 3 % ink (`#E7E4DD`, a 6-level step — the floor of "visible
  at all") and 6 % (`#E1DED7`, a 12-level step — three quarters of the way to hover, which risks the
  pointer reading as weaker than it is).
- **Type and contrast.** No text colour changes: ink on the tint reads 12.76:1 light and 13.25:1
  dark (from 13.74:1 and 14.66:1 on bare rail), so the wash costs legibility nothing.
- **Order in the cascade.** base `.entryrow` → `.entryrow[aria-expanded="true"]` →
  `.entryrow:hover` → `.entryrow[aria-current="true"]` (→ `:hover`), the last two unchanged and
  already beyond (0,2,0) or later in source.
- **Motion.** Inherited: 200 ms `cubic-bezier(.32, .72, .28, 1)` — the same curve and duration the
  chevron flips on. No new reduce rule.
- **Preview.** static preview at `specs/206-dock-expanded-tint/preview/index.html` — the real
  `tokens.css` and `obs-dock.css` plus the real rendered dock markup from `/obs/dock`, with the open
  tint switchable between 0 %, 3 %, 4 % and 6 %, a forced hover face and the live row on screen, in
  both themes.

## Assumptions

- **"Being expanded" is the state, not the 230 ms crossing.** The tint belongs to a header while its
  block is open, and is not a flash that accompanies the morph.
- **The header only.** The block beneath keeps its own surface; the request says the entry's header,
  and tinting the block as well would turn the run of screen rows into one panel.
- **The pointer replaces the state's tone rather than adding to it.** A blend would need a second
  tone for "open and hovered", which the dock has never had for any other pair of states.
- **4 % is the accepted softness.** Chosen by the owner at gate 1 (2026-11-19) from the three
  previewed strengths; 3 % and 6 % were shown and declined. It reads "really soft" as half the
  existing hover step.
- **The live row outranks the open state**, as it already outranks hover and `aria-current` — the
  operator's position in the service is never repainted by a disclosure state.
- **No new token.** Only one rule consumes the value; a token would name a number that nothing else
  shares, and `.nextband:hover` sets the precedent of the expression living at the rule.
- **The dock does not opt into forced-colours**, so no system-colour fallback is owed here.

## Traceability

- Capability: `docs/spec/dock.md` R14 (modified at Fold).
- Implementation: `static/styles/design/obs-dock.css` (one rule, between `.entryrow` and
  `.entryrow:hover`).
- Verification: `tests/e2e/test_obs_dock.py`, beside the spec 198 state tests.
- Preview: `specs/206-dock-expanded-tint/preview/index.html`.
