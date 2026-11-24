# Research: passage search comboboxes

**Spec**: `specs/238-passage-search-pickers/spec.md`
**Unknowns remaining**: 0

## D001 — What "same dropdown as the song picker" means

- **Decision**: make Book, Chapter and From verse `INPUT[type=search]` triggers with the
  song field's `.editor__songsearch` chrome, type-to-filter, Arrow/Enter/Escape and a
  viewport-capped menu anchored to the field.
- **Rationale**: the owner chose this explicitly over "same look only" and "shared code,
  click-to-open". The song picker's defining behaviour is the field-as-trigger, not its
  server fetch.
- **Alternatives considered**: restyle the button trigger while keeping the filter inside
  the menu (rejected — different interaction); add a shared component and change all four
  pickers (rejected — To verse is out of scope and the song path is green).
- **Provenance**: owner answer at slice start; `_entry_form.html:184-197` (song field) and
  `:63-158` (passage fields); `entries.js:760-880` (`wireSongPicker`).

## D002 — Filtering source: local options, no new endpoint

- **Decision**: filter the option elements already in the modal — book names/codes from
  `data-book-name-*`/`data-book-code-*`, chapter and verse numbers from `data-value`.
- **Rationale**: all 66 books are server-rendered into the menu; chapter numbers are built by
  `fillChapters()` and verses by `loadVerses()`. A fetch per keystroke would add endpoints
  for data already present, and SC-003 forbids that.
- **Alternatives considered**: mirror `/editor/entry/songs/?q=` with `/books/?q=`,
  `/chapters/?q=` and `/verses/?q=` — three endpoints, three new views and no user-visible
  gain at this list size.
- **Provenance**: `_entry_form.html:80-91`, `entries.js:490-530`, `entries.js:712-730`.

## D003 — Keep the hidden selects as the value carriers

- **Decision**: leave `book_translation`, `chapter`, `verse_start` and `verse_end` as hidden
  `<select>` elements; the search field is display and query only.
- **Rationale**: server validation, the translation-aware book id and the To verse range all
  read those selects. Keeping them means zero server change and an unchanged POST payload.
- **Alternatives considered**: post the field's label and resolve it server-side — adds a
  translation/ambiguity problem and changes validation.
- **Provenance**: `entries.js:489-560` (`chosenBook`, `fillChapters`, `syncTo`, `loadVerses`);
  live probe: book hidden `69`, chapter hidden `10`, from hidden `1` after the cascade.

## D004 — Escape must not clear the chosen label

- **Decision**: `preventDefault()` on Escape in the new combos before closing the menu.
- **Rationale**: a native search input clears its value on Escape; the live probe measured
  Chapter's field going from `"10"` to `""` while its hidden select stayed `10`. That leaves
  the UI contradicting the form. The song picker's handler is left untouched (SC-004).
- **Alternatives considered**: let both pickers clear on Escape for parity — copies a defect
  into three new controls; changing the song picker too — outside scope and breaks its pins.
- **Provenance**: `preview/probe.py` checkpoints `after_from_chosen` vs `after_escape`.

## D005 — Shared interaction helper, song picker unchanged

- **Decision**: add `wireSearchCombo(config)` for the three passage fields; do not refactor
  `wireSongPicker`. Add one shared `.is-active` CSS rule so keyboard choice is visible.
- **Rationale**: the song module has 10 green pins from spec 210; duplicating ~60 lines in a
  helper is cheaper than rewiring a passing path and risking its fetch/verse-checklist contract.
  The class was already applied by both pickers but had no rule — a single tint serves both.
- **Alternatives considered**: extract one helper for all four — higher blast radius with no
  user-visible difference; CSS-only keyboard highlight via `:focus-within` — cannot identify
  which option is active.
- **Provenance**: `tests/e2e/test_song_entry_pickers.py`; `components.css:2702-2716`; live
  probe reported 2 stale active options before the helper cleared them on refresh, 1 after.

## D006 — Verification strategy

- **Decision**: a new E2E module for the four stories plus targeted regression of the song
  module; migrate the three stale selectors in `test_entry_pickers.py`.
- **Rationale**: the new module is the independent test US1–US4 ask for; the song module is the
  green regression check; the legacy module is already red on develop (`ITEM-174`) but its
  selector assumptions must still be updated so it is not additionally broken by this slice.
- **Alternatives considered**: reuse `test_entry_pickers.py` alone — its backdrop race makes
  any result ambiguous; skip the legacy migration — leaves known-stale selectors behind.
- **Provenance**: live run of `tests.e2e.test_song_entry_pickers` (9 pass, 1 known-red on base
  `88b300bf`), `tests/e2e/test_entry_pickers.py:314-720`, board `ITEM-174`.
