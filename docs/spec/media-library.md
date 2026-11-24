# media-library

**capability**: `media-library`
**last folded**: 2026-11-24
**slices**: `239-media-filter-pill-hover`, `182-host-font-detection`, `152-transfer-scrollbar-edge`, `149-transfer-separator-seam`, `166-slides-render-fidelity`

The local Media Library and the companion's transfer dialog. This file starts at spec 149: no
media-library capability existed while the slices that built the surface landed (113, 117, 118), so
their requirements are not folded here and the tree begins with the transfer dialog's drawing rules.

**Known split, not yet resolved.** Spec 146's age grouping of this dialog folded into
`reading/R22`–`R23` because this file did not exist when it landed, so the Media Library's behaviour
currently lives in two capabilities. Moving those requirements here (renumbering them, or leaving
`R<n>` in place as a cross-reference) is its own decision and is left to the pass that next touches
the library.

### R1 — The Transfers dialog draws each boundary once, scrolls inside its own frame, and its bar is the dialog's edge

At the boundary between the transfers that finished in the current session and the older ones, the
dialog SHALL draw exactly one line: 2px in `--divider`, 9px from the text above it and 9px from the
text below it. Every other row boundary SHALL remain a single 1px `--divider` border.

When the rows are taller than the dialog's `max-height`, the list SHALL be the element that scrolls,
the `Transfers` title SHALL stay in place above it, and no row SHALL paint outside the dialog: at the
end of the scroll the last row's border sits 22px above the dialog's own border. A list short enough
to fit SHALL take the dialog's natural height, show no scrollbar and reserve no lane for one.

The list's scroll area SHALL span the dialog's inner box on the right and the bottom: its scrollbar
paints against the dialog's right border with no canvas between them, and its lane ends at the
dialog's bottom border. The rows, the title, the age headings and the list's top SHALL NOT move, and
the bar SHALL keep the app's shared drawing — 5px, `--scroll-thumb`, rounded, no stepper buttons. The
dialog SHALL clip its content to its rounded border, so the bar's bottom end is cut by the 12px corner
instead of painting over it.

**Scenarios**

- **Given** nine transfers, two of which finished after this session started, **When** the dialog is
  opened from the rail, **Then** the boundary between them is one 2px line with 9px above and below
  and no second line within 20px of it.
- **Given** fifteen completed transfers, **When** the dialog is opened, **Then** the list scrolls, the
  title stays in place, and nothing paints outside the dialog.
- **Given** a dialog opened from the Media Library's own Transfers button, or one holding an active
  transfer, **Then** no session divider is drawn and every boundary is a 1px border.
- **Given** fifteen completed transfers scrolled to their end, **Then** the bar's right edge is against
  the dialog's right border and its bottom meets the bottom border, cut by the corner radius, with the
  last row still 22px above the dialog's border.
- **Given** the same dialog, **Then** every row's text, an age heading and the title sit on the x they
  sat on before, and the list's top is still 14px below the title.

### R2 — A converted deck keeps the deck's own layout

A PowerPoint file SHALL be converted by an Impress that places text where the deck places it — 25.2 or
newer — and each family a deck names SHALL be drawn in a proportional face: `Calibri` and `Calibri
Light` in Carlito, `Cambria` in Caladea, `Arial` in Liberation Sans, `Arial Narrow` in Liberation Sans
Narrow, `Times New Roman` in Liberation Serif, `Courier New` in Liberation Mono — unless the computer
that converts has the family itself, in which case that family SHALL be the one drawn: the mapping is
a fallback, never an override. A family with no free
metric equivalent SHALL be drawn in a proportional substitute, and no proportional family SHALL be
drawn in a monospaced one. A build of the image SHALL fail when one is. The conversion command, its
120-second ceiling, its 2 GB memory and 400 MB file limits and its private LibreOffice profile SHALL
stay as they are. (spec 166; modified by spec 182)

**Scenarios**

- **Given** a deck set in Calibri and Times New Roman, **When** it is converted, **Then** every word on
  its pages lands within 1 pt of the same deck converted by LibreOffice 25.2 with the same mapping, and
  no page embeds a monospaced face.
- **Given** the reported bulletin of 16 slides, **When** page 1 is converted, **Then** its title ink
  measures 477 × 199 px at 96 dpi — the reference's own box — and page 3's words are within 0.7 pt.
- **Given** the same deck's offering page, **When** its band is converted, **Then** the band holds five
  words, each amount on its label's line at x 475.45 and x 785.56, and nothing is clipped by the edge.
- **Given** a deck that sets a run in `Courier New`, **When** it is converted, **Then** that run is still
  monospaced — the rule refuses a mono answer to a proportional request, not the face itself.
- **Given** a computer with `Calibri` installed, **When** a deck set in `Calibri` is converted, **Then**
  the real Calibri is drawn rather than Carlito, and the renderer's identity changes so a deck converted
  earlier is converted again. (spec 182)

### R3 — A derivative is named after the renderer that made it

