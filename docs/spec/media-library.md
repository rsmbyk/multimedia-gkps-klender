# media-library

**capability**: `media-library`
**last folded**: 2026-10-29
**slices**: `152-transfer-scrollbar-edge`, `149-transfer-separator-seam`

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
