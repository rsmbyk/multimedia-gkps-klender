# Spec: OBS-PROJECT — Combined OBS project projection

| Field | Value |
|-------|--------|
| **Spec ID** | `OBS-PROJECT` |
| **Area** | `project` |
| **Status** | `as-built` |
| **Folder** | `specs/project/obs-project-projection/` |

## Problem / goal

Operators need one fullscreen OBS source that listens to songs, bible, and tatib
BroadcastChannels, shows the active app’s content with auto-fit fonts, and can
hand control between apps with hotkeys.

## User stories

- **OBS-PROJECT-US1:** As a projectionist, I want one project source for all
  three apps, so that I do not switch OBS scenes for every content type.
- **OBS-PROJECT-US2:** As an operator, I want keys 1/2/3 to pick songs/bible/
  tatib and rebroadcast, so that I can recover or switch controlling app quickly.
- **OBS-PROJECT-US3:** As an operator, I want title/content/background colours
  configurable, so that projection matches the service look.

## Acceptance criteria (EARS)

### Surfaces

- **OBS-PROJECT-AC1:** THE system SHALL serve `/obs/project/source` and
  `/obs/project/settings`.

### Multi-channel listen

- **OBS-PROJECT-AC2:** WHEN song-info, tatib-item, or bible passage arrives, THE
  project SHALL format content, set title/text, auto-fit fonts, and fade text.
- **OBS-PROJECT-AC3:** Songs formatting SHALL use empty title + lyric only;
  tatib SHALL use title+text; bible SHALL use `"{book} {ch} : {v}"` plus
  optional passage title line, then verse text.
- **OBS-PROJECT-AC4:** WHEN any app status becomes true with
  `source !== 'source'`, THE project SHALL fade in and force the other two
  apps’ status to false with `source: 'source'` and `skipUpdateSubject=true`.
- **OBS-PROJECT-AC5:** WHEN status becomes false with `source !== 'source'`
  WHILE the project is visible, THE project SHALL fade out.
- **OBS-PROJECT-AC6:** WHEN the project source boots, it SHALL post inactive
  status on all three apps with `source: 'source'`.

### Hotkeys

- **OBS-PROJECT-AC7:** WHEN status updates with `source !== 'source'`, THE
  project SHALL remember that app as `lastActiveBC`.
- **OBS-PROJECT-AC8:** Left/Right/Space SHALL `postControlMessage` on
  `lastActiveBC` (no-op if none).
- **OBS-PROJECT-AC9:** Key `1` SHALL select songs and rebroadcast; `2` bible;
  `3` tatib (set last active then rebroadcast).

### Auto-fit and colours

- **OBS-PROJECT-AC10:** WHEN content updates, title font SHALL shrink from 50
  until width fits `window−72`; text from 100 until height fits remaining
  viewport−72 (minimum size 1).
- **OBS-PROJECT-AC11:** Colour settings SHALL use localStorage keys
  `SETTINGS_PROJECT_TITLE_TEXT_COLOUR` (default `ffe951`),
  `SETTINGS_PROJECT_CONTENT_TEXT_COLOUR` (`ffffff`),
  `SETTINGS_PROJECT_BACKGROUND_COLOUR` (`323233`), with `storage` events and
  onload seeding subjects; the settings page SHALL apply colours to the DOM.

## Out of scope

- Per-app dock UX (`OBS-SONGS`, `OBS-BIBLE`, `OBS-TATIB`).
- Changing BroadcastChannel names owned by those apps.

## Constraints

- Related: `OBS-SONGS`, `OBS-BIBLE`, `OBS-TATIB`.
- JS: `multimedia/obs/static/obs/project/`.

## Notes

- Vitest: `project/source/format.test.js`,
  `project/common/settings-storage.test.js`.
- Controls 1/2/3 + mutual mute lack Vitest coverage today.