The PDF of a deck SHALL be keyed on the renderer's identity — its LibreOffice version, its converter
revision and its font inventory — so that a rebuilt image, a newer LibreOffice or an added font produces
a new PDF on the next request, while an unchanged renderer converts a deck once and shares that one
conversion between concurrent requests. If the font inventory cannot be read, the version and the
revision SHALL still key it. (spec 166)

**Scenarios**

- **Given** a deck already converted, **When** a font is added or the LibreOffice version changes,
  **Then** the next request converts again and the page shows the new render.
- **Given** neither changes, **When** the same deck is requested twice, **Then** it is converted once.
- **Given** a derivative produced by an older renderer, **When** the new one is written, **Then** the
  library's own record — the deck's SHA, name, family, references and deadline — is unchanged.

### R4 — The converter draws the faces the computer has, and the folder an operator adds

The companion SHALL read two host sources, re-scanned when it starts: the computer's own font
directories, mounted read-only under `/usr/share/fonts/host`, and the operator's directory, mounted
read-only at `/usr/share/fonts/operator` from `GKPS_FONTS_DIR` (default `.fonts/` inside the checkout).
A face from either source SHALL join the renderer's inventory without rebuilding the image or changing
code. When one family exists in both, the operator's copy SHALL be the one drawn. A source the Docker
daemon cannot read SHALL be skipped and named, never mounted as an empty directory. Absent or empty,
the companion SHALL convert exactly as it does without it. (spec 166; modified by spec 182)

**Scenarios**

- **Given** a font file in that directory, **When** the companion starts, **Then** the family is
  available to the converter and the identity changes, so a deck converted before it is converted again.
- **Given** no such directory, **When** the companion starts, **Then** it starts as before and the
  substitute faces are used.
- **Given** a computer with the face installed, **When** the launcher mounts that computer's font
  directories beside the operator's, **Then** the face joins the inventory and wins over the image's
  substitute. (spec 182)
- **Given** a directory the Docker daemon cannot read, **When** the launcher runs, **Then** it is
  skipped and named, and a start that mounted nothing visible is reported. (spec 182)

### R5 — The companion manages this computer's origins on its own page

The companion SHALL serve a configuration page on its own loopback address (`http://127.0.0.1:63174/`)
that manages the origins this computer accepts: the operator adds, edits and deletes recorded origins
on the page under the exact-origin grammar with the first broken rule named under the form, a
duplicate is refused as both an add and an edit, and a deletion renumbers the list. The local seeds
(`http://localhost:<WEB_PORT>` and `http://127.0.0.1:<WEB_PORT>`) SHALL be shown read-only. The
companion SHALL enforce the union of the seeds and the recorded set on every request; a request from
an origin outside it SHALL be refused with a message naming the page and no CORS header, and the web
app SHALL surface that message in its local-media status popup when present. The recorded set SHALL
live in the companion's volume — it survives a restart — and removing the volume removes it. The
page SHALL also list the font directories the converter sees with each one's family count, and say
outright when none is found. The page and its endpoints SHALL be bound to the loopback host and the
page's own origin, with no media token. (spec 192)

**Scenarios**

- **Given** a fresh start with nothing recorded, **When** the page is opened, **Then** the empty
  state is said outright beside the read-only local seeds and the font directories with their counts.
- **Given** an origin typed with a path or trailing slash, **When** it is added, **Then** the first
  broken rule is named under the form and nothing is recorded.
- **Given** a valid origin recorded, **When** the companion restarts, **Then** the set is still
  recorded and enforced.
- **Given** the operator edits a recorded row inline, **When** they press Discard or click outside
  the field, **Then** the edits are discarded and the row keeps its origin.
- **Given** a recorded origin deleted, **When** the list is shown, **Then** the remaining rows are
  renumbered from one.
- **Given** a browser origin that is neither a seed nor recorded, **When** it uses the companion,
  **Then** it is refused with the page-naming message and the web app's status popup shows it.
- **Given** a computer whose font mounts are all empty, **When** the page is opened, **Then** the
  fonts section says no font directory was found. (spec 192)

### R6 — The Media Library's unpressed filter pills answer the pointer

The Media Library's file-type filter pills and the Unused pill SHALL take a `--focus` border
and an `--icon-hover-bg` fill while hovered — the same pair the sort and icon buttons in
that filter row already use. A pill with `aria-pressed="true"` SHALL keep its accent fill,
text and border while hovered. The change SHALL alter no box geometry, label colour,
focus-visible outline, separator dot or filter behaviour, and no surface outside those
unpressed pills SHALL change. (spec 239)

**Scenarios**

- **Given** the Media Library page with no filter selected, **When** the pointer moves over any
  of the six pills, **Then** that pill's border reads `--focus` and its fill `--icon-hover-bg`,
  in both themes.
- **Given** a hovered pill, **When** the pointer leaves it, **Then** its transparent fill and
  `--divider` border return, with no transition or added motion.
- **Given** a pressed pill, **When** it is hovered, **Then** its background, border and text
  colours are identical to its resting values.
- **Given** a pill at rest, hovered or pressed, **When** its box is measured at 1440px, **Then**
  it stays 63.36 × 30 px and the keyboard focus-visible outline stays 2px with 2px offset. (spec 239)
