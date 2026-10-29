# Research: the preview's verse tabs get their own row

**Spec**: `specs/153-preview-tabs-row/spec.md` · **Created**: 2026-10-29

Every decision below is either measured in the preview page or read in the code it names. Nothing is
decided from recollection.

## D001 — The initial focus target is `#previewContent`

**Decision.** After `showModal()`, the dialog focuses its scrolling body, explicitly.

**Rationale.** The preview already works this way wherever the tabs are not in the header: a passage
preview reports `document.activeElement = DIV.preview__body` (measured on develop at `/tatib/144/`). The
body owns the arrow / `PageUp` / `PageDown` handling (`static/web/preview.js:476`) and is the element a
click on non-control text focuses (`:470-474`). Focusing the `<dialog>` instead would leave those keys
dead on open; focusing Close would contradict the dialog's read-only nature.

**Alternatives.** (a) Keep the tab focused and suppress its ring with CSS — hides the symptom, leaves the
dialog opening on a control the reader did not ask for, and breaks the arrow-key scroll. (b) Focus the
dialog element with `tabindex="-1"` — no ring anywhere, but the scroller's key handling never sees the
keys. Both rejected.

**Provenance.** Measured: `docs` numbers in the spec's *What the dialog does today*; `preview/preview.html`
focus demos.

## D002 — The tab band sits under the title band, and the header rule falls below it

**Decision.** `.preview__versetabs` becomes a sibling of `.preview__head`; the head draws no rule when a
visible band follows it, and the band draws the rule.

**Rationale.** Measured in the preview at 704px: rule below the tabs gives a 97px header block whose title
and tabs read as one object; rule above the tabs gives 94px and a tab row that belongs to neither the
header nor the lyrics (recorded, and reachable by one click in the preview). The rule is what the lyrics
start under in both readings.

**Alternatives.** (a) Keep the tabs inside the head as a second row — the head then has two rules or none
depending on the payload, and the title band's 52px minimum stops being a fixed identity row. (b) Keep the
single row and let the title wrap to two lines — the tab row would still take 76px of the title's width
and the 52px band would no longer be fixed.

**Provenance.** `preview/preview.html` measurements at 1440 and 390; screenshots `shots/variant-rule-*.png`.

## D003 — The head's rule is dropped by `:has()`, not by a class

**Decision.** `.preview__head:has(+ .preview__versetabs:not([hidden])) { border-bottom: 0 }`.

**Rationale.** The visible band is already expressed by the `hidden` attribute that `liftIdentity()`
toggles; a second signal (a `has-tabs` class) is state that can disagree with the first. `:has()` is
already used by the product (`.tatib__item:has(:focus:not(.focus-restore-quiet))`, `components.css`), so
this is the project's existing idiom, not a new dependency.

**Alternatives.** A class toggled in `preview.js`; `:empty` on the band (the host keeps whitespace when
`innerHTML = ''` runs, so it is not reliably empty — `preview.js:331`).

**Provenance.** `components.css` current rules; `preview.js:324-341`.

## D004 — The keyboard loop runs body ↔ selected tab, and stops there

**Decision.** With a visible tab band and no screen-mode footer, `Tab` on the body focuses the selected
tab, and `Shift+Tab` on the selected tab returns to the body. Every other preview keeps the browser's
order.

**Rationale.** Measured on develop: the dialog's order is tab `1` → body → **out of the dialog** (the
scroller is the last focusable element, and the document behind a modal dialog is not a tab stop). Once
the body takes the initial focus, a plain `Tab` would leave the dialog — so the two ends must hand focus
to each other, or the tabs become Shift+Tab-only.

**Alternatives.** (a) A whole-dialog focus trap — correct, but it changes the Tab order of previews that
reported nothing, which Converge would type `unrequested`. (b) Re-sorting the DOM with flex `order` so the
tabs follow the body — the visual order and the reading order for assistive technology would disagree, and
the tablist would read after its own panels. (c) Leaving it — the tabs stay reachable, but only backwards.

**Provenance.** Measured Tab sequence on develop and on the preview page (`probe.py`'s keyboard block).

## D005 — The tests move three locators and add four cases

**Decision.** `tests/e2e/test_entry_preview.py`: the two song cases that reach the tabs through
`.preview__head .preview__tab` read `.preview__versetabs .preview__tab`; seven cases are added — the title's
width, the tab row's own place, one rule under the tabs, the passage's unchanged box, the pointer open's
focus, the keyboard open's focus, and the Tab loop.

**Rationale.** The behaviour the moved locators assert (three tabs, equal 30px circles, horizontal scroll,
click-to-panel) does not change; only the container moved. The new cases pin the four requirements that
have no test today.

**Alternatives.** Locating by `.preview__tab` alone — passes whether the tabs are in the header or not, so
it could not catch this slice regressing.

**Provenance.** `tests/e2e/test_entry_preview.py:169-206`.

## Unknowns remaining

0.
