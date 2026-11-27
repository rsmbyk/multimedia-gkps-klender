# Research: sidebar mark centring

**Spec**: `specs/237-sidebar-mark-centering/spec.md`
**Unknowns remaining**: 0

## D001 — Where the fix belongs

- **Decision**: add `align-self: center` to `.songrow__mark` beside spec 063's number
  rule in `static/styles/design/components.css`, scoped to
  `:root[data-section="tatib"] #chList` and `.reorder__ghost`.
- **Rationale**: the row is a flex line with `align-items: baseline`. The number's
  `align-self: center` already makes its box centre match the row centre (0px), while
  the mark without it reads −4px on one-line rows, −11.5px on a two-line song row and
  −22px at 390px. The same declaration is the smallest change that puts both columns
  on one rail.
- **Alternatives considered**: changing the row to `align-items: center` would move
  the label off its baseline, which spec 063 explicitly preserved; absolutely
  positioning the mark at `top: 50%` would detach it from the flex gap and need a
  new horizontal offset.
- **Provenance**: live measurement on the slice worktree at `1440×900` and `390px`,
  `components.css:1709-1724` (row and number) and `components.css:1737-1741` (mark).

## D002 — Scope: contents list and drag copy only

- **Decision**: keep the selector under `:root[data-section="tatib"] #chList` and add
  the same declaration for `.reorder__ghost`, exactly as spec 063 did for the number.
- **Rationale**: the songbook sidebar shares `.songrow` but renders no mark; the OBS
  dock has its own rows. Scoping prevents a future mark elsewhere from silently
  changing alignment.
- **Alternatives considered**: a global `.songrow__mark { align-self: center }`
  would also change any future non-contents use of the class, with no benefit here.
- **Provenance**: spec 063's implementation note, spec 214's scope note, and the
  `test_dock_and_projector_keep_their_own_rows` assertion in
  `tests/e2e/test_sidebar_kind_marks.py`.

## D003 — Slot badge follows its mark

- **Decision**: do not change `.slot__badge` or its offsets; let the absolutely
  positioned badge move with the centred mark box.
- **Rationale**: the badge is positioned against `.songrow__mark--slot`
  (`right: -3px; bottom: -2px`), so centring the parent moves the badge by the same
  4px. Measured: bottom offset from the row goes 13px → 9px, left stays 50px.
- **Alternatives considered**: compensating the badge's `bottom` would keep its
  old absolute y but break its corner relationship to the mark.
- **Provenance**: live measurement on a fill-in row in service `111ojo`.

## D004 — Verification depth before the push step

- **Decision**: one targeted E2E module for the row, wrap and badge boxes; the full
  browser suite is deferred to the push step.
- **Rationale**: a two-selector CSS change has a narrow blast radius; you asked for
  targeted verification between pushes and heavy suites at push.
- **Alternatives considered**: running the whole E2E suite now would repeat unrelated
  red tests already recorded on `develop` and add no evidence for this rule.
- **Provenance**: owner decision; research inconclusive.

## D005 — Preview shape

- **Decision**: keep the live preview and its probe script; no chat-frame `::preview`.
- **Rationale**: the evidence needs the real service rows and their marks, which are
  server-rendered; a copy of the CSS cannot prove the row's actual boxes. The probe
  reads the shipped page and reverts only the mark's `align-self` inline for the
  control numbers.
- **Alternatives considered**: a static page would need duplicated markup and CSS,
  and the `before` column would silently follow the working tree; a screenshot is not
  a preview.
- **Provenance**: live preview at `127.0.0.1:8776`, `preview/README.md`.

## Open

None.
