# Research: Hymn songbooks above a single separator, the rest A–Z

**Spec**: `specs/128-songbook-hymn-separator/spec.md`
**Unknowns remaining**: 0

## D001 — The separator is a second panel group, not a new element

- **Decision**: render the Kidung panel as two `section.group` blocks and let the existing
  `.group + .group` rule (`static/styles/design/components.css:902` — `2px solid var(--divider)`, `10px`
  margin, `10px` padding; the mini variant at line 356 belongs to the Alkitab rail, which the Kidung panel never enters) draw the line.
- **Rationale**: the rule already separates Alkitab's testaments and Tata Ibadah's months, so the divider is
  the panel's own visual language; measured on the running page it is `2px` `rgb(217, 214, 205)` with the
  `22px` total gap between row edges. A new element or class would duplicate a rule the panel already owns, and
  a heading is excluded by the request.
- **Alternatives considered**: a `<hr>` between lists (a new primitive with its own margins, and the filter
  could not hide it with the group); a `border-bottom` on the last hymn row (ties the rule to a *row* rather
  than to the boundary, so it survives when the row is filtered out); a heading per group (the request forbids
  it and it would cost 27px per side).
- **Provenance**: research — `components.css`, the Alkitab and Tata Ibadah panels, and the running page.

## D002 — Alphabetical is a folded, ordinal key built in code, with the original name as tiebreak

- **Decision**: order ordinary songbooks by `(search_lib.normalize(name), name)` compared ordinally on the
  server, and by `(normalized(name), name)` with `<` / `>` in `static/web/offline-render.js`; never by the
  database's `ORDER BY name` / `Lower()`, and never by `localeCompare`.
- **Rationale**: the test suite runs on SQLite and production on PostgreSQL, and the two collate differently;
  `localeCompare` reads the browser's locale data, which the server does not have. The folded key makes
  `Buku Ende HKBP` sort under `b`, not after `Z`, and it makes the case-only pair
  (`Lagu Setelah persembahan` / `Lagu setelah persembahan`) fall back to a deterministic ordinal tiebreak —
  both measured in the page as adjacent, capital first.
- **Alternatives considered**: `order_by('name')` (collation-dependent, and PostgreSQL's `C` vs `id-ID` differ
  on punctuation); `order_by(Lower('name'))` (handles case, not diacritics, and still collates);
  `localeCompare` in the saved renderer (the same library name would order differently in a different browser).
- **Provenance**: research — `search_lib.normalize` (`multimedia/web/reading/search.py:57`), the saved renderer's
  `normalized()`, and the running page's measured order.

## D003 — Hymn order is untouched

- **Decision**: hymn songbooks keep descending non-deleted song count, with the name as tiebreak — the order
  the accepted mockup established (`HAL 507, KJ 502, PKJ 308, NKB 239` on this database).
- **Rationale**: the request changes only the non-hymn side, and the hymn side is the numbered corpus whose
  panel order was already accepted; re-sorting it alphabetically would put `Haleluya` before `Kidung Jemaat`
  by accident rather than by rule.
- **Alternatives considered**: alphabetical on both sides (rejected — not requested, and it discards the
  largest-first reading); number-range order (not modelled in the panel today).
- **Provenance**: owner request + the existing `_songbooks()` order.

## D004 — An empty group draws no separator

- **Decision**: the server skips a group with no rows; the client filter's existing `.is-hidden` on a group is
  paired with `.group.is-hidden + .group { margin-top: 0; padding-top: 0; border-top: 0 }`.
- **Rationale**: without the second half, filtering the hymn group away leaves the ordinary group's top border
  floating above the list with nothing above it — measured before the fix as `2px` surviving at the panel's top
  padding. The same guard reaches Alkitab's testaments and Tata Ibadah's months, where the identical filter
  already empties groups.
- **Alternatives considered**: re-rendering the panel on every filter keystroke from the server (a request per
  keystroke, and it fights the in-page filter); a `:has()` selector on the previous group (newer CSS than the
  page targets).
- **Provenance**: research — measured on the running page (`border-top: 2px` with the first group hidden,
  `0px` after the guard).

## D005 — One builder per side, shared by every route

- **Decision**: server — `_songbook_groups(selected_id)` returns the two groups and all three views pass it as
  `songbook_groups`; saved renderer — `songbookGroups()` / `songbooksPanel()` replace `sortedSongbooks()` and
  both call sites (`songPage`, `listPage`) use them.
- **Rationale**: the panel is built in three Django views and two saved-render paths; a grouping written once
  per call site is how spec 122's mismatches happened. Sharing the builder means a song page and the Kidung
  index cannot disagree.
- **Alternatives considered**: grouping in the template with a `{% regroup %}` (regroup needs a sorted flat
  list and cannot express the two-key sort); leaving the saved renderer on its old flat list (a saved page
  would drop the divider — the parity gap spec 122 and 127 closed).
- **Provenance**: research — the three `'songbooks': _songbooks(...)` call sites and the two
  `sortedSongbooks(...)` call sites.

## Open

<!-- empty: Phase 0 finished -->
