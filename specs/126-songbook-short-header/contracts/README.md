# Contracts: A song page cites its songbook by its short name

**Spec**: `specs/126-songbook-short-header/spec.md`

`none — the slice exposes no request, response, event, function or payload contract.` It changes the text of
one paragraph the page already renders, and the same text in the browser renderer that mirrors that page.

## Internal surfaces the change touches (not contracts)

| Surface | Kind | Constraint |
| --- | --- | --- |
| `SongDetailView` context key `read_eyebrow` | template variable | stays a string; empty only when the route has no citation |
| `SongDetailView` context key `page_title` | template variable | `<citation> — GKPS Klender` |
| `static/web/offline-render.js` `songPage()` | browser function | writes the same string into `#readEyebrow` and `document.title` |

Neither the saved-library payload (`GKPSOffline.sync()`'s JSON) nor any IndexedDB record changes shape: the
renderer already receives each songbook's `name`, `short_name` and `is_hymn_book`.
