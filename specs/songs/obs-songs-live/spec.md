# Spec: OBS-SONGS — OBS Songs dock and source

| Field | Value |
|-------|--------|
| **Spec ID** | `OBS-SONGS` |
| **Area** | `songs` |
| **Status** | `as-built` |
| **Folder** | `specs/songs/obs-songs-live/` |

## Problem / goal

Operators control live song projection from an OBS browser dock and show lyrics
on an OBS browser source, synchronized via BroadcastChannel, with bookmarks,
search, paste, display modes, and hotkeys.

## User stories

- **OBS-SONGS-US1:** As an OBS operator, I want songbooks, search, bookmarks,
  and display tabs, so that I can prepare and project lyrics during service.
- **OBS-SONGS-US2:** As a projectionist, I want the source to follow dock
  status and song-info, so that the congregation sees the active lyric chunk.
- **OBS-SONGS-US3:** As an operator, I want display-tab hotkeys and paste, so
  that I can advance content without leaving the keyboard.

## Acceptance criteria (EARS)

### Surfaces and channels

- **OBS-SONGS-AC1:** THE system SHALL serve `/obs/songs/dock` and
  `/obs/songs/source`.
- **OBS-SONGS-AC2:** THE songs app SHALL use BroadcastChannels
  `OBS-SONGS-SONG-INFO` (content), `OBS-SONGS-STATUS` (status), and
  `OBS-SONGS-CONTROL` (control).
- **OBS-SONGS-AC3:** WHEN the dock window gains/loses focus, THE focus
  indicator SHALL use the songs colour class (`green`).

### Display / status / content

- **OBS-SONGS-AC4:** WHEN status becomes active, THE dock SHALL post
  `status: true, source: 'dock'` and song-info; WHEN inactive, post
  `status: false`.
- **OBS-SONGS-AC5:** WHEN lyric index changes WHILE status is active (or on
  activate with force), THE dock SHALL post song-info
  `{ bookNumber, verseNumber, title, is_untitled, lyric }`; IF on last chunk
  (`--- END ---`), `lyric` SHALL be `''`.
- **OBS-SONGS-AC6:** IF the operator tries to activate WHILE on the last lyric
  chunk, THEN activate SHALL be refused.
- **OBS-SONGS-AC7:** WHEN the last lyric of a non-last verse is reached, THE UI
  SHALL offer Last Lyric (advance verse + activate); WHEN last lyric of last
  verse of a non-last song, offer Last Verse (next song + activate); and status
  SHALL go inactive at those boundaries as implemented.
- **OBS-SONGS-AC8:** WHEN `numberOfLines` changes (localStorage
  `OBS_SONGS_DOCK_SETTINGS_NUMBER_OF_LINES`, default 2), THE dock SHALL regroup
  verse lines into chunks of N and append `--- END ---`.
- **OBS-SONGS-AC9:** WHEN display mode changes
  (`OBS_SONGS_DOCK_SETTINGS_DISPLAY_MODE`, default segment), THE source SHALL
  show the matching chrome among segment / box / outline.

### Hotkeys and control

- **OBS-SONGS-AC10:** WHILE active tab is `tab-display`, WHEN the user presses
  Left / Right / Ctrl+Left|Right / Shift+Left|Right / Space, THE system SHALL
  map to prev/next lyric, verse, song, or status (Right prefers Last Verse →
  Last Lyric → Next Lyric as applicable).
- **OBS-SONGS-AC11:** WHEN control subject receives `left`/`right`/`space`/
  `rebroadcast`, THE dock SHALL click the matching display controls (or
  rebroadcast = inactive then active).
- **OBS-SONGS-AC12:** WHEN control `left` arrives, THE dock SHALL cascade:
  prev lyric → else prev verse → else prev song.

### Source

- **OBS-SONGS-AC13:** WHEN the source loads, THE source SHALL post inactive
  status with `source: 'source'`.
- **OBS-SONGS-AC14:** WHEN song-info arrives, THE source SHALL update
  book/verse/title/lyric and fade lyric; IF `bookNumber === null` hide book
  info; IF `is_untitled` hide song-info header.
- **OBS-SONGS-AC15:** WHEN status is true/false, THE source SHALL fade in/out
  the active display-mode element.

### SongBooks, search, paste, settings

- **OBS-SONGS-AC16:** SongBooks dropdowns SHALL persist selection in
  localStorage; Open SHALL open song-detail.
- **OBS-SONGS-AC17:** WHEN search submit has `q` length ≥ 3, THE dock SHALL
  GET `/api/search/songs?q=` and support Load More pagination (`API-SEARCH`).
- **OBS-SONGS-AC18:** WHEN paste provides a non-empty lyric, THE dock SHALL
  activate a single untitled `[NO_TITLE]` item; IF current single item is
  `[NO_TITLE]`, reopen SHALL prefill lyric.
- **OBS-SONGS-AC19:** Settings SHALL expose paste, shared settings modal
  (`OBS_SONGS` prefix), numberOfLines, and displayMode.

### Bookmarks

- **OBS-SONGS-AC20:** Bookmarks tab behavior SHALL follow `SONGS-BM-AC13`–
  `AC16` (activate, idle, reactivate, reorder).

## Out of scope

- Combined project projection (`OBS-PROJECT`).
- Bookmark uniqueness API rules (`SONGS-BM` API section).

## Constraints

- Shared helpers: `multimedia/obs/static/obs/common/`.
- Related: `API-SONGS`, `API-SEARCH`, `SONGS-BM`, `OBS-PROJECT`, `API-ACCESS`.

## Notes

- Vitest: `songs/common/bc.test.js`, `display/hotkeys.test.js`,
  `bookmark-storage.test.js`, `common/settings-storage.test.js`.
