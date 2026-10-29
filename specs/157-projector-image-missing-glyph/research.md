# Research: the projector's image placeholder waits for the image to fail

**Spec**: `specs/157-projector-image-missing-glyph/spec.md`
**Unknowns remaining**: 0

## D001 — Toggle the placeholder through the `hidden` attribute, not the property

- **Decision**: `renderImageScreen` sets `missing.setAttribute('hidden', '')` to hide the glyph and
  `removeAttribute('hidden')` to show it; the `.hidden` property is not used on this element again.
- **Rationale**: `hidden` is not on the `SVGElement` prototype chain. A probe in Chromium against a real
  `SVGSVGElement` — `svg.hidden = true` — leaves `hasAttribute('hidden')` `false` and computed `display`
  `block`; the assignment only creates a JS own property. The stylesheet keys on the attribute
  (`projector.css:78`), so the attribute is the mechanism. The same file already does exactly this for
  audio (`projector.js:111`, `:119`), video (`:159`, `:186`) and PDF/slides (`:286`, `:301`) — this slice
  makes the image path stop being the exception.
- **Alternatives considered**: a class (`.is-missing`) — a second mechanism for a state the file already
  spells four times, and it would need a CSS rule to say what `[hidden]` already says; an inline
  `style.display` — defeats the stylesheet and leaves the attribute/state disagreement in place.
- **Provenance**: research — Chromium probe, `getComputedStyle` read, and the four sibling call sites.

## D002 — The markup ships hidden, like every other placeholder

- **Decision**: the image box's `<svg class="screen__image-missing">` gains the `hidden` attribute in
  `projector.html:46`, matching the audio, video, PDF and slides placeholders on the lines below it.
- **Rationale**: with the attribute in the markup, the screen's *pending* state paints nothing even before
  `projector.js` runs — and today it paints the glyph (US1 AC3, measured in the preview's `pending` state:
  `block` on the left, `none` on the right). Relying on the script alone would leave a first-paint leak and
  make the four paths differ again.
- **Alternatives considered**: hide it from the script only — the template would then be the one place
  that says "visible by default", which is the defect; a CSS rule keyed on the parent's state (e.g.
  `.screen__image-box:not(.has-image) svg`) — new state to maintain, and `[hidden]` covers it.
- **Provenance**: research — the four sibling placeholders in `projector.html:47-49` and the CSS rule at
  `projector.css:78`.

## D003 — Leaving a screen clears its failed state

- **Decision**: `clearImageScreen()` (`projector.js:198`) resets the placeholder with
  `setAttribute('hidden', '')` when it drops its host, as `clearVideoScreen()` (`:137-143`) already does.
- **Rationale**: `renderImageScreen` returns early when the active screen is unchanged, so a screen that
  failed keeps the glyph while it is off-screen; a return to it re-renders and would reset it, but the
  screen is also readable in the interval (it stays in the DOM, `aria-hidden`) and the video path already
  states the rule. Two kinds disagreeing about the same state is how the next defect starts.
- **Alternatives considered**: rely on `renderImageScreen`'s own reset on the next visit — true today, but
  it makes correctness depend on a render path that an early return can skip.
- **Provenance**: research — `clearVideoScreen` at `:137-143`, the early return at `:213`.

## D004 — No CSS change

- **Decision**: `static/styles/design/projector.css` is untouched.
- **Rationale**: `[hidden] { display: none }` is already declared for `.screen__image-missing`
  (`:78`), and a `display: none` child takes no space in the flex row, so the picture centres by itself.
  The 40px offset is a consequence of the glyph occupying the flow, not of a rule that needs writing.
- **Alternatives considered**: reduce the glyph's width to 0 when hidden — unnecessary once it is
  `display: none`; absolutely position the glyph — changes the visible state's box, which FR-006 forbids.
- **Provenance**: research — the preview's two boards measured against the frozen stylesheet.

## D005 — One new E2E case, in the module that owns the surface

- **Decision**: add
  `test_projector_loaded_image_shows_no_placeholder` to `tests/e2e/test_image_display.py`, driven exactly
  as its neighbours (`_page(..., available=True)`, Space, `Control+ArrowRight`), asserting the active
  screen's `.screen__image` is visible and its `.screen__image-missing` is not. The existing
  `test_missing_preview_and_projector_icon` keeps its 404 assertion untouched.
- **Rationale**: TDD-06 — one behaviour per case; the loaded state is the behaviour nobody asserted, and
  the failure state is already covered (it passed for the wrong reason, and after this slice it passes for
  the right one without a rewrite). The route stub `_page` already answers 200 with a real PNG, so no
  fixture changes.
- **Alternatives considered**: extend the 404 case with a second scenario — two behaviours in one case,
  and its name would stop describing it; a unit test of `renderImageScreen` — the module is an IIFE with
  no seam, and the repo's convention is Playwright for user-visible acceptance.
- **Provenance**: research — `tests/e2e/test_image_display.py:59-71` (the stub), `:87-117` (both cases).

## D006 — `bump: patch`, declared here and applied at delivery

- **Decision**: `bump: patch`; one `### Fixed` line under `## [Unreleased]`.
- **Rationale**: VER-10 — a fix to shipped behaviour. `VERSION` is `1.22.10` on this base; the number is
  re-read immediately before the merge (VER-04) because sibling slices may take the next patch first.
- **Alternatives considered**: `none` — wrong: the projector's output changes for a user.
- **Provenance**: research — `VERSION`, `CHANGELOG.md`, `docs/PROCESS.md` VER-04/VER-10.

## Open

<!-- empty when Phase 0 is finished; anything here blocks Phase 1 -->
