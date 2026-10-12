# Plan 067: Consistent scrollbars

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-070
- **Bump:** patch

## Why

The Tata Ibadah sidebar in the owner's screenshot uses a narrow, rounded, subdued scrollbar. Other scrollable areas in that new app UI should feel consistent with it.

## Scope / edges

**In:** Scrollbars in the new app UI, including the main page, sidebars and lists, detail/preview panels, preview and other modal content, dropdowns and popovers with overflowing options, search results, and multiline text fields. Use a shared shape with colors appropriate to the surface.

**Out:** Legacy web management/public reading pages and legacy OBS docks/sources; changing scroll behavior, layout dimensions, content, or browser chrome outside app pages.

## Approach

Use the existing `static/styles/design/tokens.css` and `components.css`, loaded by `multimedia/web/templates/reading/base.html`. The shared scrollbar has a 6px vertical width and horizontal height, a transparent track, a fully rounded thumb, and a darker/lighter hover state. The light thumb is `#AAA59B` (`#827D73` on hover); the dark thumb is `#514D45` (`#777268` on hover). Standard `scrollbar-width: thin` and `scrollbar-color` provide the browser-supported equivalent. Apply to the document and descendants so `.panel__body`, `.editor__content`, `.editor__date-calendar`, `.preview__body`, `.preview__tabs`, `.editor__picker-options`, and native textareas share the treatment. Preserve the intentional hidden scrollbars in the collapsed mini rails (`[data-nav="mini"] .panel__body` and `.ch__body`), which use scroll chevrons.

## TDD

- Domain/app tests: N/A; CSS only.
- E2E: Inspect representative new UI pages with overflowing page, panel, preview modal, dropdown, and textarea content; verify pointer, keyboard, and touch scrolling remain functional.

## Risks

- Browser engines differ in scrollbar support and overlay behavior. Native scrollbars remain the fallback.
- A single dark thumb color can lose contrast on a light panel; confirm both surface variants visually.
- Collapsed mini rails deliberately hide native scrollbars in favor of chevrons; global styling must not override that behavior.
