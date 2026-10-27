# Feature Specification: A service entry draws no box until it is pointed at

**Slice**: `specs/142-entry-surface`
**Branch**: `feat/142-bare-entry-surface`
**Created**: 2026-10-28
**Status**: Draft
**Input**: "i want to revamp the entry item style. what would you do? i mean, i dont feel like the border and a slight fill there" — then, on the candidates: "try bare as default, then filled when being hovered" — then, on the five entry kinds: "leave all kinds bare — media reads fine up close"

## What the page does today

Spec 068 gave every service entry a resting surface: a fill at `rgba(31, 31, 29, .012)` and a 1px inset
ring at `rgba(31, 31, 29, .08)` (`--tatib-entry-fill`, `--tatib-entry-outline`), on `.tatib__item--acts`
and `.tatib__eos` alike.

Measured on `/tatib/142/` in both themes, that surface reads as one thing, not two:

| | light | dark |
| --- | --- | --- |
| fill over the canvas | `rgb(244, 242, 238)` on `rgb(247, 245, 241)` — **3 of 255 levels**, contrast **1.027 : 1** | 3 of 255 levels over `#14130F` |
| inset ring over the canvas | `rgb(230, 228, 224)`, contrast **1.166 : 1** | contrast **1.261 : 1** |

The fill is below what the eye resolves, so the ring carries the whole signal: a service of 24 entries
draws 24 faint rectangles, and the page reads as a wireframe laid over the liturgy. The one divider in
the service that *means* something — the section break's 2px rule and diamond — is then the same kind of
mark as the 23 that mean nothing.

The box was also carrying separation that spacing owed. The rule written for it,
`.tatib__item + .tatib__item { margin-top: 2px }`, never matches in the editor because an `.entry__add`
row sits between two entries; the visible gap has always been that row's own `6px + 6px`, and the box
then added its `8px` padding top and bottom on top of it.

## User Scenarios & Testing

### US1 — An entry is the page until you point at it (P1)

**Why this priority**: this is the request. The resting surface is what the owner rejected, and every
other kind of entry inherits whatever this rule says.

**Independent Test**: open `/tatib/142/` and `/tatib/144/`, park the pointer off the page, and read the
entries: no fills and no outlines anywhere, in both themes, while the section breaks still draw their
rule.

**Acceptance scenarios**

1. **Given** a Tata Ibadah stage at rest in the light theme, **When** nothing is hovered or focused,
   **Then** every `.tatib__item--acts` and `.tatib__eos` computes `background-color: rgba(0, 0, 0, 0)`
   and `box-shadow: none`.
2. **Given** the same stage in the dark theme, **When** nothing is hovered or focused, **Then** the
   same two computed values hold.
3. **Given** any entry kind — text, scripture, song, media, section break — **When** it is at rest,
   **Then** it paints no surface of its own, and nothing about its geometry changes (see US3).

### US2 — The row appears when it is pointed at (P1)

**Why this priority**: removing the box is only safe if the hover affordance survives, because that is
the row's whole shape — it is what the pointer, the keyboard and an open modal all rest on.

**Independent Test**: hover one entry, then Tab to another, then open an entry's editor: each shows the
`--icon-hover-bg` fill over the same 8/8/8/12 box, and each returns to the canvas when the pointer, the
focus or the modal leaves.

**Acceptance scenarios**

1. **Given** an entry at rest, **When** the pointer enters it, **Then** it fills with
   `--icon-hover-bg` — `rgba(31, 31, 29, .08)` light, `rgba(255, 255, 255, .09)` dark — inside the same
   9px radius, with no outline and no layout shift.
2. **Given** the pointer leaves, **When** the 200ms `--ease` transition has run, **Then** the fill is
   gone and the entry is transparent again.
3. **Given** an entry reached by the keyboard, **When** it takes deliberate focus, **Then** it fills as
   on hover; a quiet focus restoration does not, exactly as spec 058 already requires.
4. **Given** an entry whose editor is open, **When** the modal is up, **Then** the entry behind the
   backdrop keeps its fill (spec 065, unchanged).

### US3 — Every kind keeps its own geometry and its own identity (P2)

**Why this priority**: the surface was the only thing the five kinds shared, so removing it must not
flatten them into one another. Media rows in particular are objects, not prose.

