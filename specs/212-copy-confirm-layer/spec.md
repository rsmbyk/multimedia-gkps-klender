# Feature Specification: the Copy as template confirmation is a layer of the edit modal

**Slice**: `specs/212-copy-confirm-layer`
**Branch**: `fix/212-copy-confirm-layer`
**Created**: 2026-11-21
**Status**: Draft
**Input**: "what is this? the layout is broken" — a screenshot of the Edit template modal with both the form and the Copy as template confirmation painted in the same flow (production, 2026-11-21).

## User Scenarios & Testing

### US1 — The confirmation covers the form instead of stacking under it (P1)

**Why this priority**: today the confirmation is a block in the modal's own flow, so pressing Copy as template grows the modal from 241px to 477px, pushes the form's own Save/Cancel up out of view and paints a second, left-aligned pair of the same labels under it. The state reads as a broken dialog, and the person cannot tell which Save belongs to what.
**Independent Test**: open a template's Edit modal, press **Copy as template**: one card over a dimmed form, its two answers right-aligned; the form's own Save is no longer reachable.

**Acceptance scenarios**

1. **Given** the Edit modal of a template **When** **Copy as template** is pressed **Then** the confirmation renders as a card centred over the modal, on a scrim that covers the whole dialog, and the modal's own height does not change.
2. **Given** the confirmation is up **When** the form's **Save** is clicked **Then** the click lands on the confirmation, not on Save — the form underneath is inert.
3. **Given** the confirmation is up **When** **Cancel** is pressed **Then** the layer hides, the form is visible and operable again, and nothing else about the modal moved.
4. **Given** the confirmation is up **When** the modal's rounded corners are inspected **Then** the scrim follows the dialog's 14px radius rather than squaring it off.

### US2 — The card reads as the preview that was accepted (P2)

**Why this priority**: spec 167's preview is what the owner accepted for this surface; the product sheet never received the confirmation's rules (the same miss that ITEM-201 fixed for the header). Without them the card has no fill, no radius, no shadow, and its heading falls back to the browser's `h3`.
**Independent Test**: the confirmation's card measures 448 × 176.3 inside a 480px modal, 22px padding, 12px radius, `--canvas` fill, `--shadow`; the heading is 18px/650, the body 13.5px/1.55.

**Acceptance scenarios**

1. **Given** the confirmation is up **When** its card is measured **Then** it is `min(468px, 100%)` wide — 448px inside a 480px modal — with 22px padding and a 12px radius.
2. **Given** the confirmation is up **When** its type is measured **Then** the heading is 650 18px/1.25 and the body 400 13.5px/1.55 in the UI sans face.
3. **Given** the dark theme **When** the confirmation is up **Then** the card takes the dark `--canvas` and the scrim the dark `--backdrop`, with no colour named in the rule.

### Edge Cases

- **When** the dialog is narrowed to the viewport (`min(30rem, 100vw - 32px)`) **Then** the card stays inside the layer's 16px padding, because its width is `min(468px, 100%)`.
- **When** the layer is closed **Then** `hidden` still hides it — the layer's own `display` would otherwise beat the user agent's `[hidden]` rule.
- **When** the confirmation is cancelled by the backdrop, Escape or the form's own Cancel **Then** the behaviour is unchanged from today; this slice adds no new dismissal path.
- **When** the copy succeeds **Then** the browser navigates to the new template as it does today; the layer is not re-entered.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The Copy as template confirmation SHALL render as a layer that covers the whole edit dialog — a scrim over the form and a card centred on it — so the modal's own height does not change when it opens. | `new: reading` → R47 |
| FR-002 | While the layer is up, the form beneath SHALL be covered: a click at the form's Save position resolves to the confirmation, never to the button. | `new: reading` → R47 |
| FR-003 | The confirmation's card SHALL carry `min(468px, 100%)` width, 22px padding, a 12px radius, the canvas fill and the dialog's shadow. | `new: reading` → R47 |
| FR-004 | The confirmation's heading and body SHALL read at 650 18px/1.25 and 400 13.5px/1.55, and its two answers SHALL be right-aligned with an 8px gap. | `new: reading` → R47 |
| FR-005 | The layer SHALL keep the dialog's rounded silhouette, and SHALL still be hidden by its `hidden` attribute when closed. | `new: reading` → R47 |
| FR-006 | The confirmation's answers SHALL remain the editor's own buttons (`.editor__save` / `.editor__cancel`, 38px), and its Cancel SHALL restore the form as it does today. | `reading` R37 |

### Key Entities

None — this slice changes no model, no field and no endpoint. It is stylesheet and test work.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Pressing Copy as template does not change the modal's height | the dialog's `getBoundingClientRect().height` is equal before and after, to the tenth of a pixel |
| SC-002 | The confirmation is one surface over the form | the layer's rect equals the dialog's rect; `elementFromPoint` at the form Save's centre is inside the layer |
| SC-003 | The card matches the accepted preview's numbers | 448 × 176.3 (± 1px), padding 22px, radius 12px, heading 18px/650, body 13.5px |
| SC-004 | The answers sit on the card's right edge | the accept button's right edge is 22px inside the card's right edge, and the gap between the two is 8px |

