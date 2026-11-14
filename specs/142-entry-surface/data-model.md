# Data model: a service entry draws no box until it is pointed at

**Slice**: `specs/142-entry-surface`

No entity changes. The slice touches one stylesheet rule and two custom properties; nothing is
stored, migrated or exposed. What follows is what the stylesheet reads, and what each thing is now.

## Service entry box — `.tatib__item--acts`, `.tatib__eos`

The box an entry owns in the Tata Ibadah stage. Unchanged: `min-height: 56px`,
`padding: 8px 8px 8px 12px`, `border-radius: 9px`, `padding-right: 106px` below a 700px pane and
`264px` at or above it. Removed: `background` and the inset `box-shadow`.

## Row fill — `--icon-hover-bg`

The one paint an entry can carry: `rgba(31, 31, 29, .08)` light, `rgba(255, 255, 255, .09)` dark.
Applied on hover, on deliberate keyboard focus, and while the entry owns its open modal; never on
quiet focus restoration. It is shared with the rail's icon hover, and this slice does not change it.

## Deleted tokens

| Token | Light | Dark | Readers after this slice |
| --- | --- | --- | --- |
| `--tatib-entry-fill` | `rgba(31, 31, 29, .012)` | `rgba(255, 255, 255, .012)` | none |
| `--tatib-entry-outline` | `rgba(31, 31, 29, .08)` | `rgba(255, 255, 255, .09)` | none |

## Entry kinds — `ServiceEntryKind`

The surface rule reaches all five; the same paint applies to each, and only two kinds have geometry
of their own.

| Kind | Geometry the slice keeps | Identity it relies on |
| --- | --- | --- |
| `TEXT` | 56px floor, 8/8/8/12 padding | its words, and the `L` / `J` voice colours (spec 059) |
| `SCRIPTURE` | as text | its title (`Kisah Para Rasul 1:1`) |
| `SONG` | as text | its title and `Bait` line |
| `MEDIA` | `min-height: 80px`, `padding: 16px 16px 16px 64px`, 42px icon tile at `left: 13px` | the tile, the filename and the type line |
| `SECTION_BREAK` | 56px box, `margin: 0` | its own 2px `--divider` rule and 5px diamond |

## DOM attributes read

None added or removed. Of the existing ones, this slice's behaviour depends on `.tatib__item`,
`.tatib__eos`, `.tatib__item--acts`, `.tatib__item--media`, `.read__body` (the `stage-pane`
container) and the `data-kind="tatib"` attribute on the article.