**Independent Test**: open `/tatib/144/`, which holds all five kinds in one service, and check each at
rest: the numbers below hold and each kind is still told apart by its own content.

**Acceptance scenarios**

1. **Given** a text, scripture or song entry, **When** it is at rest, **Then** it keeps `min-height:
   56px` and `padding: 8px 8px 8px 12px`, and its words sit at the same x as before.
2. **Given** a media entry, **When** it is at rest, **Then** it keeps `min-height: 80px`,
   `padding: 16px 16px 16px 64px` and its 42px icon tile at `left: 13px`, so it is still an object even
   though it no longer wears a box.
3. **Given** a section break, **When** it is at rest, **Then** it keeps its 56px box and draws its own
   2px `--divider` rule with the centre diamond — the only rule in the service.
4. **Given** any entry on a pane 700px wide or more, **When** it is drawn, **Then** the controls'
   column is still reserved (`padding-right: 264px`; `106px` below 700px), so no title runs under the
   buttons.

### Edge Cases

- **When** a row is hovered on a touch screen, where nothing can hover **Then** no fill appears and the
  controls are drawn at rest instead (the existing `(hover: none)` rule); the entry stays readable and
  every control stays reachable.
- **When** the add-row between two entries is revealed by hovering the entry above **Then** the gap it
  opens and the entry's own padding are unchanged, so nothing jumps as the row appears.
- **When** a long title or a long body wraps **Then** it wraps inside the same box it did before; the
  surface rules never set a width.
- **When** `prefers-reduced-motion: reduce` **Then** the fill still appears and disappears, without the
  200ms transition (existing rule).
- **When** an entry flashes after a save or a jump (`tatibFlash`) **Then** the flash still paints, since
  it is an animation and not the resting surface.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | At rest, `.tatib__item--acts` and `.tatib__eos` SHALL paint no background and no inset ring, in both themes: computed `background-color` is `rgba(0, 0, 0, 0)` and computed `box-shadow` is `none`. | `new: reading` |
| FR-002 | Hovering an entry, giving it deliberate keyboard focus, or owning its open modal SHALL fill it with `--icon-hover-bg`, and the fill SHALL leave when the pointer, the focus and the modal do; quiet focus restoration SHALL NOT fill it. | `new: reading` |
| FR-003 | The shape the fill occupies SHALL be unchanged: `min-height: 56px`, `padding: 8px 8px 8px 12px`, `border-radius: 9px`, and the reserved controls column at `106px` below a 700px pane and `264px` at or above it. | `new: reading` |
| FR-004 | A media entry SHALL keep `min-height: 80px` and `padding: 16px 16px 16px 64px` with its 42px icon tile at `left: 13px`; a section break SHALL keep its 56px box and draw its own 2px rule and diamond. | `new: reading` |
| FR-005 | `--tatib-entry-fill` and `--tatib-entry-outline` SHALL be removed from both themes, and no rule or test SHALL read them. | `new: reading` |
| FR-006 | No other surface SHALL change: the add rows, the controls' backing, the stage's flash, the sidebars, the editors, the dock and the projector keep their present styles. | `new: reading` |

### Key Entities

- **Service entry surface** — the resting paint of `.tatib__item--acts` and `.tatib__eos` in the Tata
  Ibadah stage; today a fill plus an inset ring, after this slice nothing.
- **Row fill** — `--icon-hover-bg` (`rgba(31, 31, 29, .08)` light, `rgba(255, 255, 255, .09)` dark), the
  one paint an entry can carry, shared with the rail's icon hover.
- **Entry kinds** — text, scripture, song, media and section break (`ServiceEntryKind`). The surface
  rules reach all five; only media and the break have geometry of their own.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Nothing is boxed at rest | computed `background-color` `rgba(0, 0, 0, 0)` and `box-shadow: none` on the first entry and on a section break, light and dark |
