---
id: ITEM-105
status: in_review
title: 'Search query grammar and token ranking'
type: feat
priority: P1
effort: L
created: 2026-10-17
updated: 2026-10-17
spec: [105](../../specs/105-search-query-grammar/spec.md)
branch: feat/105-search-query-grammar
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.13.6
---

# ITEM-105: Search query grammar and token ranking

## Summary

The search page treats the whole query as one substring. The owner defined a grammar instead:
symbols separate words (the quote and the exclusion dash excepted), each word or quoted phrase is
a token, `-word` excludes, results rank by matched-token count then token order, and the status
line shows the purged query. A lone exclusion explains why it lists nothing.

## Notes

- Owner rules, 2026-10-17 (twelve rules; recorded in spec 105's Domain rules).
- Owner chose soft AND: all-token results rank first, partial matches still list below.
- Tokens still match substrings/fragments (owner, 2026-10-17): `kasih` matches `berkasih` and `Kasih-Nya`.
- The owner asked for the Go To and the page to use separate search functions ("separate the goto
  and search page search() function to avoid future conflicts or bugs"); `search_page()` is the
  page's matcher and the legacy `search()` stays the Go To's fallback.
- Supersedes spec 104's ranking ladder on the search page; spec 104's field scope stands.

## Acceptance sketch

- `Allah, Tuhan. Yesus:Kristus` reads four tokens; `5:13` reads two.
- `Tuhan Yesus` ranks the both-token text above the one-token text; more tokens beat better order.
- `"Tuhan Yesus"` matches only the contiguous phrase; symbols inside quotes are ignored, dashes
  included.
- `Bangsa -Israel` drops rows containing `Israel`.
- `-Israel` alone lists nothing and says why; `---` lists nothing and says why.
- `Allah, "Tuhan. Yesus:Kristus" -kasih` shows `Results for “Allah 'Tuhan Yesus Kristus' -kasih”`;
  the field and the URL keep the typed text.
- The saved copy agrees; the Go To is unchanged.

## Links

- Spec: [105](../../specs/105-search-query-grammar/spec.md)
- Plan: [105](../../specs/105-search-query-grammar/plan.md)
- Related items: ITEM-104 (the field scope), [ITEM-021](./ITEM-021-search-reset-state.md) (spec
  019 — search state)
