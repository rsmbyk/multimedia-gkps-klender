# Spec: OBS-BIBLE — OBS Bible dock and source

| Field | Value |
|-------|--------|
| **Spec ID** | `OBS-BIBLE` |
| **Area** | `bible` |
| **Status** | `as-built` |
| **Folder** | `specs/bible/obs-bible-live/` |

## Problem / goal

Operators browse bible versions/books/chapters/verses in an OBS dock, keep a
short history, and project the active passage on an OBS source via
BroadcastChannel.

## User stories

- **OBS-BIBLE-US1:** As an OBS operator, I want to browse and display a verse,
  so that scripture can be projected live.
- **OBS-BIBLE-US2:** As an operator, I want history of recent passages, so that
  I can jump back during service.
- **OBS-BIBLE-US3:** As a projectionist, I want the source to follow passage and
  status posts, so that the screen stays in sync.

## Acceptance criteria (EARS)

### Surfaces and channels

- **OBS-BIBLE-AC1:** THE system SHALL serve `/obs/bible/dock` and
  `/obs/bible/source`.
- **OBS-BIBLE-AC2:** THE bible app SHALL use BroadcastChannels
  `OBS-BIBLE-PASSAGE`, `OBS-BIBLE-STATUS`, and `OBS-BIBLE-CONTROL`.
- **OBS-BIBLE-AC3:** WHEN the dock gains/loses focus, THE focus indicator SHALL
  use the bible colour class (`blue`).

### Browse and display

- **OBS-BIBLE-AC4:** Bible tab version/book/chapter dropdowns SHALL persist in
  localStorage; Open SHALL load browse for that translation/chapter.
- **OBS-BIBLE-AC5:** WHEN a verse is clicked in Browse, THE system SHALL
  `display(...)` and switch to the Display tab; chapter prev/next SHALL disable
  at 1 / `number_of_chapters`.
- **OBS-BIBLE-AC6:** WHEN Display version abbreviation changes, THE system
  SHALL refetch translation + verses for the same book/chapter and re-display;
  IF the fetch fails, THEN restore the previous selection.
- **OBS-BIBLE-AC7:** Version/book icons SHALL use a flag when `lang.id === 2`,
  else a language icon (as-built language cue).

### History

- **OBS-BIBLE-AC8:** WHEN `display()` runs, THE manager SHALL upsert history by
  translation+chapter+verse, cap at 25, save `OBS_BIBLE_HISTORY`, and expose
  newest-first.
- **OBS-BIBLE-AC9:** WHEN a history item is clicked, THE system SHALL restore
  display + browse and navigate to Display.

### Hotkeys, BC, source

- **OBS-BIBLE-AC10:** WHILE `tab-display`, Left/Right/Space SHALL map to
  prev/next verse / status toggle.
- **OBS-BIBLE-AC11:** WHEN activate, THE dock SHALL post status true + passage;
  WHEN inactive, status false.
- **OBS-BIBLE-AC12:** WHEN verse number changes, THE dock SHALL always
  `postPassage` (not gated on active — unlike songs/tatib).
- **OBS-BIBLE-AC13:** Prev SHALL disable at verse 1; next at last verse.
- **OBS-BIBLE-AC14:** WHEN the source loads, it SHALL post inactive status with
  `source: 'source'`.
- **OBS-BIBLE-AC15:** WHEN passage/status arrive, THE source SHALL update
  fields and fade the segment accordingly.
- **OBS-BIBLE-AC16:** Control messages `left`/`right`/`space`/`rebroadcast`
  SHALL drive dock display controls (verse-scoped, no song-style cascade).
- **OBS-BIBLE-AC17:** Shared settings SHALL use prefix `OBS_BIBLE`.

## Out of scope

- Bible REST filter details (`API-BIBLE`).
- Project combined view (`OBS-PROJECT`).
- Bible web content admin (not built).

## Constraints

- Related: `API-BIBLE`, `OBS-PROJECT`, `API-ACCESS`.

## Notes

- Vitest: `bible/common/bc.test.js`, `display/hotkeys.test.js`,
  `history-storage.test.js`.
