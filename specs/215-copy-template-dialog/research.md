# Research: the copy confirmation as a dialog of its own, and the copy's name

**Spec**: `specs/215-copy-template-dialog/spec.md`
**Unknowns remaining**: 0

## D001 — Where the "second dialog" lives in the DOM

- **Decision**: keep the existing `[data-copy-confirm]` layer node and make it `position: fixed; inset: 0`, inside the edit `<dialog>`, rather than adding a second `<dialog>` element.
- **Rationale**: a `<dialog>` nested inside a modal `<dialog>` is placed in its own top layer only if it is shown with `showModal()`, and a nested `showModal()` throws `InvalidStateError` while an ancestor dialog is modal. The alternatives that do work (a second top-level `<dialog>` outside the editor) would have to duplicate the copy trigger, the CSRF token and the failure announcement, and would fork the one handler `editors.js` already owns. A `position: fixed` child of a top-layer dialog is painted above the dialog and its `::backdrop`, resolves its containing block to the viewport (no ancestor is transformed, filtered or contained), and keeps `editors.js`, `_copy_confirm.html` and the `[data-copy-*]` hooks intact.
- **Alternatives considered**: a real `<dialog>` element (rejected — nested `showModal` throws); a `<div popover>` (popover is also a top-layer mechanism, but a popover opened from inside a modal dialog paints in the dialog's layer and its light-dismiss fires on the dialog's own backdrop, which is the same trap); moving the layer to `document.body` (works, but leaves the node outside the dialog that `modal.querySelector('[data-copy-confirm]')` looks in, and the dialog's `close` handler clears `#editorContent` — the layer would have to be cleaned up separately).
- **Provenance**: research — HTML's dialog spec (`showModal` throws on a modal ancestor) plus the measured behaviour of the preview page.

## D002 — Why the scrim is light

- **Decision**: `rgba(0, 0, 0, .26)` in dark and `rgba(20, 20, 18, .26)` in light, not the `--backdrop` token the layer carried inside the dialog.
- **Rationale**: the edit dialog's own `::backdrop` is already a full-strength `--backdrop` (`.52` light, `.68` dark). A second scrim at the same strength stacks to roughly 77% dark, and the measured screenshot showed the edit dialog's fields at `rgb(11,10,8)` against a `rgb(3,3,2)` page — present but unreadable, which defeats the point of leaving the dialog open. At `.26` the dialog's own surface stays at `rgb(20,19,15)` against `rgb(3,3,2)` and its title is legible.
- **Alternatives considered**: `--backdrop` at full strength (measured: the dialog disappears); no scrim at all (then nothing signals that the dialog is inert); a blur (a blur on a full-window layer repaints the whole page behind it on every frame in this app's Chrome target, and it is a behaviour nobody asked for).
- **Provenance**: research — pixel sampling of the preview page in both themes, at `.38` and `.26`.

## D003 — How the name travels to the server

- **Decision**: a JSON body, `POST {"name": "..."}`, read the way `entry_reorder` already reads its payload; the response shape stays `{id, url}` with 201.
- **Rationale**: the endpoint already answers JSON and the client already parses `result.data.error`, so a JSON body needs no new response shape. It is also the shape the neighbouring `web-entry-reorder` endpoint uses, so one reading idiom covers both. `Content-Type: application/json` also sidesteps form-encoding the name (which can hold spaces and parentheses).
- **Alternatives considered**: form-encoded (`name=` in a `FormData`): works, but the endpoint's other failures are JSON and the client would need a second parser path; a query parameter: puts a user-typed name in the URL and in the access log.
- **Provenance**: research — `views.py::entry_reorder` (lines 973–978) and `editors.js` (lines 501–513).

## D004 — What the endpoint does when no name is posted

- **Decision**: a request with no `name` key at all keeps today's behaviour and names the copy `<source name> (Copy)`, trimmed to fit; a request that posts `name` uses it after trimming, and refuses it if it is empty or longer than 64 characters.
- **Rationale**: two existing unit tests (`test_a_copy_converts_nothing`, `test_a_template_copy_keeps_its_slots`) post with no body and assert only the copy's entries, so they keep passing and keep proving what they were written for — the copy's *content* rule (spec 167). Refusing a nameless request would force those tests to change for a reason unrelated to their behaviour (TDD-07).
- **Alternatives considered**: make the name required (breaks two unrelated tests and any API caller); treat a missing name as an empty one and refuse (same); default to the source's name unchanged (contradicts FR-003's default and would let a copy share its source's name silently — the exact defect US2 exists to remove).
- **Provenance**: research — the two tests at `multimedia/web/test_tatib_templates.py:409` and `:421`.

## D005 — Where the default name is computed

- **Decision**: in the view, as `copy_name` on the editor-fragment context, and rendered as the field's `value` by `_copy_confirm.html`.
- **Rationale**: the 57-character trim and the ` (Copy)` suffix are one rule with two halves, and the server already knows both the source's name and the model's 64-character limit. Computing it in the template would put a `slice` filter next to a literal, and computing it in JS would let the field's default drift from what the endpoint would have produced for a nameless request (D004).
- **Alternatives considered**: JS (drifts from D004's server-side default); a template filter (no filter exists for this and one use is not worth a `templatetags` module).
- **Provenance**: research — `views.py::_editor_fragment_context` (lines 135–148), which already computes `copy_url` for the same include.

## D006 — Escape and the scrim, without closing the edit dialog

- **Decision**: a `cancel` listener on the dialog that calls `preventDefault()` and closes only the layer while it is open; and a click handler that closes the layer when the click's target is the layer itself.
- **Rationale**: today `Escape` closes the whole edit dialog through the dialog's own `cancel` event, which would throw away the form the confirmation is about. `cancel` is cancelable, so `preventDefault()` keeps the dialog open; the layer then hides, which is what FR-009 asks. The scrim click needs no `stopPropagation`, because the dialog's existing backdrop handler only fires when `event.target === modal`, and a click on the layer has the layer as its target.
- **Alternatives considered**: letting Escape close both (loses the form); a document-level `keydown` handler (the dialog's `cancel` is the platform's own Escape path and a second one would fire twice).
- **Provenance**: research — `editors.js` lines 129, 404 and 481–514.

## D007 — The card's radius, 12px → 14px

- **Decision**: 14px, the dialog's own radius, instead of spec 212's 12px.
- **Rationale**: 212's card sat inside a dialog and read as a panel in it; this card stands alone over the dialog, so it takes the dialog's silhouette rather than being one step tighter than it. 212's own reason for the 12px was the preview it copied, and that preview is superseded here.
- **Alternatives considered**: keeping 12px (a card that no longer sits in the dialog it was sized for); 16px (rounder than every other surface in the product).
- **Provenance**: owner decision — the accepted preview at `specs/215-copy-template-dialog/preview/index.html`, measured at 14px.

## D008 — What the E2E tests do with 212's two assertions

- **Decision**: rewrite both of 212's geometry tests rather than delete them, and keep their names' subject (the layer covers the window; the card matches the preview).
- **Rationale**: they encode the behaviour this slice replaces — layer rect equals the dialog's rect, `position: absolute`, a 176.3px card — so leaving them is a guaranteed red, and deleting them removes the only guard on the card's numbers. TDD-07 allows a test to change when the behaviour changed, which is exactly the case: the layer's box and the card's height are what this slice redefines.
- **Alternatives considered**: deleting them (loses the geometry guard); keeping the assertions and adding new ones (contradictory assertions cannot both hold).
- **Provenance**: research — `tests/e2e/test_tatib_templates.py:901` and `:936`.

## Open

None. Every question above is decided by the code, the preview's measurements, or the owner's answers at Clarify.
