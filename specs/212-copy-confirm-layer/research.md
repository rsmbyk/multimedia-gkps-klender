# Research — spec 212

Every decision below is grounded in a file read in this worktree or a measurement taken from the
static preview at `specs/212-copy-confirm-layer/preview/`. **Unknowns remaining: 0.**

## D001 — Where the layer's rules live: `components.css`, scoped to the layer

**Decision.** The block goes into `static/styles/design/components.css`, immediately after the existing
`.editor__confirm` rule, and every selector is scoped to `.editor__confirm-layer` — the layer, its card,
its heading, its paragraph and its actions row.

**Rationale.** `.editor__confirm` is a *shared* primitive: `_copy_confirm.html` and
`_generate_modal.html` both emit it, and `generate.css` already styles it — but only through
`.generate__confirm-layer .editor__confirm` and `.choose-layer .editor__confirm`, i.e. scoped to those
two dialogs. A bare `.editor__confirm { … }` rule would therefore land on the generate page's cards as
well. Measured: `generate.css` gives those cards `width: min(440px, 100%)`, `padding: 20px 22px 18px`
and an `h3` at 17px, while this slice's card is `min(468px, 100%)` / `22px` / 18px. Scoping keeps the
two designs independent without touching a surface this slice did not ask about.

**Alternatives rejected.**
- *Put the rules in `generate.css`.* Wrong home: that sheet is the generate page's, and the editor's
  modal is not the generate page's.
- *Un-scope the existing generate rules and share one card.* A visual change to the generate
  confirmation, which no requirement here authorises (spec's Assumptions record it as a separate
  decision).
- *A new stylesheet.* A fifth design sheet for fifteen lines; `components.css` is where `.editor`,
  `.editor__actions` and `.editor__confirm` already live.

**Provenance.** `static/styles/design/generate.css:159–175`; `static/styles/design/components.css:2648`;
`multimedia/web/templates/reading/_generate_modal.html:138–149`.

## D002 — The card's numbers come from spec 167's accepted preview, not from `generate.css`

**Decision.** `width: min(468px, 100%)`, `padding: 22px`, `border-radius: 12px`, `background: var(--canvas)`,
`box-shadow: var(--shadow)`, `h3` at `650 18px/1.25`, `p` at `400 13.5px/1.55`, actions right-aligned
with an 8px gap.

**Rationale.** Spec 167 is the preview the owner accepted for *this* surface, and its `## UI/UX` names
the Copy as template confirmation as part of that surface. The preview's own rules are
`.confirm { width: min(468px, 100%); padding: 22px; border-radius: 12px; … }` and its type at 18px and
13.5px — the numbers above, verbatim. `generate.css`'s card is the same shape at a different scale
because the generate dialog is an 840px frame and the editor is a 480px one.

**Alternatives rejected.** Copying `generate.css`'s 440px / 20px 22px 18px / 17px card would have made
the two confirmations identical in source but left this one 8px narrower than the design that was
approved for it.

**Provenance.** `specs/167-tata-ibadah-templates/preview/preview.css:153–173`;
`specs/167-tata-ibadah-templates/spec.md` §UI/UX (the Edit modal, 480px).

## D003 — The scrim restates the dialog's 14px radius

**Decision.** `border-radius: 14px` on `.editor__confirm-layer`, written as a literal.

**Rationale.** Measured in the preview: `border-radius: inherit` resolves to **0px**, because the
layer's parent is `.editor__body` (no radius), not the `<dialog>`. Without a radius the scrim squares
off the dialog's corners while the confirmation is up — visible against the page behind. 14px is
`.editor`'s own radius (`components.css:516`), so the two move together by hand; a `--radius-dialog`
token would be the durable fix and is not this slice's to introduce.

**Alternatives rejected.** Leaving the scrim square (the preview drew it square, inside a mockup whose
dialog was a `div` with its own overflow clipping — the product's `<dialog>` does not clip).

**Provenance.** preview probe, `layer.border-top-left-radius`: `0px` under `inherit`, `14px` under the
literal.

## D004 — The verification seam is a Playwright E2E, not a unit test

**Decision.** Two new tests in `tests/e2e/test_tatib_templates.py`, in the existing
`TataIbadahTemplateE2ETests` class: `test_the_copy_confirmation_covers_the_form` and
`test_the_copy_confirmation_card_matches_the_preview`.

**Rationale.** The behaviour is computed layout inside a live `<dialog>` — `position: absolute` against
a `position: fixed` ancestor, a scrim's stacking over a form, and `elementFromPoint` resolving to the
layer rather than to the button. No unit seam can see any of it: the rules are CSS, and the only thing
that resolves CSS is a browser. The repo's TDD block already declares user-visible acceptance as
Playwright E2E through `StaticLiveServerTestCase`, and this suite is where the copy flow's existing
test lives.

**Alternatives rejected.** A Python test asserting the stylesheet's text would pass with the rule in
the wrong cascade layer or overridden by a later rule — it certifies the source, not the render.

**Provenance.** `docs/PROCESS.md` §Tests `repo:` block; `tests/e2e/test_tatib_templates.py:30`,
`:829` (`test_copy_as_template_asks_and_copies`).

## D005 — No motion is added

**Decision.** The layer appears at once; no transition, no animation.

**Rationale.** Spec 167's preview has no transition on `.confirm-layer`, and the accepted `## UI/UX`
records none. A fade would be a behaviour nobody asked for and a second thing to verify.

**Provenance.** `specs/167-tata-ibadah-templates/preview/preview.css:153–173` (no `transition` /
`animation` property in the block).

## D006 — `hidden` is re-stated on the layer

**Decision.** `.editor__confirm-layer[hidden] { display: none; }`

**Rationale.** The layer carries `display: grid` from this slice. An author `display` declaration beats
the user agent's `[hidden] { display: none }`, so without the restatement the confirmation would paint
on every editor open — the same trap `.editor:not([open])` documents for the dialog itself
(`components.css:524–527`). Measured in the preview with the layer's `display: grid` present and only
this restatement absent: `hidden` set, `getComputedStyle(layer).display` = **`grid`**; with the
restatement, **`none`**.

**Provenance.** `static/styles/design/components.css:524–527`; preview probe on the first candidate.