| SC-002 | The hover row still exists | hovering the first entry computes `rgba(31, 31, 29, 0.08)`; leaving it returns to transparent |
| SC-003 | Geometry is untouched | the reserved column still clears the controls by ≥4px; padding `8px 12px 8px`; `min-height` `56px`; the text column measures 976px at a 1440px window with both sidebars collapsed on `/tatib/142/` |
| SC-004 | All five kinds hold | on `/tatib/144/`: 15 entries — 1 text, 1 scripture, 4 songs, 3 media, 6 breaks — every one transparent at rest, media still 80px tall, breaks still drawing their rule |
| SC-005 | The tokens are gone | `--tatib-entry-fill` and `--tatib-entry-outline` return nothing from `getComputedStyle` in both themes, and `git grep` finds no reader |
| SC-006 | No regressions in the suite | `tests.test_design_tokens` 6/6 green; `tests.e2e.test_tatib_entry_controls` + `tests.e2e.test_tatib_hover` 35/36, the 36th being the pre-existing `test_touch_controls_remain_visible_after_dismissal`, red identically on `develop` (carded separately) |

## UI/UX

Measured in headless Chromium at 1440×900 against the real `tokens.css` and `components.css`, on the
live branch server (`/tatib/142/`, `/tatib/144/`) and in the static comparison at
`preview/preview.html`.

- **Resting surface**: none. `background-color: rgba(0, 0, 0, 0)`, `box-shadow: none`, both themes.
  Removed values, kept for the record: fill `rgba(31, 31, 29, .012)` → `rgb(244, 242, 238)` on the
  canvas (3/255, 1.027 : 1); ring `rgba(31, 31, 29, .08)` → `rgb(230, 228, 224)` (1.166 : 1);
  dark ring 1.261 : 1.
- **Hover / focus / modal-origin fill**: `--icon-hover-bg` — `rgba(31, 31, 29, .08)` light,
  `rgba(255, 255, 255, .09)` dark — inside the existing 9px radius, over the existing box.
- **Box**: `min-height: 56px`, `padding: 8px 8px 8px 12px`, `border-radius: 9px`; `padding-right:
  106px` below a 700px pane, `264px` at or above it. Media: `min-height: 80px`,
  `padding: 16px 16px 16px 64px`, 42px icon tile at `left: 13px`, 23px glyph. Section break: 56px box,
  2px `--divider` rule, 5px diamond at the centre.
- **Rhythm**: unchanged. Between two entries the text gap stays **32px** (4px last-line margin + 8px
  padding + the add-row's 6px + 6px + 8px padding); box-to-box it measures 12px, as it did.
- **Column**: on `/tatib/142/` at 1440×900 with both sidebars collapsed the reading pane is **1232px**
  and the text column **976px** — identical before and after. Text starts at x = 202 in the 1040px
  static preview column.
- **States**: resting (nothing), hover (fill), deliberate focus (fill), quiet focus restoration
  (nothing), modal-origin (fill), entry flash after a save (unchanged), touch (nothing at rest; the
  controls are drawn instead).
- **Motion**: none added or removed. The fill keeps its 200ms `--ease` background transition and the
  `prefers-reduced-motion` opt-out.
- **Unchanged by design**: the section break's rule and diamond, the media tile and its unavailable /
  missing colours, the add rows' reveal, the controls' backing, the sidebars, the editors, the dock and
  the projector.

## Assumptions

- **The two tokens are deleted, not zeroed.** A token that resolves to nothing keeps a dead concept
  alive in the palette; the two readers of it were this surface and two tests.
- **No outline is substituted.** A hairline on focus exists already (the 2px `--focus` outline); the
  resting state gets no mark, not a fainter one.
- **The vertical rhythm is left alone.** 32px between entries was judged comfortable in the preview;
  tightening it is a separate change, and it would move every entry on every service.
- **All five kinds are treated alike** (owner decision, 2026-10-28): media rows read as objects from
  their icon tile, filename and type line, so they need no surface of their own.
- **Spec 068 is superseded, not rewritten.** It stays the record of the box and its values; this slice
  says what replaced it. `specs/README.md` marks it superseded when this lands.
- **The preview tier is live.** The change is CSS on a server-rendered page, so the preview is the
  branch's own server (`http://localhost:8820/tatib/142/`, `/tatib/144/`); the static comparison in
  `preview/` is kept as the record of the four candidates that were weighed.
- **Dark mode is not a separate decision.** Both themes lose the surface; only the hover fill differs,
  as it already does.

## Clarifications

### Session 2026-10-28

- Q: Which entry surface should replace the border and the slight fill? → A: **bare at rest, filled while
  hovered** (owner, 2026-10-28).
- Q: Do media rows keep a surface of their own, being objects rather than prose? → A: **no — leave all
  kinds bare; media reads fine up close** (owner, 2026-10-28).
