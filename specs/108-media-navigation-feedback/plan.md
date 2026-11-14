# Plan 108: Keep media navigation selection feedback in sync

- **Status:** Accepted (2026-10-17)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-108
- **Bump:** patch

## Why

The Upload / Media Library switch changes its active styling immediately, while the app's
other segmented switches move a single active thumb between options. Separately, the main
sidebar's Media Library link keeps its `aria-current="page"` styling after the reading shell
navigates in place to another destination, because that rail node is retained during the page
swap. The operator should get the same clear selection feedback from the media tabs and the
sidebar, and the sidebar highlight should describe the page that is actually open.

## Scope / edges

**In:**

- Add the approved sliding active thumb to the Upload / Media Library tab switch in the New
  media form, matching the app's existing segmented-switch motion and preserving its current
  dimensions, hover treatment, tab semantics, default selection, and file-selection behavior.
- Keep the main-sidebar Media Library link marked current only while the Media Library page is
  the active destination, including in-place navigation and browser history navigation.
- Preserve existing expanded/collapsed/mini state and `aria-expanded` behavior for Bible,
  Songs, and Tata Ibadah rail menus.

**Out:**

- Changes to any other switch, sidebar icon, selected-row cue, menu layout, or page layout.
- Changes to media upload, library contents, file selection, or entry save behavior.
- Changes to full-page route behavior beyond keeping the server-rendered Media Library current
  marker correct on a direct page load.

## Approach

Use [preview.png](./preview.png) as the approved visual reference. Put one decorative thumb
behind the two equal-width media-tab buttons and move it between their positions as
`aria-selected` changes. Use the existing `--ease` transition and theme tokens; disable the
transition under reduced motion. Keep the existing tab track size and hover behavior.

In the reading shell's in-place page application, synchronize the Media Library rail link's
`aria-current="page"` with the arriving destination. Do not change the rail menu buttons'
`aria-expanded` state or the existing panel navigation state machine. Cover direct load,
in-place menu navigation, and back/forward restoration in targeted browser tests.

## TDD

- Domain/app tests: N/A; no domain or persistence rules change.
- E2E: add targeted cases in `tests/e2e/test_media_library.py` for the tab thumb, selected
  panel/accessibility state, reduced motion, and Media Library rail state across in-place
  navigation and browser history.

## Risks

- The media library page is navigated in place while the main rail is retained. Update the
  retained link from the arriving page state so the direct-load and client-navigation states
  cannot disagree.
- Keep the selected visual state on the tab button and its accessible `aria-selected` value in
  sync with the moving thumb; the thumb itself is decorative and must not enter the accessibility
  tree.
- Respect reduced-motion preferences without preventing tab selection or route navigation.
