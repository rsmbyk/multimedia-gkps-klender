# Glossary and naming

Shared vocabulary for this project. Use these terms consistently in code, docs, commits, and
conversation. Canonical terms are in **bold**; *also called* lists legacy or colloquial aliases
still found in the codebase.

## Naming rules for new work

- Write identifiers, comments, docs, and commits in **English**.
- Use the **canonical** term below. Do not invent new synonyms for an existing concept.
- Keep existing app/model names (`TataIbadah`, `tatib`, `bookmarks`, …) for data compatibility;
  new concepts use the canonical English term.
- Django: models singular `PascalCase`; apps/modules lowercase; URL paths `kebab-case`.
- Retired: per-app version counters (`b`, `s`, `t`, `p`, `dj`) and strings like `v0.4.s30`.
  There is one product version (see [`docs/VERSIONING`](ARCHITECTURE.md)).

## Domain

| Canonical | Also called | Definition | Lives in |
| --- | --- | --- | --- |
| **Bible** | — | Scripture content: languages, versions, books, translations, verses. | `multimedia/bible`, `/api/bible/`, `/obs/bible/` |
| **Language** | — | A natural language (e.g. Indonesian, Simalungun). | `bible.Language` |
| **Version** | Bible version | A named translation/edition of the Bible in a language. | `bible.Version` |
| **Book** (Bible) | — | A book of the Bible (name, testament, chapter count). | `bible.Book` |
| **Book translation** | — | A `Book` as it appears in a specific `Version`. | `bible.BookTranslation` |
| **Verse** (Bible) | — | One verse: chapter, verse number, optional title, text. | `bible.Verse` |
| **Passage** | — | The Bible text currently being projected (book, chapter, verse, text). | OBS `passageSubject` |
| **Songbook** | — | A collection of songs: a **Hymn book** when its songs carry numbers, an ordinary songbook when they do not. | `songs.Book` |
| **Hymn book** | SongBook | A songbook whose songs carry numbers (`is_hymn_book`, e.g. NKB). | `songs.Book` (`is_hymn_book`) |
| **Song** | — | A numbered song in a hymn book: number, sub-number, title, key. | `songs.Song` |
| **Key** | — | The musical key of a song. | `songs.Key` |
| **Lyric verse** | Song verse | A numbered lyric stanza of a song. | `songs.Verse` |
| **Setlist** | Bookmark | An ordered selection of songs (and verse ranges) for a service. | `bookmarks.SongBookmark`, `SongBookmarkItem` |
| **Service order** | Tata Ibadah, Tatib | The ordered order-of-worship for a service. | `tatib.TataIbadah` |
| **Service item** | TataIbadahItem | One ordered element of a service order. Types: **Text item**, **Section break** (End of Section / EOS). | `tatib.TataIbadahItem` |

## OBS surfaces

| Canonical | Also called | Definition |
| --- | --- | --- |
| **Dock** | — | The operator control panel opened inside OBS as a browser dock. |
| **Source** | OBS source, browser source | A page captured by OBS as a browser source; it displays text. |
| **Projection** | Project | The full-screen text display surface (`/obs/project/source`) for song lyrics, service items, and Bible passages. |
| **Panel** | Segment | A UI container/region within a page. Prefer **panel** in new code; `segment` survives in legacy CSS. |
| **Unit** | — | What a plain `Home` / `End` acts on: the live bait when the live entry is a song, the live entry otherwise. Never the whole service — `Ctrl`/`⌘` with the same key is the chord that reaches that. |

## OBS messaging

| Canonical | Definition |
| --- | --- |
| **Broadcast channel** | A named `BroadcastChannel` passing messages between OBS windows (e.g. `OBS-SONGS-SONG-INFO`). |
| **Info message** | Broadcast of content to display (song info, service item, passage). |
| **Status message** | Broadcast that an app is active/inactive and which surface set it. |
| **Control message** | Broadcast of a navigation command (`left`, `right`, `space`, `rebroadcast`). |
| **Subject** | An RxJS wrapper that both holds and streams messages (see `static/helpers/rx.js`). |

## Web

| Canonical | Also called | Definition |
| --- | --- | --- |
| **Public site** | — | The public reading experience at `/` and `/songs/…` (later `/bible/…`). |
| **Editor** | Web admin UI, `web` | The content-management surface at `/editor/…`. |
| **Design language** | Design system | This project's own tokens and components, drifting off Semantic/Fomantic UI; palette drawn from the GKPS logo. |
| **Maintenance page** | — | The notice served at `/` while maintenance mode is on. | `reading/maintenance.html` |
| **Retired address** | Legacy route | An address a release stops serving, answering one 302 to its live successor for one release; the next release decides between a 301 and reuse. | `multimedia/retirement.py` |
| **Archive namespace** | — | `/archive/<old path>`: the temporary namespace that answers a retired address's successor in one hop, removed the release after it was added. | `multimedia/retirement.py` |
