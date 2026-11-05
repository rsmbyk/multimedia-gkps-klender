# The projector's sheet, before and after

`before.png` and `after.png` are captures of the **living** projector sheet at
`/projector?service=142` on the local compose stack (1920 × 1080, `device_scale_factor=2`), not
re-drawings:

- `before.png` — the sheet as `develop` serves it: three columns, the middle carrying Library
  passage, Library Detour, Image and PDF, Audio, Video; the right carrying Display, Find, While
  Finding, Fullscreen. It measures **1095 × 676.5 px**.
- `after.png` — the same page, same CSS, with the DOM moved in the browser exactly as FR-013 and
  FR-014 ask: `Image and PDF` and the merged `Audio and Video` (one `Play/Pause` row) appended to the
  left column; Display absorbing Find's and Fullscreen's rows; **While Finding** renamed **Find** and
  its rows reordered to `Previous Match`, `Next Match`, `Open Match`, `Close When Empty`, `Close Find`.
  The capture predates the owner's next move — merging `Passage` and `Library passage` into one
  `Passage` group at the top of the middle column — which the implementation carries; with it the
  middle reads `Passage`, `Library Detour` and the left column is the tallest at **686 px** for the
  whole frame.

Nothing in the page's markup, styles or scripts is changed by this capture; it is evidence for the
gate, not the implementation. The implementation edits `multimedia/web/templates/reading/projector_controls.html`
(section order) and the sheet's own CSS height rule, and the E2E asserts the frame at 1080p and the
scroll at 720p.
