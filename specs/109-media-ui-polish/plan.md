# Plan 109: Clarify Media Library controls and align media entry labels

- **Status:** Accepted (2026-10-17)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-109
- **Bump:** patch

## Why

The Media Library sort button reads like a plain option button, and the main-rail image pictogram suggests an image-only section. On Tata Ibadah, the general heading margin pushes a media entry's title and subtitle below the center of its file icon. The upload hint also crowds the size limit onto the format line and splits PPT and PPTX into separate labels.

## Scope / edges

**In:** The Media Library sort button icon, the main-rail Media Library icon, Tata Ibadah media entry title/subtitle alignment, and the New media upload hint and unsupported-file copy.

**Out:** Sorting behavior, navigation behavior, upload acceptance rules, file inspection, file size enforcement, missing-file semantics, and projector rendering.

## Approach

Follow the approved Media Library, service-entry alignment, and media-entry form previews. Keep the sort icon separate from the mutable option label so changing sort order cannot remove it. Replace the image pictogram with a folder containing file lines. Make the media-specific title margin override the general Tata Ibadah heading margin. Put the format list and size limit on two lines in the upload drop area.

## TDD

- Domain/app tests: none; behavior and persistence are unchanged.
- E2E: targeted Media Library sort-label/icon and rail-icon checks; service-entry titled/untitled alignment; upload hint copy.

## Risks

This spec depends on the media feature stack and on the parallel offline media service-entry work. Rebase after those changes land and validate the final Tata Ibadah markup before implementation. Preserve missing-file danger styling and selected/hover states.
