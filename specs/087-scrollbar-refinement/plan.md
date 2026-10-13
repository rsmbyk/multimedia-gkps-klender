# Plan 087: Slimmer, softer scrollbars with no stepper buttons

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-090
- **Bump:** patch

## Why

The shared scrollbar block sets the **standard** properties and styles the **WebKit pseudo-elements** at
the same time:

```css
:root, :root * { scrollbar-width: thin; scrollbar-color: var(--scroll-thumb) transparent; }
:root *::-webkit-scrollbar { width: 6px; height: 6px; }
```

In Chromium a browser that understands `scrollbar-width` / `scrollbar-color` takes the **native**
scrollbar path and ignores `::-webkit-scrollbar*` for that element. The native thin bar on this platform
still paints **up/down stepper buttons**, so the pseudo-element rules never run and a
`::-webkit-scrollbar-button` rule is inert — which is why the arrows were still on screen after the first
draft of this slice (and why the first preview showed them in both panes).

Measured in Chromium 145 on Linux (`offsetWidth - clientWidth`, minus 2 x 1px border):

| scroller | bar | stepper glyph at the top |
| --- | --- | --- |
| today's rule (standard + webkit) | 10px | **present**, sitting above the thumb |
| the webkit path alone (no standard properties) | 5px | none |

The first draft of this plan had it wrong: it assumed a modern Chromium had stopped drawing steppers on
custom scrollbars and that one missing `::-webkit-scrollbar-button` rule was the whole fix. The bar was
measured instead of assumed, and the mechanism is the one above.

The owner also wants the bar itself quieter and a little thinner: the thumb is `#AAA59B` on the light
canvas (2.25:1) and `#514D45` on the dark canvas (2.21:1), with 3.76:1 / 3.89:1 hover states — louder
than a passive indicator needs to be.

## Scope / edges

**In:**

- The shared scrollbar block in `components.css` (every scroller in the reading UI, the dialogs, the
  pickers, and the textareas).
- The `--scroll-thumb` / `--scroll-thumb-hover` tokens in both themes.

**Out:**

- The places that deliberately hide their scrollbar: the mini panel (`.panel__body` under
  `[data-nav="mini"]`) and the Tata Ibadah entry list (`.ch__body`).
- Scroll behaviour, the scroll-indicator chevrons of the Bible mini panel, and the legacy OBS docks.
- The `--scroll-thumb` contrast pair: `tests/test_design_tokens.py` does not assert it (the pairs list
  holds text and focus pairs only), and this spec lowers it on purpose.

## Approach

Give each engine the path that has no steppers:

```css
@supports not selector(::-webkit-scrollbar) {
  :root, :root * { scrollbar-width: thin; scrollbar-color: var(--scroll-thumb) transparent; }
}
:root *::-webkit-scrollbar { width: 5px; height: 5px; }
:root *::-webkit-scrollbar-track { background: transparent; }
:root *::-webkit-scrollbar-thumb { background: var(--scroll-thumb); border-radius: 999px; }
:root *::-webkit-scrollbar-thumb:hover { background: var(--scroll-thumb-hover); }
:root *::-webkit-scrollbar-button { display: none; width: 0; height: 0; }
:root *::-webkit-scrollbar-corner { background: transparent; }
```

Blink and WebKit match `selector(::-webkit-scrollbar)`, so they never see the standard properties and
draw the custom 5px bar, which has no buttons. Engines that do not match (Firefox) take the standard
branch and get the slim coloured bar; Firefox has no steppers either way. The button rule stays as a belt
for engines that draw steppers on the custom path. The track and thumb go from 6px to 5px and the two
thumb tokens are re-tuned so the resting thumb sits nearer its surface while the hover state still reads
as active:

| | now | proposed |
| --- | --- | --- |
| light thumb | `#AAA59B` (2.25:1) | `#B4B0A6` (1.99:1) |
| light hover | `#827D73` (3.76:1) | `#948F85` (2.95:1) |
| dark thumb | `#514D45` (2.21:1) | `#45413A` (1.83:1) |
| dark hover | `#777268` (3.89:1) | `#65615A` (3.02:1) |

Ratios are against each theme's canvas.

## TDD

- Domain/app tests: N/A — CSS only. One CSS-text assertion is worth having: the standard properties
  (`scrollbar-width`, `scrollbar-color`) appear only inside the `@supports not
  selector(::-webkit-scrollbar)` block, and `::-webkit-scrollbar-button` is suppressed. A regression
  here is silent in the browser and visible only to a pixel check, so pin the text.
- E2E (Playwright, Chromium): `tests/e2e/test_reading.py` — a scroller's occupied width
  (`offsetWidth - clientWidth` minus its borders) is 5px, its computed `scrollbar-width` reads `auto`
  (proving the native bar is not in use), a screenshot of the bar's top and bottom carries no stepper
  glyph, and the thumb takes the token colour in both themes. The existing hidden-scrollbar cases stay
  green.

## Risks

- The gate is the whole fix. If `scrollbar-width` stays at the top level, Blink silently returns to the
  native bar with steppers; `getComputedStyle` on the pseudo-element keeps reporting the custom rules
  even while the browser ignores them, which is exactly how the first draft passed a check it should have
  failed. Only the measured width is trustworthy.
- A thumb under 2:1 against its surface is quiet by design, so the hover state has to stay clearly
  different (2.95:1 / 3.02:1) or the bar stops announcing itself when the pointer is on it.
- `@supports selector()`: Blink and WebKit match, Firefox does not; an engine that supports neither the
  pseudo-element nor the standard properties simply keeps its default bar.
