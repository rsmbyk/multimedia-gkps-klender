# Spec: Sidebar editors for Kidung and Tata Ibadah

- **ID:** 005
- **Status:** Accepted
- **Item:** ITEM-006
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

Let the people preparing a service fix and extend the corpus where they are reading it: add a
songbook, add a song to the songbook they have open, add a Tata Ibadah, and edit any of those
rows — from the same three sidebars that already list them, without leaving the shell.

## Scope

### In scope

- A full-width, accent-coloured **add** button directly below the filter field in three
  sidebars: the songbook panel (Kidung), the song list (Kidung's third level), and the Tata
  Ibadah panel. Each opens a modal that creates the corresponding record — a songbook, a song
  in the currently open songbook, a Tata Ibadah service.
- An **edit** control on each row of those three lists, revealed on hover and on keyboard
  focus, opening the same modal prefilled.
- Server-rendered forms with the models' own rules; validation errors shown in the modal;
  CSRF enforced on every write.
- An optional login gate behind one setting, so the corpus can be locked to signed-in staff
  later without redesigning the controls.

### Out of scope

- Deleting or archiving anything; no bulk import or export.
- Bible books/verses (Alkitab is not editable here).
- Tata Ibadah **items** — the contents rows stay quicklinks; a service's sections are still
  edited through the admin.
- A permissions model of its own (only the one-setting hook below), revision history, drafts,
  or an approval flow.
- OBS, the public API, bookmarks, the maintenance page.

## Domain rules

- **Hymn songbooks are read-only, and so are their songs.** A row for a songbook with
  `is_hymn_book` true — and any song whose `book` is one — gets no edit control at all. The
  rule is data-driven: it reads the flag, it does not keep a list of names.
- **The add button follows the sidebar it sits in.** The song list's add button creates a song
  in the songbook currently open in that sidebar; with no songbook chosen yet it is disabled
  and says so. The songbook panel's button creates a songbook, the Tata Ibadah panel's creates
  a service.
- **Forms mirror the model's own constraints** rather than inventing looser ones: `Book` name
  unique per language and `short_name` unique (the existing validator); `Song` unique on
  `(book, number, sub_number)`, with `number` **required for a hymn book** (a hymn's identity
  is its number) and optional otherwise; `TataIbadah` name and optional date.
- **Songbook fields:** name, short name, language, hymn flag. The hymn flag is editable, so a
  new hymn book can be created — and setting it locks that book's songs against editing, which
  is the intended consequence, reversible by clearing the flag.
- **Tata Ibadah fields:** name, date, active. An empty date means a *recurring template*, not
  an undated service, and the form says so.
- **A service is visible once it has a public section.** The public lists and search only show
  active services with at least one `TEXT` item, so the create form carries an optional first
  section (title + text) — without it the new service would be created but invisible, which
  reads as a failed save.
- **Writing follows the shell's existing rules.** Saving does not change the URL, does not
  reload, does not move the reading stage or the sidebar scroll, and leaves focus on a
  sensible control (the saved row's edit control, or the add button).
- **Writes are server-authoritative.** The endpoints validate and reject invalid input even
  when the modal is bypassed; a hand-crafted POST cannot store a record the forms would
  refuse.
- **The no-JS floor is unchanged.** Without JavaScript the reading experience is exactly what
  it is today; the editor controls are inert enhancements (they are rendered only in a state
  that does nothing without JS), and the endpoints still enforce their rules.

### Accepted risk (owner decision, 2026-10-03)

The owner chose that **anyone may write** through these forms, with no login: the corpus
becomes publicly editable. It is recorded here deliberately. The mitigation is a single
setting — `SIDEBAR_EDITORS_REQUIRE_LOGIN` — which, when true, hides every control from
anonymous visitors and answers their writes with 403, so the gate can be switched on in
production without touching the UI code. Recommended before the site is exposed beyond the
team; the spec pins it as the first thing to revisit.

## Acceptance scenarios

### Scenario: Add a songbook

- **Given** I am on any reading page
- **When** I open the Kidung sidebar and activate the add button below its filter
- **Then** a modal opens with the songbook form (name, short name, language, hymn flag)
- **And** saving it adds the row to the songbook panel, selected, with the reading stage
  untouched and no reload

### Scenario: Add a song to the open songbook

- **Given** a songbook is open in the Kidung sidebar
- **When** I activate the add button below the song list's filter and save a song
- **Then** the song appears in that list in its place
- **And** in a hymn songbook the form requires a number, and the saved row shows its citation
- **And** with no songbook open the button is disabled and explains why

### Scenario: Add a Tata Ibadah

- **Given** the Tata Ibadah sidebar is open
- **When** I add a service with a date, and separately one without
- **Then** the dated service joins its year+month group and the undated one joins *Templates*
- **And** a service saved without any section is explained in the form before it is saved

### Scenario: Edit a row

- **Given** a non-hymn songbook, one of its songs, or a Tata Ibadah service
- **When** I hover its row (or reach it with the keyboard) and activate the edit control
- **Then** the modal opens prefilled with that record, and saving updates the row in place
- **And** if the reading stage shows that record, its content updates without losing the
  place I was reading

### Scenario: Hymn songbooks and their songs offer no edit control

- **Given** a hymn songbook (or a song inside one)
- **When** I hover its row, or tab through the list
- **Then** no edit control exists — in the markup, not merely hidden — while its neighbours
  in a non-hymn list still have one

### Scenario: Invalid input writes nothing

- **Given** the modal for any of the three records
- **When** I submit a duplicate short name, a duplicate song number, or a hymn song without a
  number
- **Then** the modal shows the error beside the field, keeps what I typed, and stores nothing
- **And** a POST without a valid CSRF token is rejected

### Scenario: The optional login gate

- **Given** `SIDEBAR_EDITORS_REQUIRE_LOGIN` is true
- **When** an anonymous visitor loads a reading page
- **Then** no add or edit control is rendered, and their create/update requests are refused
- **And** a signed-in staff user sees and can use the controls as above

## Traceability

- Domain/app tests: `multimedia/web/tests.py` — `EditorViewTests` (create/update for each
  record, the constraint matrix, CSRF, POST-only, the login hook, hymn exclusion in the
  rendered shell)
- E2E: `tests/e2e/test_editor.py` — `EditorE2ETests` (the three add flows, both edit flows,
  the hover reveal with its keyboard reach, the error path, and the stage surviving a save)
- Implementation: `multimedia/web/reading/editors.py` (forms + accept/save helpers),
  `multimedia/web/reading/views.py` (`editor_form`, `editor_save`),
  `multimedia/web/reading/context_processors.py` (`editor_enabled`),
  `multimedia/web/urls.py` (four `/editor/...` routes),
  `multimedia/web/templates/reading/{_editor_modal,_editor_form}.html` plus the add buttons
  and row controls in `base.html`, `_songbooks_panel.html`, `_song_list.html`,
  `_tatib_panel.html`; `static/web/editors.js`; the `refresh` kind in
  `static/web/reading.js`; `static/styles/design/components.css`
