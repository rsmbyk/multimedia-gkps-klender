# Fold — spec 215

**Date**: 2026-11-21
**Capabilities touched**: `reading`
**Operations**: 2 `modified` (R37, R47), 0 `added`, 0 `removed`, 0 `renamed`
**Requirement counts**: before 47 · after 47 (no requirement added or retired; two were rewritten)

## `reading` — R37, modified

`Any Tata Ibadah copies as a template`. The block was replaced whole. What changed:

- **Added**: the confirmation carries a Name field for the record it creates, defaulting to
  `<source name trimmed to 57> (Copy)`; a click selects all of it and a later click places a caret; the
  accept button is disabled while the name is blank.
- **Added**: the copy is created under the name the field holds; the endpoint reads `name`, refuses a
  blank or over-64-character one, and names a nameless request `<source> (Copy)`; the source keeps its
  own name.
- **Removed**: *"The copy SHALL keep the name"* — superseded. A copy that silently kept its source's name
  left two records sharing one, which is the defect this slice exists to remove.
- **Kept**: every entry copied in order as ordinary editable entries, a template source's fill-ins and
  choices brought along, no date, a template, landing on Templates.
- **Scenarios**: two added (`naming the copy`, `a name that cannot be used`); the two existing ones kept
  unchanged.

## `reading` — R47, modified

`The Copy as template confirmation covers the form it asks about` → `… is a dialog of its own`. The block
was replaced whole. What changed:

- **Changed**: the layer covers the **window**, and the card is centred on the window rather than on the
  dialog. The dialog's own height is unchanged on open **and on close**.
- **Changed**: the card is `min(448px, 100%)` with a **14px** radius (the dialog's own), the dialog's
  hairline and shadow, and a 13.5px **lead**; the old block's `min(468px, 100%)` inside a 16px-padded
  layer and its 12px radius described a card inside the dialog and no longer hold.
- **Added**: the card's parts in order — the copy's description, the Name field, the three facts, the
  answers.
- **Added**: Cancel **and a click on the scrim** dismiss the confirmation; Escape dismisses the
  confirmation without closing the edit dialog.
- **Corrected at Converge** (owner's decision, recorded in `converge.md` finding #3): the block no longer
  says the dialog stays *legible*. The card (341.7px) is taller than either dialog (312.5px service,
  241.3px template), so the dialog's text sits behind the card and never shows; what shows is its dimmed
  silhouette. The text now says exactly that, and says the text is not expected to show.
- **Kept**: the form is inert, the answers stay the editor's own buttons, `hidden` still hides the layer,
  the generate page's card is untouched.
- **Scenarios**: four, rewritten to the new numbers; the narrow case now speaks of the window rather than
  the dialog.

## Not folded

Nothing. Both requirements converged.

## Header

`last folded` 2026-11-21 (unchanged date — the slice folded the same day); `215-copy-template-dialog`
prepended to the `slices` list.
