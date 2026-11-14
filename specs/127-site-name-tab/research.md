# Research: The tab names the site, and the index's tab stops at the name

**Spec**: `specs/127-site-name-tab/spec.md`
**Date**: 2026-10-24

## D001 — Where the document title is actually produced

**Decision**: treat the title as three producers that must agree, and change all three.

**Finding**: `grep -rn "GKPS Klender" multimedia/ static/` shows the reading surface's title written in
three places:

| Producer | Where | Count |
| --- | --- | --- |
| Server view context `page_title` | `multimedia/web/reading/views.py` | 12 strings |
| Server template defaults (`base.html` and the six `{% block title %}` defaults) | `multimedia/web/templates/reading/` | 7 strings |
| Browser: saved renderer (`common()`, `homePage()`, `listPage()`, the search results document) | `static/web/offline-render.js` | 4 strings |
| Browser: in-place update after a Bible edition switch | `static/web/reading.js` (`syncVisibleBibleTitle`) | 1 string |

**Rationale**: the saved renderer and the in-place update both overwrite `document.title` after the server
page has painted, so changing only the server would leave a tab that renames itself mid-session — the
mismatch class spec 122 closed for headings and labels.

**Alternatives rejected**: change only `views.py` — the saved page and the edition-switch path would keep
the old name.

## D002 — Literal strings, not a new `SITE_NAME` constant

**Decision**: replace the token in each literal; add no shared constant or context processor.

**Rationale**: the title strings are assembled at nineteen sites across Python, Django templates and two
browser files, and the templates would still need the value threaded in (a context processor, or a settings
import in each template). A constant would touch the same lines and add indirection to a repo whose tests
pin full title strings by design — the tests, not a constant, are what keep the name one thing.

**Alternatives rejected**: a `SITE_NAME` setting plus a context processor — more surface than the slice,
with no caller that wants a variable.

## D003 — The index's title stops at the site name

**Decision**: `/`, `/home/` and `/search` with no query read exactly `Multimedia GKPS Klender`; every other
route keeps its leading text and appends ` — Multimedia GKPS Klender`.

**Rationale**: the trailing tagline (`Search Alkitab, Kidung, and Tata Ibadah`) is what the page's own
search field already says, and in the request's vertical tab strip it is truncated to `Sea…` anyway. The
owner confirmed this reading of "remove any trailing when opening index" in the request session.

**Alternatives rejected**: keeping the tagline — the tab would spend its width on words the page repeats.

## D004 — The URL is not a surface of this change

**Finding**: an HTTP request for a site root always carries the path `/`; the browser's display of it is
chrome, not page content. The request's screenshot shows the address as `localhost:63404` with no trailing
slash, and no route in `multimedia/web/urls.py` redirects `/` anywhere.

**Decision**: no URL or redirect change. The "trailing" in the request is the tagline, confirmed by the
owner.

## D005 — Visible and assistive text keeps the congregation name

**Decision**: headings, placeholders, `alt` text and `aria-label`s keep `GKPS Klender`.

**Rationale**: the request names the tab. `alt="GKPS Klender"` on the logo names the mark, and
`aria-label="GKPS Klender — home"` names the destination; renaming those would announce a product name to
screen readers where the congregation's name belongs. The templates' remaining `GKPS Klender` occurrences
were read one by one and left as found.

## D006 — No migration or data change

**Finding**: nothing about the title is stored. Every string is composed at render time, server or browser.

**Decision**: no model, migration, fixture or saved-payload change; the saved library's JSON is untouched.
