# Research: A text entry is written and edited in the media modal's large frame

**Spec**: `specs/133-text-modal-large-frame/spec.md`
**Unknowns remaining**: 0

## D001 — Key the large frame on what the form *is*, not on the media hook

- **Decision**: the text create form and the media create form both carry `data-editor-size="large"`,
  and the six large-frame rules in `components.css` match `.editor:has([data-editor-size="large"])`
  instead of `:has([data-media-create])`.
- **Rationale**: the frame is a property of the dialog, not of a kind's fields. `data-media-create` stays
  on the form because the media JavaScript needs it; overloading it as the styling hook would have made
  the CSS reach into a feature it does not own, and adding a second selector set for text would have
  duplicated six declarations that must stay identical.
- **Alternatives considered**: a parallel `.editor:has([data-entry-form="text"])` rule set (duplication,
  drift); marking the `<dialog>` from script (breaks on the 400 re-render, which replaces the body);
  a `.editor--large` class toggled by JS (the same problem, plus a flash before the class lands).
- **Provenance**: research — both dialogs were measured before and after (probe output in `preview/`).

## D002 — Mark the growing field explicitly

- **Decision**: the Text field carries `data-editor-grow`; the CSS gives that field `flex: 1` and its
  textarea `flex: 1; min-height: 0`.
- **Rationale**: `:has(> textarea)` would also match a future field with a textarea for another reason,
  and the field, not the textarea, is the flex item (it also holds the label and the error paragraph).
  An explicit hook states the intent and survives markup moving around it.
- **Alternatives considered**: `:has(> textarea)` (works today, unstated intent); a fixed `height` on the
  textarea (the frame changes with the window, so a fixed height is wrong at 1280×600).
- **Provenance**: research — measured 419px at 1440×900, 227px at 1280×600, 507px on the edit form.

## D003 — Both text forms, not only the create form

- **Decision**: the marker is written for `kind == 'text'` whatever `entry` is; edit text is large too.
- **Rationale**: owner decision at Clarify. The edit form is the same template with the same two fields,
  and a size that depends on which step the operator is on reads as two different dialogs.
- **Alternatives considered**: create-only (mirrors media, where the edit form shows a read-only file
  reference and has nothing to grow); create now, edit later.
- **Provenance**: owner decision.

## D004 — The dialog is positioned `fixed`, not `relative`

- **Decision**: `.editor` takes `position: fixed`, replacing `position: relative`.
- **Rationale**: a `position: relative` dialog in the top layer is laid out in document coordinates, so
  the page's scroll offset moves it: a 760px frame opened from a scrolled service was measured at y = −4
  with only 74px of scroll, clipping its title band. Edit text always sits below the fold of a filled
  stage, so US2 cannot be satisfied without this. `fixed` still establishes a containing block, so the
  absolutely positioned date popover keeps resolving inside the dialog — verified: it opens 8px under its
  trigger (504.3 against a 496.25 trigger bottom) and inside the window.
- **Alternatives considered**: `position: absolute` (same document-coordinate fault); centring the
  document before opening (moves the page under the operator); scroll-locking the page (`position:
  fixed` on `body` would fight the shell's own layout and its sticky header).
- **Provenance**: research — before/after measured on `/tatib/144/` (scrollY 556 → y = 70) and on
  `/tatib/` (scrollY 250 → y = 285.8 for a 328.5px form).

## D005 — No motion added

- **Decision**: the text dialog keeps opening without animation; the 190ms `media-library-in` scale stays
  media-only.
- **Rationale**: the animation is named for the media library and is triggered by the media form's own
  selector; extending it is a second, visible change the request did not ask for. Recorded as assumption
  A-4 so the owner can veto it at gate 1.
- **Alternatives considered**: share the animation with the text dialog (would move both create dialogs
  alike — a defensible second reading of "the same modal").
- **Provenance**: owner decision (implicit in A-4, not vetoed at gate 1).

## D006 — Keep the media dialog's numbers exactly

- **Decision**: the frame is 840×760 clamped to the window, with 26px gutters, a `20px 26px` title band at
  21px, and an action row at `14px 26px 20px` with no divider — the media dialog's own values, reused
  rather than re-derived.
- **Rationale**: the request is parity; any other pair of numbers ("large, but a little narrower") would
  need its own justification and would break the comparison the operator makes between the two actions.
- **Alternatives considered**: 720 wide (text lines are short), 900×780 (more room without touching the
  media dialog's numbers).
- **Provenance**: owner decision ("the same large modal").

## Open

<!-- empty: Phase 0 finished, zero unknowns -->
