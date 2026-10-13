# Plan 069: Manual screen breaks for multiline Text entries

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Visual preview:** [./preview.html](./preview.html)
- **Item:** ITEM-072
- **Bump:** minor

## Why

Ordinary Tata Ibadah Text entries currently become projector screens in pairs of lines. Blank lines already end a screen. An editor needs to keep selected lines together or show a selected line on its own screen without changing the wording or adding extra blank lines to the text.

## Scope / edges

**In:** Per-entry screen breaks for ordinary multiline Tata Ibadah Text entries, configured in the existing preview modal; an interactive browser preview of the proposed modal; saved projector output and navigation; automatic fallback.

**Out:** Song entries, Scripture entries, legacy Tata Ibadah rows, and the distinct single-screen Text entry kind. No change to speaker cues or wording.

## Approach

Keep the Text body as written and store optional screen-boundary metadata on its ServiceEntry. Make Preview available for all ordinary Text entries, including those short enough that the pane does not clamp them. In that modal, show one row per written line. Hovering an eligible gap reveals a prospective divider; clicking it sets the break. Render existing breaks as delicate lines in default mode and regular lines in custom mode. A hovered or focused break changes shade and reveals a centered “Remove break” label; it can then be clicked to remove it. The modal has a mode indicator and a Reset breaks control in its sticky footer. Its rows and dividers update immediately after each action. Non-editors can still read the preview, but cannot change breaks.

The default mode uses the existing two-line grouping. On the first newly added break, switch to custom and lay out breaks at every second line outward from that chosen boundary within its blank-line-separated block; other blocks keep their default pairs. A click on a displayed break removes only that break and also enters custom mode. Subsequent clicks toggle just their chosen boundary. Custom groups may contain one or more lines, including three or more when deliberately chosen. Blank lines remain mandatory boundaries. Persist each modal action without requiring the Create/Edit form. Use the same grouping rules for modal dividers and projector output. Preserve voice assignment by parsing the complete body before grouping.

If a later text edit changes the number or positions of nonempty lines and blank lines, invalidate the saved split and return to default grouping with a clear notice when the preview next opens; do not silently apply old break positions to different lines. Keep the current trailing blank screen and screen navigation behavior.

## TDD

- Domain/app tests: Grouping and validation for automatic and custom layouts, blank lines, voice continuity, and stale boundaries.
- E2E: Preview-modal hover and toggle controls, first-break cadence, keyboard access, persistence, reset, projector sequence, and projector update after a saved edit.

## Risks

- Blank lines already act as explicit pauses. A custom layout must respect them to avoid changing the operator's established text semantics.
- Larger groups rely on existing projector fitting; verify long groups are readable and do not overflow.
- The current preview is view-only and only appears for hidden/clamped Text entries. This slice makes it available for every ordinary Text entry and limits editing controls to authorized editors.
