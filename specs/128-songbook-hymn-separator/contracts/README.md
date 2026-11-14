# Contracts: Hymn songbooks above a single separator, the rest A–Z

**Spec**: `specs/128-songbook-hymn-separator/spec.md`

## Interfaces exposed by this slice

`none — the slice changes server-rendered markup, one template context key, and a saved-render builder. No
HTTP endpoint, API payload, model field or migration is added or changed, so no external consumer has an
interface to contract against.`

## Not exposed

- The template context key `songbook_groups` is internal to the three Kidung views and
  `_songbooks_panel.html`; no other template reads it.
- `songbookGroups()` / `songbooksPanel()` are internal helpers of `offline-render.js`, alongside
  `biblePanel()` and `servicePanel()`.
