# Research: a contents row marks its entry's kind

**Spec**: `specs/214-sidebar-entry-kind-marks/spec.md`
**Unknowns remaining**: 0

## D001 — One partial, one new class, no stage-CSS coupling

- **Decision**: add `multimedia/web/templates/reading/_toc_mark.html`, included from `_toc.html`
  between `.songrow__c` and `.songrow__t`. It branches on `item.mark` and writes inline SVG inside a
  single `.songrow__mark` span; a slot's mark carries the spec 213 corner badge with
  `data-kind-badge` from `item.mark_kind`.
- **Rationale**: `_toc.html` is the only live renderer of these rows (`tatib.html` includes
  `reading/_toc.html` into `#chList`); the saved renderer was removed by spec 136. One partial keeps
  every glyph in one place and keeps the row template readable. The glyph paths are copied from
  `_entry_kind_icon.html`, `_slot_mark.html` and `_slot_kind_badge.html` rather than those partials
  being included: including them would bring `.entry__kind-icon` and `.slot__mark` with their own
  absolute positioning and 20px sizing, forcing a stack of sidebar overrides, and would put
  `.entry__kind-icon` inside `#chList`, which spec 144's `test_the_sidebar_and_dock_keep_their_own_rows`
  still counts as zero. The sidebar's mark is a different mark in the same stroke language, not the
  stage's element.
- **Alternatives considered**: (a) include the stage partials and override their CSS — rejected for
  the coupling and the test above; (b) a client script keyed on a `data-*` attribute — rejected: the
  kind is known at render time, and a script would leave the column empty on the first paint;
  (c) a CSS `::before` with a font glyph — rejected: the product draws its marks as inline SVG with
  `stroke="currentColor"`, and there is no kind-icon font.
- **Provenance**: research (`multimedia/web/templates/reading/_toc.html:20-26`,
  `tatib.html:7,92-95`, `docs/spec/reading.md:45-49`, `tests/e2e/test_stage_kind_marks.py:215-223`).

## D002 — Which value drives each mark

- **Decision**: `_tatib_stage()` adds `mark` (and `mark_kind` for slots) to each `toc` row. Values:
  `text` for a legacy text row and a text entry; `scripture`, `song`, `media` for those entry kinds;
  `fill_in` / `choice` for slots with `mark_kind` = the lowercased `SlotKind` name; no mark on a
  section break (entry or legacy EOS), whose divider is already its mark.
- **Rationale**: the kind is already resolved for every row at `views.py:1400` (`kind_name`) and
  `:1407-1409` (`slot_kind`). A UI-side `mark` key keeps the template a pure consumer and lets a legacy
  row, which carries no `kind` field, be marked as text from its own shape. No model field or migration
  is needed, matching FR-003.
- **Alternatives considered**: deriving the glyph from `song_label` / `eos` / `label` in the template —
  rejected: it confuses a song's availability with its kind and cannot tell a media file from a passage.
- **Provenance**: research (`multimedia/web/reading/views.py:1371-1559`, especially `:1393-1395`,
  `:1407-1409`, `:1474-1477`, `:1486-1489`, `:1554-1559`; `multimedia/tatib/models.py:133-149`).

## D003 — B's geometry: 24px number box, 8px gap, 16px mark

- **Decision**: in the `#chList` scope only, `.songrow__c` gets `min-width: 24px`, `.songrow` gets
  `gap: 8px`, and `.songrow__mark` is `flex: none; 16 × 16px`. The number keeps its 10px left padding
  and its `:root[data-section="tatib"]` vertical centring. A fourth digit is allowed to grow the box
  rather than clip the number.
- **Rationale**: measured on the static preview at a 404px pane, 1×, both themes: the 24px box holds
  up to 999, the mark starts at 42px and the label at 66px (8.39px left of today's 74.39px); the list
  height stays 354.25px and no numbered row changes height. Growing past three digits keeps the number
  readable; clipping it would break spec 063's centring test and lose information.
- **Alternatives considered**: candidate A (leave the 54.39px box, push the label right 26px) — seen
  by the owner and not taken; a 20px mark matching the stage — rejected because it would change a
  row's 52px rhythm at the 404px pane; shrinking the number's font — rejected, it would make the numbers
  smaller than the spec 063 figure.
- **Provenance**: `specs/214-sidebar-entry-kind-marks/preview/index.html` and `preview/probe.py`
  (numbers in the spec's UI/UX); owner decision 2026-11-21.

## D004 — The slot's corner modifier at 16px

- **Decision**: for `fill_in` and `choice`, the mark keeps the dashed 20-viewBox frame and the `+` /
  `◎` path, and carries the spec 213 badge partial's four 12-unit glyphs on an **11px** disc with an
  **8px** glyph, overhanging 3px right / 2px bottom. The disc paints `--canvas` and re-lays
  `--icon-hover-bg` in the row's fill states, by the same gradient mechanism spec 213 adopted.
- **Rationale**: the owner asked for the modifier explicitly. Scaling spec 213's 13px disc to the
  16px sidebar mark keeps the badge a modifier of the mark, not a second mark; the 12-unit glyph grid
  holds a resolvable stroke at 8px. The badge names the resolved kind, which the row already prints in
  words (`Fill-in · Song`), so it repeats rather than replaces that label.
- **Alternatives considered**: a bare dashed mark — rejected by the owner; the full 13px/10px badge
  unchanged — rejected because it is 81% of a 16px mark and buries the frame; no badge when the slot's
  kind is unreadable — kept as the legacy degradation from spec 213 FR-007.
- **Provenance**: `multimedia/web/templates/reading/_slot_kind_badge.html`,
  `specs/213-slot-kind-badge/spec.md` §UI/UX, `preview/probe.py` after the badge was added (list height
  unchanged at 354.25px).

## D005 — The break row is not marked

- **Decision**: `li.toc__eos` keeps its rule and gains no mark, for a section-break entry and a legacy
  EOS row alike.
- **Rationale**: it paints no visible order number, so the new column has no seat; its rule is the
  break's own mark. Adding one raised the divider row from 13px to 24px in the preview (+11px list
  height) and would disturb a geometry other specs fixed. The owner chose B from a preview with no
  mark on that row; the question was skipped with its recommendation recorded at Clarify.
- **Alternatives considered**: a diamond mark before the rule — rejected as above; reusing the
  number column for the break — rejected because that would paint a number the product deliberately
  omits.
- **Provenance**: `preview/index.html` columns B (with and without the break mark),
  `specs/214-sidebar-entry-kind-marks/spec.md` §Clarifications.

## D006 — Verification split

- **Decision**: the rendered-markup behaviours are Django tests in `multimedia/web/tests.py`; the
  geometry, states and cross-surface exclusions are Playwright E2E in a new
  `tests/e2e/test_sidebar_kind_marks.py`. Frozen geometry from specs 063, 135, 137, 144 and 213 stays
  covered by its own suites.
- **Rationale**: the repo declares TDD for domain and application rules and Playwright for
  user-visible acceptance. Markup presence is a render fact a Django test can assert; a 16px column's
  effect on wrapping and contrast needs a browser.
- **Alternatives considered**: one E2E file for everything — rejected: it would test render facts with
  a browser and run slower; no test for the mark set — rejected: SDD-13 needs a verifiable row for each
  FR.
- **Provenance**: `docs/PROCESS.md` "Tests — tdd" repo block; `multimedia/web/tests.py:3619+`
  (`SlotKindBadgeTests`), `tests/e2e/test_toc_number_centering.py`,
  `tests/e2e/test_stage_kind_marks.py`.
