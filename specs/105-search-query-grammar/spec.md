# Spec 105: Search query grammar and ranking

- **ID:** 105
- **Status:** Draft
- **Item:** ITEM-105
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

The owner defines how the search page reads a query (2026-10-17): symbols are separators; each
word (or quoted phrase) is a token; `-word` excludes; results rank by how many tokens they match,
then by how many of those appear in the query's order; the status line shows the purged query; a
lone exclusion says why it lists nothing.

Spec 104 says *which fields* may match. This spec is the query layer over them: how the typed
string is cut into tokens, how a result qualifies, how it ranks, and what the page shows. It
replaces spec 104's ranking ladder on the search page; 104's field scope stands either way. The
projector's Go To is out of scope and untouched (owner, 2026-10-17).

## Scope

### In scope

- The parser: symbols to spaces, words as tokens, quoted phrases, `-` exclusions, digits as word
  characters, case and diacritic folding.
- Matching: soft AND over the spec-104 fields — a result lists when it matches at least one include
  token in any field and no excluded token in any field.
- Ranking: matched-token count first, then token order, then the existing title order.
- The canonical (purged) query string: rebuilt from the tokens, shown in the status line and page
  title; the field and the URL keep what was typed.
- The two queries that have no word to search: an exclusion-only query and a symbols-only query
  list nothing and say why.
- Parity: the saved-copy renderer (`static/web/offline-render.js` `searchPage()`) parses, matches,
  ranks, and displays the same way.

### Out of scope

- The projector's Go To — untouched, no code, behavior, or test change (owner: "do not touch
  anything on goto"). Its fallback keeps calling the legacy `search()`, which this spec does not
  edit.
- The field set itself — spec 104 (verse text/title, song title/lyrics, service name, row title,
  text-entry body).
- The look: groups, row shapes, group counts, `shown` paging, and the clear control. Only the
  status line's text, the two notices, and the excerpt anchor change.
- The offline payload (`offline.py`) and sync; models and migrations.
- Ranking across corpora — the three groups stay separate.
- The editor pickers' filters and the legacy `/api` search endpoint.

## Domain rules

### Words, symbols, tokens

- Fold case and diacritics for matching; the typed spelling is kept for display.
- A **word** is a maximal run of letters and digits. Digits are word characters: `152` is a word
  and `5:13` is two words (`5`, `13`).
- Everything that is not a letter or a digit is a **symbol**. Outside quotes a symbol separates
  words — except `"` and the exclusion dash, which the rules below give a role.
- Outside quotes:
  - `"` opens or closes a phrase. An unclosed `"` runs to the end of the query.
  - `-` immediately followed by a letter, digit, or `"` marks the next token as excluded; anywhere
    else it is a symbol.
- Inside quotes every character is literal text except the closing `"`: symbols, **including the
  dash**, become spaces.
- Each bare word is one token. Each quoted phrase is **one** token whose words must appear
  consecutively (a phrase is not split into separate tokens).
- Empty tokens are dropped.

### Matching

- A token matches a result when one of the result's searchable fields contains it — whole words
  only, never a fragment: `kasih` does not match `mengasihi`. A phrase matches where its words
  appear consecutively in one field.
- Searchable fields are spec 104's, per row kind: verse — title, text; song — title, lyrics (live
  verses joined in order); service — name; row — title, body.
- **Coverage** = how many distinct include tokens the result matches. A token found in two fields
  still counts once; occurrences do not add up.
- A result is listed when coverage is at least 1 and no excluded token matches any of its fields.
  This is the soft AND: results with every token rank first, results with fewer still list below.

### Ranking

1. **Coverage**, descending — more matched tokens first.
2. **Order**, descending — the longest run of matched tokens that appears in the query's own order
   inside one field. Words need not be adjacent; a repeated token may take any occurrence; the
   longest run over the best field and the best occurrences is used. A single matched token scores
   1.
3. **Title**, normalized ascending — the existing deterministic tie-break.

More coverage always beats better order. Ranking stays inside each group; the three groups stay
separate.

### Canonical query

- Rebuild the query from its tokens, in the typed order: words joined by single spaces; a phrase
  as `'word word'` (single quotes); an exclusion as `-word` or `-'word word'`. Case and word
  spelling stay as typed; symbols are gone.
- The status line and the page title show the canonical form. The search field and the URL keep
  the typed text.
- When the canonical form equals the typed text, the page reads the same as today.

### No words to search

- With at least one exclusion and no include token: nothing is listed, and the status line reads
  **“Nothing to search — an exclusion like “-Israel” needs at least one other word.”**
- With no tokens at all (symbols only): nothing is listed, and the status line reads
  **“Nothing to search — add at least one word.”**
- With include tokens but no matches: today's line, **“No results for “<canonical>”. Try another
  keyword.”**
- An empty or whitespace-only query keeps returning the landing, as today.

### Both renderers

