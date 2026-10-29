# Contract: `window.gkpsAgeBuckets`

**Slice**: `specs/146-media-and-transfer-age-buckets`
**Interface**: a browser global, not an HTTP endpoint. The companion's API (`/v1/...`) is unchanged, and no
server route is added, so this is the only interface this slice introduces.

Defined once in `static/web/age-buckets.js`, loaded by `base.html` before `media-library.js` and
`media-handoff.js`. Two surfaces and the browser suite are its callers.

```js
window.gkpsAgeBuckets = {
  FILE_BUCKETS,        // read-only: [{ key, label }, …] in ladder order
  TRANSFER_BUCKETS,    // read-only: [{ key, label }, …] in ladder order
  presentDay(nowMs),   // → Number: the Jakarta calendar day of nowMs, at UTC midnight
  todayIso(nowMs),     // → String: 'YYYY-MM-DD' in Asia/Jakarta, for date comparisons
  fileKey(file, nowMs),       // → String: a key of FILE_BUCKETS
  transferKey(transfer, nowMs), // → String: a key of TRANSFER_BUCKETS
  group(rows, keyOf, ladder)  // → [{ key, label, rows }, …]: only non-empty buckets, ladder order
}
```

## Guarantees

1. **Total.** Every row gets exactly one key and no key outside the ladder is ever returned. A row whose
   timestamp will not parse is drawn in `older` rather than dropped, so a malformed companion row still
   appears in the list it came from.
2. **Pure.** No argument is mutated, no DOM is touched, nothing is fetched or stored. `nowMs` defaults to
   `Date.now()` only when omitted.
3. **Ladder order.** `group()` returns buckets in ladder order and never an empty one, so a caller draws
   headings by iterating the result.
4. **Jakarta.** Every day and year decision is the congregation's (`Asia/Jakarta`), per `reading/R9` — never
   the server's UTC date and never the browser's local zone.
5. **Labels.** `label` is sentence case; the uppercase in the UI is `.media-library__group` /
   `.media-transfers__group` doing the transforming, so an accessible name keeps its words.

## What each caller may rely on

- `media-library.js` draws `h2.media-library__group[data-bucket]` per bucket, and only when the sort is by
  upload date; it reverses the ladder for an ascending sort.
- `media-handoff.js` draws `h3.media-transfers__group[data-bucket]` per bucket, and not at all when the
  dialog was opened from the transfer rail.
- `tests/e2e/test_media_age_buckets.py` calls the rule with an explicit `nowMs` to pin every edge.

## Prohibited

- A caller computing a bucket itself — the point of the contract is that there is one rule.
- A caller adding, renaming or reordering a ladder entry.
- Storing a bucket key anywhere: it is derived per draw and never written to the companion or the page's
  storage.
