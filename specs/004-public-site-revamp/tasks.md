# Tasks 004: Public site revamp

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from `develop` (`feat/004-public-site-revamp`)
- [x] Red — `tests/test_design_tokens.py`: contrast pairs fail against current `tokens.css`
- [x] Green — rewrite `static/styles/design/tokens.css` to the spec's pinned palette and
      metrics (light + dark) until the contrast test passes
- [x] Red — `tests/test_web_search.py`: reference parsing (`Kidung Jemaat 120` ≡ `KJ 120`,
      `Matius 5:13`), ranking rules, minimum query length — failing
- [x] Green — `multimedia/web/reading/` search view + URL: cross-corpus query (Bible,
      Kidung, Tata Ibadah), grouped results, reference-first ranking, minimum length
- [x] Green — reading views + URLs for Bible (books/chapters) and Tata Ibadah (service
      list + order), rendering the existing models
- [x] Red — E2E: search-first home, grouped results, reference resolution, validation,
      keep-last-results, sidebar open/close/restore, dark mode, print, no-overflow
- [x] Green — `multimedia/web/templates/reading/base.html` — rail shell: logo, destinations
      (Search / Alkitab / Kidung / Tata Ibadah), theme toggle, tooltips, `data-*` state
      attributes, inline pre-paint theme script
- [x] Green — `reading/home.html` — search-first landing (96px logo, 56px field, 610px
      column, example-query hint)
- [x] Green — `reading/search.html` — results (group heads Alkitab / Kidung / Tata Ibadah,
      counts, excerpts, *Show more*, validation message, empty state)
- [x] Green — `reading/bible*.html` — chapter reading (verse numbers, TB/SIM toggle,
      search-target marking) plus books/chapters sidebar markup with mini collapse
- [x] Green — `reading/song*.html` — songbook panel + wide song list + lyrics (stanza
      numbers, citation eyebrow)
- [x] Green — `reading/tatib*.html` — service list (year+month groups, Templates view),
      contents quicklinks, service order stage (speaker marks, quiet end-of-section notes,
      date-only eyebrow)
- [x] Green — `static/styles/design/components.css` rebuilt: rail, push panels with
      clip-wipe, mini collapse, song-list swap below 1272px, overlays ≤720px, reader
      typography, tooltips, print block
- [x] Green — `static/web/reading.js` (new, dependency-free): state machine (`nav`, `ch`,
      `read`, `home`, `section`, `theme`), parent-first rails, content-based restoration,
      search destination semantics (keep last results, exclusive `aria-current`),
      validation wiring, tooltips
- [x] Green — dark mode: persistence (`gkps-*` keys), pre-paint restore, AA in both modes
- [x] Parity harness: re-run the mockup's browser-check suite (search, rail, reader, Tata
      Ibadah modes, restoration, highlight exclusivity, widths 320–1440) against the
      implementation — every check green on the mockup must be green here
      (run 2026-10-03: 111/111 green)
- [x] Parity review: side-by-side against the mockup at acceptance — structure, states,
      copy (terms, dates), metrics (80/64px rail, 610/690px columns, breakpoints), plus a
      pixel comparison of the key views (home, results, each reading kind) at fixed
      viewports; list any deliberate deviations in the PR
      (segmented pixel comparison: home + results byte-identical; bible/song/tatib
      ≤ 0.00004 RMSE, antialiasing level; deviations in the PR)
- [x] Retire the mockup **only after** parity passes pixel-perfect — keep
      `scratch/revamp-mockup/` (and the Hermes working copy) until then
      (parity passed 2026-10-03; both copies retained — removal follows owner sign-off)
- [x] Verify existing suites still green: `multimedia.web`, `tests.e2e.test_reading`,
      maintenance test (2026-10-03: 46 unit + 12 e2e + full run 66 OK)
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: minor` on ITEM and spec header
- [x] `VERSION` → 0.8.0, changelog `## [0.8.0] - 2026-10-03`, `release_version` in **this PR**
- [x] Update ITEM-005 + [`backlog/board.md`](../../backlog/board.md) in **this PR**
      (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Commands

```bash
DJANGO_DEVELOPMENT_MODE=True .venv/bin/python manage.py test \
  tests.test_design_tokens tests.test_web_search multimedia.web

# E2E needs the browser binary once:
#   .venv/bin/playwright install chromium
DJANGO_DEVELOPMENT_MODE=True .venv/bin/python manage.py test tests.e2e.test_reading
```

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Token contrast test green in light and dark (pinned palette)
- [x] Search-first home; grouped search over Bible, Kidung, Tata Ibadah; references rank
      first; `Kidung Jemaat 120` ≡ `KJ 120`
- [x] Minimum 3 letters/numbers enforced; an invalid query never clears the last results
- [x] Search icon keeps the last result set; logo starts fresh; indication exclusive to
      closed sidebars
- [x] Nested sidebars: parent-first, mini collapse (Bible), song-list swap (Kidung),
      year+month groups + templates (Tata Ibadah), quicklinks unselected, content-based
      restoration
- [x] English chrome + Indonesian terms and dates (`23 Agu 2026`, `Agustus 2026`)
- [x] Dark mode persists with no flash; print yields reading content only
- [x] No horizontal scroll at 320px; rail narrows 80px → 64px at 560px
- [x] Existing `multimedia.web` + e2e + maintenance suites green
- [x] Board, tasks, and version complete in this PR
