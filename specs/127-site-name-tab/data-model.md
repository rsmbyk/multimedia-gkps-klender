# Data model: The tab names the site, and the index's tab stops at the name

**Spec**: `specs/127-site-name-tab/spec.md`

`n/a — no entity, field, relationship, constraint, migration or payload changes.` Every title is composed
at render time; nothing is persisted.

## Values read (unchanged)

| Value | Source | Used by |
| --- | --- | --- |
| Site name | the literal `Multimedia GKPS Klender` | every title |
| Book translation name, chapter | `bible.BookTranslation.translation`, the route's chapter | a Bible page's leading text |
| Song citation | `songs.Book` + `songs.Song` (spec 126's rule) | a song page's leading text |
| Service name | `tatib.TataIbadah.name` | a Tata Ibadah page's leading text |
| Canonical search query | the search grammar's canonical form | the results page's leading text |

## Derived values

| Route | Title |
| --- | --- |
| `/`, `/home/`, `/search` (no query) | `Multimedia GKPS Klender` |
| `/bible/<book>/<chapter>/` | `<book name> <chapter> — Multimedia GKPS Klender` |
| `/bible/` | `Alkitab — Multimedia GKPS Klender` |
| `/songs/` | `Kidung — Multimedia GKPS Klender` |
| `/songs/<song>/` | `<citation> — Multimedia GKPS Klender` |
| `/tatib/`, `/tatib/<service>/` | `Tata Ibadah` / `<service name>` ` — Multimedia GKPS Klender` |
| `/search?q=…` | `Results for “<canonical>” — Multimedia GKPS Klender` |
| `/media-library/` | `Media Library — Multimedia GKPS Klender` |

Nothing is persisted: the value is computed per request by the view and per render by the browser.
