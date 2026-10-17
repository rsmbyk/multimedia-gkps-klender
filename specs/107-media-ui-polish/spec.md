# Spec: Clarify Media Library controls and align media entry labels

- **ID:** 107
- **Status:** Accepted (2026-10-17)
- **Item:** ITEM-107
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make the Media Library's sort and navigation controls recognizable, align service media text with its file icon, and make upload guidance easier to scan.

## Scope

### In scope

- Media Library sort trigger and its visible label after a sort option changes.
- Main-sidebar Media Library pictogram in the reading shell.
- Tata Ibadah media entry title and subtitle alignment for titled, untitled, and missing-file rows.
- New media Upload tab's supported-formats and size-limit copy, and the corresponding unsupported-file dialog wording.

### Out of scope

- Sort options or ordering, main-sidebar routing or selection, file type detection, size validation, uploads, stored filenames, and media rendering.

## Domain rules

- Changing the sort option updates the visible option label and accessible sort name while preserving the decorative sort pictogram.
- A media entry's file reference, title value, subtitle content, and missing-file status are unchanged.
- The copy change does not broaden the accepted formats or alter the 200 MB per-file limit.

## UI details

The owner accepted the local previews `local-media-library-preview.html`, `media-entry-alignment-preview.html`, and `media-entry-form-preview.html` in the 2026-10-14 visualization set, with the upload copy revisions accepted on 2026-10-17.

- **Sort control:** Retain the existing button's minimum 36 px height, 8 px radius, 8 px vertical/12 px horizontal padding, and position at the right of the filter row. Add a 17 × 17 px up/down arrow SVG before the label with a 7 px gap. Use `currentColor` at 1.7 px stroke, with the icon in `--head-ink` and the label in `--ink`. Keep the existing menu and its selected state; update only a dedicated label element when the option changes. The icon is decorative (`aria-hidden="true"`), while the button's accessible name names the current sort option.
- **Main rail:** Replace only the Media Library image pictogram with an outlined folder containing two file lines. Size the SVG at 24 × 24 px within the existing rail button; use `currentColor`, 1.7 px stroke, rounded caps and joins. Keep the existing rail button dimensions, current-page highlight, tooltip/accessibility name, keyboard focus, and navigation behavior. Apply the same pictogram wherever the reading-shell Media Library rail is shown.
- **Service entries:** Keep the existing 42 × 42 px file icon at the left and the row's present padding and surface. Vertically center the title/subtitle block beside the icon. Override the general Tata Ibadah `.read__sec` 30 px top margin for media rows, leaving 0 px top and 3 px bottom margin on the title and 0 px on the subtitle. Keep the existing 17 px semibold title and 12 px muted subtitle treatments, wrapping behavior, action controls, and red missing-file icon. Untitled rows still display the filename as the title with their file-type label below.
- **Upload hint:** Inside the existing drop area, keep the 12 px supported-files paragraph at 1.5 line-height and 8 px below the upload button. The first line reads `Supported files: images, audio, video, PDF, and PPT/PPTX`; only `Supported files:` is semibold. The second line reads `Maximum 200 MB per file`; emphasize `Maximum 200 MB` at 650 weight in `--ink`, leaving `per file` at regular weight in `--head-ink`. Use a deliberate line break, allowing each line to wrap naturally on narrow screens. Change the unsupported-file dialog list to use `PPT/PPTX` as one label.
- **States and responsiveness:** Preserve the sort menu's current hover, active, focus, and keyboard behavior, and the rail's current, hover, and focus states. SVGs follow theme colors through CSS tokens. The sort control and upload hint must wrap or fit without horizontal overflow at the existing narrow breakpoint. No new animation; existing menu/modal motion and reduced-motion behavior remain as-is.

## Acceptance scenarios

### Scenario: Sort remains identifiable

- **Given** the Media Library page is open
- **When** the operator selects any sort option
- **Then** the up/down icon remains before the updated label
- **And** the selected option, accessible button name, and file order agree

### Scenario: Library rail describes mixed files

- **Given** the reading shell is displayed
- **When** the Media Library rail button is shown or its current-page state changes
- **Then** it uses the outlined folder-and-files pictogram at the same size and position
- **And** its navigation and selected-state behavior remain unchanged

### Scenario: Service media labels align with their icons

- **Given** a Tata Ibadah has titled, untitled, and missing-file media entries
- **When** the service page renders them or navigates to them in place
- **Then** each title/subtitle block is vertically centered beside its file icon
- **And** the missing-file icon keeps its danger treatment

### Scenario: Upload guidance is scannable

- **Given** the New media form is open on Upload with no selected file
- **When** the operator reads the drop area
- **Then** supported formats and the 200 MB limit occupy separate lines
- **And** PPT/PPTX appears as one format label and `Maximum 200 MB` is emphasized
- **And** selecting an unsupported file shows the same combined PPT/PPTX wording

## Traceability

- Domain/app tests: N/A, no rules change.
- E2E: `tests/e2e/test_media_library.py` covers the sort icon and label, rail icon, upload hint, and titled/untitled media heading margins.
- Implementation: `multimedia/web/templates/reading/base.html`, `multimedia/web/templates/reading/media_library.html`, `multimedia/web/templates/reading/_entry_form.html`, `static/styles/design/components.css`, `static/web/media-library.js`, and `static/web/media-entry.js`.