## UI/UX

`static preview at specs/212-copy-confirm-layer/preview/index.html` — the real editor modal, the real `_editor_form.html` markup the server sends for a template, the real `_copy_confirm.html` block with `hidden` removed, the product's own `tokens.css` and `components.css`, and `candidate.css` toggled by the page's own button (`Proposed CSS` ⇄ `Current CSS (production)`). A theme button switches light/dark.

Measured in that page at 1440 × 900, device scale 1 (`.venv/bin/python specs/212-copy-confirm-layer/preview/probe.py`):

- **Layout / position**: the layer is `position: absolute; inset: 0` inside `.editor` (the dialog is `position: fixed`), so its rect equals the dialog's — **480 × 241.3 at (480, 329.4)** — and `elementFromPoint` at the form Save's centre (781.8, 510.6) returns `.editor__confirm`, not the button. The card is centred: **448 × 176.3 at (496, 361.8)**, i.e. 16px inside the layer on every side, because the layer's 16px padding caps `min(468px, 100%)` at 448px.
- **Size / spacing**: card padding **22px**, radius **12px**; heading box 404 × 22.5 with a 10px bottom margin; body 404 × 41.8 with a 20px bottom margin; the actions row is 404 × 38 at y 478.2. The answers are **81.6 × 38** (Cancel, x 682.4) and **150 × 38** (Copy as template, x 772), ending 22px inside the card's right edge, 8px apart.
- **Colour / typography**: scrim `--backdrop` (**rgba(20, 20, 18, .52)** in light, .68 in dark), card `--canvas` (**rgb(247, 245, 241)**), shadow `--shadow` (**0 6px 18px -10px rgba(20, 20, 18, .5)**). Heading 650 **18px**/1.25, body 400 **13.5px**/1.55, both UI sans. No colour is named in the rule, so the dark theme needs nothing of its own.
- **States**: closed — `hidden` keeps the layer `display: none`; open — as measured; Cancel — the layer hides and the form is operable again (today's behaviour, unchanged). Hover and focus on the two answers come from `.editor__save` / `.editor__cancel`, which already ship their own hover and `:focus-visible` rules; the accept button focuses on open, as it does today.
- **Motion**: none. The layer appears at once, as spec 167's preview drew it.
- **Responsive**: the dialog is `min(30rem, 100vw - 32px)`; the card is `min(468px, 100%)` inside the layer's 16px padding, so it never overflows at any width the dialog can take.

The current state, for comparison (the preview with `candidate.css` disabled — the same numbers
production serves, to within a tenth of a pixel): the layer is `position: static`, `display: block`,
transparent, no radius; the card is **436 × 235.5** with 4px/2px padding, no fill and no shadow; the
heading falls back to the browser's `h3` (**18.72px / 700**, 18.72px margins); the body to **16px**;
the actions row is `display: block` with `justify-content: normal`, so both answers sit left; the modal
grows to **476.8px** tall (241.3 with the proposal) and `elementFromPoint` at the form's Save returns
`.editor__save` — the form is still live under the confirmation.

## Assumptions

- **The card follows spec 167's accepted preview, not generate.css's card** — 468px max width, 22px padding, 12px radius, `--canvas`, `--shadow` — because 167 is the preview accepted for *this* surface. The generate dialogs carry a 440px card with a 17px heading in `generate.css`, scoped to their own layer; inside a 480px modal the layer's 16px padding caps both at 448px, so the difference is 8px of card width and 1px of type, and unifying the two cards is a separate decision this slice does not take.
- **The answers keep the editor's own buttons at 38px**, not the preview's 36px `.confirm__actions button` rule, because the shipped `_copy_confirm.html` already uses `.editor__save` / `.editor__cancel` and the generate confirmation ships the same 38px pair; the preview's own button rule never reached the product.
- **The scrim restates the dialog's 14px radius** (`border-radius: 14px` on the layer). The preview drew the layer without a radius, which squares off the dialog's corner while it is up; `inherit` is not available because the layer's parent is `.editor__body`, not the dialog.
- **The rules are scoped to the layer** (`.editor__confirm-layer .editor__confirm …`) rather than to the bare class, because `.editor__confirm`'s own `display: grid; gap: 10px` in `components.css` is what the generate page's cards are built on, and restyling the bare class would re-space those dialogs.
- **No motion is added**: the preview and the accepted spec-167 design show the confirmation appearing at once, and a fade would be a behaviour nobody asked for.

## Clarifications

### Session 2026-11-21

- Zero open items. No `[NEEDS CLARIFICATION]` markers were written: the surface, its accepted preview and the failing state are all on record, and the three judgement calls above were taken as recorded assumptions rather than questions.
