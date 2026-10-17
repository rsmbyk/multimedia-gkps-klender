# Plan 105: Search query grammar and ranking

- **Status:** Accepted (owner, 2026-10-17)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-105
- **Bump:** patch

## Why

Owner request, restated (2026-10-17): symbols are separators except the quote and the exclusion
dash; each word is a token; quoted phrases are searched as phrases; `-word` excludes; results rank
by how many tokens they match, then by how many appear in the query's order; the status line shows
the purged query; a lone exclusion explains itself. Matching stays substring-based — `kasih` still
matches `mengasihi` and `Kasih-Nya`.

Everything here lands on the page matcher (`search_page()`, introduced by spec 104) and the saved
copy (`offline-render.js` `searchPage()`). The legacy `search()` — the Go To's free-text fallback —
is a separate function and is not edited ("do not touch anything on goto. only search page"); the
owner confirmed the separation explicitly (2026-10-17: "separate the goto and search page search()
function to avoid future conflicts or bugs"). No Go-To behavior or test moves.

Today's page matcher cannot express any of this: it scores plain substrings on a 200/120/95/35/16
ladder, has no tokens, no phrases, no exclusion, and shows whatever the user typed.

## Scope / edges

**In:**

- `multimedia/web/reading/search.py`: `parse_query()` (tokens, canonical form, notice),
  `search_page()` matching and ranking (soft AND, coverage, order), excerpt anchoring.
- `multimedia/web/reading/views.py` `SearchView` + `templates/reading/search.html`: the canonical
  status line, the page title, and the two notices.
- `static/web/offline-render.js` `searchPage()`: the same parser, matching, ranking, canonical
  line, and notices.
- Tests: the grammar table (unit), the served page, one E2E walk, one saved-copy parity walk.

**Out:**

- The projector Go To (`search()`, `projector_lookup`, `projector-library.js`) — untouched.
- The fields themselves (spec 104), the look, group counts and `shown` paging, the offline payload,
  models and migrations, the editor pickers, the legacy `/api` endpoint.

## Approach

1. **Parser (`parse_query`).** One left-to-right scan over the folded-for-matching string that also
   keeps the typed spelling for display:
   - outside quotes: `"` toggles a phrase; `-` + word/`"` marks the next token excluded; any other
     non-alphanumeric becomes a space; letters and digits build words;
   - inside quotes: only `"` closes; every other non-alphanumeric, dash included, becomes a space;
   - the phrase is one token; empty tokens drop.
   Return a small structure: `tokens` (words, excluded flag, quoted flag), `canonical`, and
   `notice` (`exclusion_only` or `no_words`, else None). Unit-test the table first, including the
   owner's `Allah, "Tuhan. Yesus:Kristus" -kasih` → `Allah 'Tuhan Yesus Kristus' -kasih`.
2. **Matching (`search_page`).** For each corpus, fetch a superset with one `icontains` per include
   word (OR across words and fields — the same shape as today's candidate queries), then verify in
   Python on the folded field text: a token matches where `normalize(token) in normalize(field)`
   (substrings count — `kasih` matches `mengasihi`), a phrase where its folded words appear as one
   contiguous stretch, an excluded token anywhere drops the row; keep rows with coverage ≥ 1.
   Fields per row kind are spec 104's.
3. **Ranking.** Coverage descending, then the order score: per field, the longest run of matched
   tokens whose chosen match offsets increase in the query's order (subsequence, non-adjacent
   allowed, repeated tokens may take any occurrence). Compute it as an LCS-style DP over the
   query's tokens and the field's match offsets — greedy fails when the first token's earliest
   match sits late — and take the best field. Then `normalize(title)` ascending, as today. The
   ladder and `score` are not used by the page.
4. **Display.** `SearchResults` (or the page result object) carries `canonical` and `notice`;
   `SearchView` passes them to the template; `search.html` renders the canonical line, the page
   title, and the two notices in the existing `#searchStatus` paragraph. The field keeps
   `request.GET['q']` as typed; the URL is untouched.
5. **Saved copy.** Port the same parser, substring matcher, and offset-based ranking into
   `searchPage()`; build the same canonical line and notices; keep the existing group markup,
   counts, and paging. Keep one shared table of inputs → (rows, canonical, notice) in the tests so
   both renderers are checked against it.
6. **Excerpt.** Anchored on the first matched token in the row's body (phrase start for a quoted
   phrase), same 44/172 window.
7. **Docs and housekeeping.** Module docstring: `search()` is the Go To's frozen fallback,
   `search_page()` is the public page. Note that spec 105 supersedes spec 104's ladder. VERSION,
   changelog, ITEM-105, board in the implementation PR (patch).

## TDD

- Domain: `tests/test_web_search.py` — new `search_page()` tests: symbols to tokens; digits are
  words; quoted phrase is one token; dash inside quotes is ignored; `-word` excludes; exclusion
  only and symbols only give the notice and no rows; canonical table (owner's example, already-
  canonical input unchanged); substring match (`kasih` matches `mengasihi` and `Kasih-Nya`);
  phrase adjacency and a symbol between the words breaking it; coverage ordering; order ordering
  (in-order beats reversed); best-occurrence configuration; tie-break by title. The legacy
  `search()` tests stay green untouched.
- App: `multimedia/web/tests.py` — the served page shows the canonical status line, the exclusion
  notice, and partial matches below full ones.
- E2E: `tests/e2e/test_reading.py` — one grammar walk (quoted phrase + exclusion + canonical
  status). `tests/e2e/test_offline_library.py` — the same query table on the saved copy.
- Go To: no test change; `tests/e2e/test_projector.py` and the lookup tests must pass as-is.

## Risks

- **Soft AND widens results.** A multi-word query lists single-token matches below the full ones
  (owner's choice, 2026-10-17): `Tuhan Yesus` lists verses with only `Tuhan`, and `Kidung Jemaat`
  lists songs whose title or lyrics contain either word. Group counts will be large; that is the
  chosen semantics, not a regression.
- **Substring recall stays wide.** `kasih` matches `mengasihi`, `Kasih-Nya`, and `berkasih`
  (owner, 2026-10-17: tokens still match fragments). Order is therefore computed on match offsets,
  not word positions.
- **Phrase strictness.** A symbol between the words in the stored text breaks a quoted phrase;
  that follows "searches exactly". Unquoted tokens still match inside it.
- **Performance.** The candidate query is one `icontains` per include word; common words (e.g.
  `tuhan`) fetch thousands of rows and are scanned in Python. Measure the page on the prod copy
  before implementation; if it is slow, prefilter on the rarest token first.
- **Parity.** Two parsers (Python and JS) must agree on the canonical string and the order. One
  shared input table in the tests is the guard.
- **Separate matchers.** The page no longer calls `search()`; that function and its tests stay
  untouched, so the Go To cannot drift with page changes.
- **104 supersession.** 105 replaces the ladder 104 described; if 104 is accepted alone first, its
  ladder ships and is then replaced — note it in the changelog of the later PR.
