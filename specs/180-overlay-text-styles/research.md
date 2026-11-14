# Research: the overlay reads by kind

**Spec**: `specs/180-overlay-text-styles/spec.md`
**Unknowns remaining**: 0

## D001 — The kind comes from the projector's data island, not from a new endpoint

- **Decision**: the overlay reads `projectorEntryData` (already embedded in `/obs/source/projector`), finds the entry
  whose `start..end` holds the live screen index, and takes its `type` (`song` · `passage` · `text` · `media` ·
  `break`) as the paint mode. `overlay.js` fetches that page once per service and caches it.
- **Rationale**: the overlay is listen-only and already fetches the projector page for the screen model; the kind was
  sitting in the same response, one island away. No new request, no new cache key, no server change.
- **Alternatives considered**: a JSON endpoint per service — a second request and a second cache to invalidate for
  data that already arrives; reading the DOM of the projector page — the kind is carried as `data-*` on rows, not on
  the painting element, so it would have meant scraping a page rendered for people.
- **Provenance**: research (`multimedia/web/reading/views.py::_projector_data`, `projector.html` islands).

## D002 — Two objects with different structure, not one plate with two headings

- **Decision**: a passage is a centred quotation card with a rounded corner; a liturgy is a left-aligned script panel
  with a bar on its leading edge and a near-square corner.
- **Rationale**: the two things are opposite in kind — a quotation is a whole object read as one voice, a liturgy is a
  script spoken in turns. One plate with two headings only renamed them.
- **Alternatives considered**: a single shared plate — offered first and rejected by the owner as the wrong shape.
- **Provenance**: owner decision (review of the first preview).

## D003 — One number drives the plate's whole type scale

- **Decision**: `font-size: clamp(5.5px, 1.875cqw, 40px)` on the plate (36 px at 1920, exactly half the caption's
  72 px), and every inner size in `em` of it: title `.808em`, kicker `.5em`, rule gaps `.38em` / `.54em`, line gap
  `.3em`.
- **Rationale**: the surface has to hold at 720p, 1080p and 4K without a media query; container units do that, and one
  base number keeps the hierarchy intact when the owner turns a single knob.
- **Alternatives considered**: fixed px per breakpoint — three sets to keep in step, and the ratios drift; `rem` with a
  root scale — the overlay is not the document root inside OBS.
- **Provenance**: research, then owner tuning of the individual ratios during review.

## D004 — The speaker column travels in the data

- **Decision**: `_screen_lines()` carries `mark` (the speaker token, e.g. `L.`, `Pelayan :`) and `words` beside the
  full line the projector paints; the overlay lays each marked line as a two-column grid and sizes the column to the
  widest mark on that screen.
- **Rationale**: 133 distinct marks are stored in the database, so no CSS indent can be exact — a hanging indent needs
  the mark's own width, and the screen needs one column for all of its turns.
- **Alternatives considered**: `padding-left` + negative `text-indent` with an assumed mark width — fails on any mark
  wider than the guess (`Pelayan :` is 155 px at 36 px type); splitting the string in the browser on a regex — the
  stored text is free-form and a mark like `P + K:` has no single delimiter.
- **Provenance**: research (`multimedia/web/reading/voices.py`, the stored Tata Ibadah text).

## D005 — Motion as CSS animations on a class, with a fallback settle

- **Decision**: entering and leaving are two keyframes on `.is-entering` / `.is-leaving`; the script adds the class,
  removes it on `animationend`, and keeps a 600 ms timer that removes the node if the event never arrives. A
  `prefers-reduced-motion` media query disables both.
- **Rationale**: the paint path is state-driven and can be called repeatedly; classes keep the animation declarative
  and the reduced-motion branch free. The timer is the only defence against a throttled tab leaving a stale panel up.
- **Alternatives considered**: the Web Animations API — more control, but the same keyframes end up in script and the
  reduced-motion branch becomes manual; a CSS transition on a state class — a transition cannot run when the node is
  created and removed in the same frame.
- **Provenance**: research.

## D006 — A same-kind step morphs the box instead of re-entering

- **Decision**: when the next screen is another panel of the same entry, the panel keeps its place and transitions its
  own width and height from the old measure to the new one over 180 ms, with the words resolving inside it after
  110 ms. A caption step simply swaps its words.
- **Rationale**: stepping verses is one continuous reading; an object that blinks out and back between verses reads as
  a fault. The hold on the words stops the new lines from re-wrapping while the card is moving, which is what the
  first attempt looked like.
- **Alternatives considered**: re-flowing the text during the resize — visible as jitter at 180 ms; re-entering the
  panel per screen — breaks the reading into flickers; freezing the text at its final width with a clip — reads as a
  window opening, and the card's own border gets clipped with it.
- **Provenance**: owner request ("can you also morph the panel resize"), then measured against captured frames.

## D007 — Hierarchy by ink, not by weight

- **Decision**: the tip of the scale is weight and the quiet end is ink: assembly full `#F6F7F5`, joined
  `rgba(255,255,255,.8)`, leader `rgba(255,255,255,.381)`.
- **Rationale**: on a dark card, thinning a font at 36 px to 350 weight costs legibility at stream bitrates; alpha
  keeps the glyph shapes and still separates the voices.
- **Alternatives considered**: lower font weights — the faces thin unevenly over video; italic and size — already
  spent on the title and the kicker.
- **Provenance**: owner decision, tuned twice by eye against the live frame.

## D008 — The song keeps the caption exactly as it is

- **Decision**: the song path is the pre-existing caption, unchanged in type, ink, outline and position.
- **Rationale**: it is the surface the congregation already reads every week, and a lyric is a subtitle.
- **Alternatives considered**: giving songs a plate too, for consistency — rejected by the owner in the first review.
- **Provenance**: owner decision.

## Open

<!-- empty: Phase 0 finished, no unknowns carried into design -->
