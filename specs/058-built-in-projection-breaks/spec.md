# Spec 058: Built-in blank after each entry and each song verse

- **ID:** 058
- **Status:** Accepted
- **Item:** ITEM-060
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

Every content entry on the service projector ends with a blank screen, and every
verse of a song ends with one too. That blank is part of projection. It is not a
**Section break**, so it does not appear in the service order and cannot be
moved or deleted.

## Scope

### In scope

- One trailing blank screen after each text entry, single-screen text entry,
  scripture entry, and legacy text row.
- One blank screen after each verse of a song entry, including the last verse.
- Stored section breaks and legacy end-of-section rows remain a single blank
  screen with no additional built-in blank.

### Out of scope

- Persisting the blank as a `ServiceEntry`.
- Editor rows, reorder, and delete.
- Blanks between lyric lines of one verse, or between two-line screens of one
  text.
- Blanks between individual scripture verses.
- The OBS dock.

## Domain rules

- **The blank is not an entry.** The service order stores the same rows as
  before. Reorder and delete never see the built-in blank.
- **One blank after content.** After the last content screen of a text,
  single-screen text, scripture, or legacy text row, the next projector screen
  is blank.
- **One blank after each song verse.** A song's verses project in stored verse
  order. Each verse keeps today's two-line lyric screens, then a blank. The
  blank after the last verse is the entry's only trailing blank.
- **A stored break is only itself.** A section break or legacy end-of-section
  contributes its one blank and does not gain another.
- **Adjacent blanks stay.** A content entry followed by a stored section break
  shows the built-in blank and then the break. They are not merged.

## Acceptance scenarios

### Scenario: A text entry is followed by a blank that is not a row

- **Given** a service whose only entry is a text item with two lines
- **When** the projector builds its screens
- **Then** the screens are that text, then one blank
- **And** the service order still has one entry

### Scenario: The blank cannot be moved or deleted

- **Given** a service with a text entry
- **When** the editor lists the order
- **Then** there is no blank row after the text, and nothing extra to reorder or delete

### Scenario: Each song verse ends on a blank

- **Given** a song entry whose selected verses are 1 and 2, each with lyrics
- **When** the projector builds its screens
- **Then** verse 1's lyric screens are followed by one blank, then verse 2's lyric screens, then one blank
- **And** there is not a second blank after verse 2

### Scenario: A section break stays a single blank

- **Given** a text entry followed by a section break
- **When** the projector builds its screens
- **Then** the screens are the text, one built-in blank, then the section break's one blank
- **And** the section break is still the only break entry in the order

### Scenario: A passage gets one blank after the last verse

- **Given** a scripture entry covering two verses
- **When** the projector builds its screens
- **Then** the two verse screens are consecutive, and one blank follows the second verse

## Traceability

- Domain/app tests: `multimedia/web/tests.py` (`ServiceProjectorTests`).
- E2E: `tests/e2e/test_projector.py`.
- Implementation: `multimedia/web/reading/views.py` (`_projector_screens`, `_song_screens`).
