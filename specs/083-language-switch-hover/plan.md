# Plan 083: Give the translation switch the same hover as the screen-mode switch

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-086
- **Bump:** patch

## Why

The two segmented controls in the new UI behave differently under the pointer. The Text screen-mode
switch fills the option under the cursor:

```css
.screen-mode button:hover:not([aria-pressed="true"]) { color: var(--ink); background: var(--icon-hover-bg); }
```

The translation switch only darkens the glyph's colour:

```css
.read__lang button:hover, .read__lang a:hover { color: var(--ink); }
```

Two switches that look alike but respond unlike each other read as a bug, and the translation switch is
the one that looks inert — which is what the owner reported.

## Scope / edges

**In:**

- `.read__lang` in both places it is rendered: the reading header (`base.html`, anchors) and the entry
  form's passage picker (`_entry_form.html`, buttons).

**Out:**

- The Multi-line / Single-screen switch, which already has the hover being matched.
- The thumb, the selected fill, sizes, and the focus outline.
- The legacy OBS dock controls, which are a separate front-end.

## Approach

Bring the translation switch's hover rule to the same shape as the screen-mode one: an unselected
option under the pointer takes `--icon-hover-bg` and `--ink`, and a selected option takes nothing.
Both instances share `.read__lang`, so one rule covers the header and the modal; the enhanced
transition list gains `background` so the fill fades with `--ease` like the text colour.

## TDD

- Domain/app tests: N/A — CSS only.
- E2E (Playwright): `tests/e2e/test_reading.py` for the header switch and
  `tests/e2e/test_entry_pickers.py` for the modal switch. Assert the computed background of an
  unselected option under hover and of the selected option under hover (unchanged).

## Risks

- The header switch is rendered with anchors and the modal one with buttons; `.read__lang a` and
  `.read__lang button` already share a rule, but the anchors' transition currently lists only `color`,
  so the fill would snap rather than fade if that list is not extended.
- The decorative thumb sits behind the options; a hover fill on the *selected* option would paint over
  it, so the `:not([aria-pressed="true"])` guard is load-bearing. It must also hold for the anchors'
  `aria-pressed` state.