The saved copy applies the same parser, matching, ranking, canonical form, and notices. For the
same input the two renderers produce the same canonical string and the same order.

## UI details

- **Status line:** the existing `<p class="search-results__intro" id="searchStatus" role="status">`.
  Text `Results for “<canonical>”` — curly double quotes around the whole query, single quotes
  around phrases, so `Allah, "Tuhan. Yesus:Kristus" -kasih` reads
  `Results for “Allah 'Tuhan Yesus Kristus' -kasih”`.
- **Page title:** `Results for “<canonical>” — GKPS Klender`.
- **The field and URL** keep the typed query; only the status line and page title show the
  canonical form.
- **Notices:** rendered in the same paragraph with `role="status"`, no groups; the field keeps the
  typed query.
- **Excerpts:** unchanged window (44 characters before, 172 wide), anchored on the first matched
  token in the row's body (the phrase start for a quoted phrase).
- No other class, spacing, or colour changes.

## Acceptance scenarios

### Scenario: Symbols separate words

- **When** I search `Allah, Tuhan. Yesus:Kristus`
- **Then** it reads four tokens — `Allah`, `Tuhan`, `Yesus`, `Kristus`, in that order

### Scenario: Soft AND lists partial matches below full ones

- **Given** one text with both `Tuhan` and `Yesus` and another with only `Tuhan`
- **When** I search `Tuhan Yesus`
- **Then** the text with both ranks above the text with one, and both are listed

### Scenario: More tokens beat better order

- **Given** a text with both query tokens out of order and a text with one token
- **When** I search the two-word query
- **Then** the two-token text ranks above the one-token text

### Scenario: Order ranks within equal coverage

- **Given** two texts that contain the same tokens, one in the query's order and one reversed
- **When** I search the phrase's words unquoted
- **Then** the in-order text ranks first

### Scenario: The best occurrence configuration is used

- **Given** a text where the first occurrence of the second token precedes the first token, and a
  later occurrence follows it
- **When** I search both tokens
- **Then** the text counts the ordered pair, not the reversed one

### Scenario: A quoted phrase matches only as a phrase

- **When** I search `"Tuhan Yesus"`
- **Then** only rows where `Tuhan Yesus` appears consecutively are listed — a row with `Yesus`
  before `Tuhan` is not

### Scenario: Symbols inside a phrase are ignored, dashes included

- **When** I search `"Tuhan. Yesus:Kristus"` or `"Tuhan -Yesus"`
- **Then** both read the phrase `Tuhan Yesus` (and the second drops the dash, not the word)

### Scenario: A dash excludes

- **Given** a row containing both `Bangsa` and `Israel` and a row with only `Bangsa`
- **When** I search `Bangsa -Israel`
- **Then** the row containing `Israel` is not listed, the other is

### Scenario: A lone exclusion explains itself

- **When** I search `-Israel`
- **Then** nothing is listed, and the status line reads “Nothing to search — an exclusion like
  “-Israel” needs at least one other word.”

### Scenario: Symbols only

- **When** I search `---`
- **Then** nothing is listed, and the status line reads “Nothing to search — add at least one
  word.”

### Scenario: The status line shows the purged query

- **When** I search `Allah, "Tuhan. Yesus:Kristus" -kasih`
- **Then** the status line reads `Results for “Allah 'Tuhan Yesus Kristus' -kasih”`, the field
  still holds the typed text, and the URL still carries it

### Scenario: The saved copy agrees

- **Given** the offline library is ready
- **When** I repeat the queries above on the saved-copy renderer
- **Then** the same rows, the same order, the same canonical status line, and the same notices

### Scenario: The Go To is unchanged

- **Given** the projector's Go To find
- **When** I type a query there
- **Then** it behaves exactly as today — this spec does not edit `search()` or any projector path

## Traceability

- Domain/app tests: `tests/test_web_search.py` — new `search_page()` tests: tokenizing and
  canonical form (the owner's example included), whole-word and phrase matching, exclusion,
  exclusion-only and symbols-only notices, coverage and order ranking (including the best
  occurrence configuration and the tie-break); the legacy `search()` tests stay green untouched
  (Go To). `multimedia/web/tests.py` — the served page: canonical status line, exclusion notice,
  partial matches listed below full ones.
- E2E: `tests/e2e/test_reading.py` — one grammar walk on the served page (phrase, exclusion,
  canonical status); `tests/e2e/test_offline_library.py` — the saved-copy parity walk over the same
  query table.
- Go To: no code and no test change — `tests/e2e/test_projector.py` and the projector-lookup tests
  in `multimedia/web/tests.py` stay green untouched.
- Implementation: `multimedia/web/reading/search.py` (`parse_query()`, `search_page()`),
  `multimedia/web/reading/views.py` (`SearchView`'s canonical query and notice),
  `multimedia/web/templates/reading/search.html`, `static/web/offline-render.js` (`searchPage()`).
