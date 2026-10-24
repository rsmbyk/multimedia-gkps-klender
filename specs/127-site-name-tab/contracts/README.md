# Contracts: The tab names the site, and the index's tab stops at the name

**Spec**: `specs/127-site-name-tab/spec.md`

`none — the slice exposes no request, response, event, function or payload contract.` It changes the text
of the `<title>` element that every reading page already renders, and the same text in the browser
functions that mirror it.

## Internal surfaces the change touches (not contracts)

| Surface | Kind | Constraint |
| --- | --- | --- |
| View context key `page_title` | template variable | a string; the index's is the site name alone, every other is `<leading> — Multimedia GKPS Klender` |
| `base.html`'s `{% block title %}` default | template | the site name alone — the value a page with no `page_title` falls back to |
| `static/web/offline-render.js` `common()`, `homePage()`, `listPage()`, the search results document | browser functions | write the same two shapes into `document.title` |
| `static/web/reading.js` `syncVisibleBibleTitle()` | browser function | the same suffix, after an in-place edition switch |

Neither the saved-library payload (`GKPSOffline.sync()`'s JSON) nor any IndexedDB record changes shape: the
renderer already receives every value the title is built from.
