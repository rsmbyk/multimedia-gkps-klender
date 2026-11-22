# Research: Keep Add song when the songbooks sidebar is closed

**Spec**: `specs/222-add-song-parent-closed/spec.md`
**Unknowns remaining**: 0

## D001 — Where the button is hidden

- **Decision**: the hide comes from the shared editor rule in `static/styles/design/components.css:463`:
  `[data-nav="mini"] .editor-add, [data-nav="closed"] .editor-add { display: none; }`. It matches
  every `.editor-add` in the document, including `#songAdd` inside `.ch__add` in the second sidebar.
- **Rationale**: reproduced on the live page at 1440×900 — after `#panelCollapse.click()` the root is
  `data-nav="closed"` with `data-ch="open"`, `#chapters` computes `visibility: visible`, and
  `#songAdd` goes from `display: flex`, 38px high to `display: none`, 0×0. The node and its
  `data-editor-book` remain in the DOM; only the computed display changes.
- **Alternatives considered**: a JS re-show on `panelCollapse` (would fight the CSS state on reload
  and at other breakpoints), and a template move of the button into the first sidebar (changes the
  approved layout and the second list's markup). Both lose to fixing the selector boundary.
- **Provenance**: research — live browser measurement and source read.

## D002 — The selector boundary

- **Decision**: scope the hide to the first sidebar: `[data-nav="mini"] .panel .editor-add,
  [data-nav="closed"] .panel .editor-add`. The second-level rule `.ch__add .editor-add` keeps its
  existing `width`/`margin`, and its visibility follows the `.chapters` sidebar instead.
- **Rationale**: `#panelAdd` is a child of `aside.panel`; `#songAdd` is a child of `aside.chapters`.
  The static preview confirms the scoped rule gives `flex / 38px` for `#songAdd` and `none` for
  `#panelAdd` with `data-nav="closed"`, `data-ch="open"`.
- **Alternatives considered**: a single `.ch__add .editor-add { display: flex }` override — works
  but leaves the over-broad hide rule in force and invites the same bug for any future second-level
  control. Scoping at the source is the smaller, root-cause change.
- **Provenance**: research — preview and source read.

## D003 — How the mini state is reached

- **Decision**: the regression test sets `document.documentElement.dataset.nav = 'mini'` directly
  for the shared-rule assertion, with a comment explaining that Kidung has no mini control (only
  Alkitab's collapse produces mini). The user-reported closed state is driven through the real
  `#panelCollapse` control.
- **Rationale**: the CSS rule is state-driven; the bug's reported path and the mini variant share
  the same selector. Driving the reported path through the UI keeps the E2E honest; setting only
  the unreachable state directly avoids inventing a control the product does not have.
- **Alternatives considered**: adding a mini toggle to Kidung (new behaviour, out of scope), or
  dropping the mini assertion (leaves half the fix untested).
- **Provenance**: research — reading.js:1295–1303.

## Open

None.
