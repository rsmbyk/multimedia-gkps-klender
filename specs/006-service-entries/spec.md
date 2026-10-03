# Spec 006: Service entries — one Tata Ibadah holds texts, scriptures and songs

- **Status:** Accepted (owner, 2026-10-03) — needs the owner's Accept (SDD gate; no implementation before that)
- **Spec:** 006-service-entries
- **Item:** [`backlog/items/ITEM-007-service-entries.md`](../../backlog/items/ITEM-007-service-entries.md)
- **Owner:** GKPS Klender
- **Bump:** minor (0.9.0 → 0.10.0 when it ships)
- **Depends on:** 005 (accepted). Nothing here changes spec 004/005 behaviour.

## Intent

A service today is prepared as three separate lists — scriptures, songs, and the liturgy — each
living in its own OBS dock (Bible, Songs, Tata Ibadah). The operator prepares all three, then
switches which dock is talking to the display, dock by dock, during the service. The kataibadah
is the one that describes the service's running order, so it should be able to *hold* all three
kinds of thing: a passage, a song, a plain text, and the section breaks between them.

The win is one surface driving a whole service, with the running order matching the printed
order of worship.

**The display side is built fresh, beside the old one.** The current projector and overlay are
production and stay exactly as they are; this spec adds *my own* screen projector and *my own*
OBS overlay for the new system, as new pages with their own scripts and their own sync channel.
They follow the same display *rules* the operator already relies on — the two-line split, the
projector resizing to fit, the overlay growing to fit, the blank line as the pause — because
those are habits, not implementation details. The old pages keep serving the old data on the
old channel, and nothing about them changes.

## Compatibility promise (the part that must not break)

This is an addition to the production app, not a replacement of it.

1. **The current OBS pages are not touched.** `/obs/project/source`, `/obs/<bible|songs|tatib>/
   source`, `/obs/<bible|songs|tatib>/dock` and `/obs/project/settings` keep their templates,
   scripts, endpoints and behaviour — not one line of this spec edits them. The new system gets
   its own pages and its own files, and its own sync channel so an old dock and a new display
   can never speak to each other by accident.
2. **The existing API keeps working.** Every current endpoint (including
   `/api/tatib/items/` and its `reorder` action) answers as it does today, for the current data.
   The old dock can keep driving services through it.
3. **The existing model is left alone.** `tatib.TataIbadahItem` and its rows stay as they are.
   The new capability is a new model beside it, so no existing reading path can be affected by
   it. Migrating the old rows into the new model is a separate, later, owner-triggered slice.
4. **The display contract keeps its shape.** Whatever an entry is, what the new projector is
   given is a title and a body — the same pair of strings the current Tata Ibadah source renders.
   My projector owns the font sizing, my overlay owns the container growth, and the split into
   two lines lives on the display side, exactly as it does today.

## Scope

### In scope

- A new **service entry** model in the `tatib` app: one ordered element of a service order that
  is one of **text**, **scripture**, **song**, or **section break** (end of section). It carries
  the fields its kind needs, and an order number within its Tata Ibadah.
- Managing entries **in the content pane** of the reading app (the page that shows a Tata
  Ibadah's items today), not in a sidebar.
- Per-entry add controls that open one modal each: scripture, song, text, section break.
- The scripture modal: book, chapter, start verse, optional end verse — each a dropdown, from
  the data. Changing the book or the chapter resets chapter and verses to 1.
- The song modal: a searchable song dropdown grouped by songbook, then a verse checklist.
  All verses are checked by default; unchecking excludes a verse. The control's label reads
  which verses are shown ("all verses" when everything is checked).
- The text and section-break modals: the current item's fields.
- **Reorder by dragging**, with a reorder mode that holds changes until saved or discarded,
  adds disabled, and a confirmation before leaving with unsaved changes.
- **A new screen projector and a new OBS overlay** for this system, as new pages: they render
  every kind of entry, split a body into two lines, size the font to fit (projector) or grow the
  box to fit (overlay), and treat a blank line as the operator's pause. Own templates, own
  scripts, own sync channel.
- **A project button** on a Tata Ibadah in the reading app that opens the new projector in a
  **new window** — a sized popup, opened from the operator's click so the browser allows it, and
  falling back to a tab if the browser insists. Being same-origin, it is on the same channel as
  the app that opened it. On the projector: previous, next, and a toggle for on and off — nothing
  more for this first version. The OBS overlay follows in a later slice, where it needs its own
  exclusive control surface inside OBS (as the current dock is) because that is a different
  browser process from the operator's.
- A **jump-to-it** control on a scripture entry and on a song entry, opening that passage or that
  song the way a search result does.
- **Display mode**, held on the server and shared by every tab: at most one Tata Ibadah is being
  displayed at a time; while one is, its entries cannot be added to, edited, reordered or
  deleted from any tab, though the Tata Ibadah's own fields stay editable (they are not on
  screen). Its project button becomes **Stop projecting** and **Update the current state** (to
  re-read a song whose lyrics changed while it is on screen).
- **Soft deletion for songs, songbooks and song verses**, so a service entry that refers to one
  keeps a working reference and shows that its target was deleted, rather than breaking or
  disappearing.

### Out of scope

- Any change to the current OBS dock, source, projection or settings pages, their templates,
  scripts or endpoints. They are read as a reference for the display rules and otherwise left
  alone.
- Any change to how the *current* display splits text into two lines, sizes its font, or grows
  its box. The new display implements those rules in new code.
- Reworking the Bible or Songs docks' own bookmark/workflow behaviour.
- Editing entries from a sidebar, and any public (anonymous) editing of entries: the sidebar
  editors of spec 005 keep their scope (songbooks, songs as records, Tata Ibadah headers).
- Driving the display from an OBS dock: this version drives it from the projector page the
  project button opens. A dock can come later, on the same channel.
- Hard-deleting a song, songbook or verse that a service entry refers to.
- Deleting a Tata Ibadah, and the old-rows migration (both separate slices).

## Domain rules

- **One running order.** Entries are ordered by `order_number` within their Tata Ibadah, and the
  numbers are contiguous from 1. The second-level sidebar shows the entries in that order, and
  reflects a pending reorder immediately, before it is saved.
- **A kind's fields.** Text: title, text. Section break: title (a label), no text. Scripture:
  book translation, chapter, start verse, optional end verse (end ≥ start, same chapter).
  Song: song, and a non-empty set of included verse numbers.
- **Dropdowns come from the data.** Chapters are the book's chapter count, verses are that
  chapter's verses. Selecting a book or a chapter resets the fields below it to 1.
- **A song entry fixes which verses it shows.** A new song entry includes all of the song's
  verses at that moment, and that list of numbers is what is stored. A verse added to the song
  later does *not* appear in a prepared service — it has to be added to the entry deliberately.
  What the song *says* is still resolved live, so a lyric edit reaches every service that uses
  it. At least one verse must stay included; the control reads "all verses" when every verse is
  included, otherwise it names the ones that are.
- **A deleted song is still a working reference.** Songs, songbooks and verses are soft-deleted:
  the row stays, normal lists stop offering it, and a service entry that refers to it keeps
  resolving what it can and says its target was deleted, so the operator can see and fix the
  order rather than lose it.
- **Reorder is transactional in the UI.** While entries are being reordered, nothing else is
  added, edited or reordered; the pending order lives in the page until Save or Discard. Leaving
  — switching what is open, opening another Tata Ibadah, running a search, or closing the tab —
  asks first, in a modal, and the answer decides: keep editing, discard, or save.
- **Rendering is per kind, into one shape.** Each kind resolves to the title + body pair the
  Tata Ibadah source already renders: a text entry is its own text; a scripture entry is the
  passage as the app already cites it; a song entry is the selected verses as the app already
  formats lyrics; a section break is its label with no body.
- **The projector is a window, not a page you navigate to.** It opens beside the app, sized for a
  screen, and is asked for full screen on the operator's own gesture rather than grabbing it.
  Closing it does not stop projecting on its own; the toggle does.
- **The display state lives in the browser that started it, and nowhere else.** It is shared
  across that browser's tabs over a `BroadcastChannel`, and deliberately not stored on the
  server: several laptops project to different screens — one for OBS, several for displays — and
  each has to be able to show something different. No server record is added for any of this.
- **One Tata Ibadah at a time, per browser.** Starting another Tata Ibadah's projection in the
  same browser replaces the first. Another browser is untouched and may show something else.
- **The entry lock belongs to the browser that is displaying.** While a Tata Ibadah is on screen
  there, none of its tabs will add, edit, reorder or delete an entry, while the Tata Ibadah's own
  fields stay editable (they are not on screen). The endpoints keep their normal validation: this
  is the shell refusing an action, not a server-side restriction, so the current API is exactly
  as it is today.
- **The display is only pushed when the operator shows it.** Showing an entry is an explicit
  action; reordering never re-pushes what is on screen, and the display keeps showing what it was
  told to until the operator shows something else or presses Update.
- **Hand-written, and consistent with the public site.** The new projector and overlay share the
  public reading app's design tokens and components rather than the OBS docks' Fomantic stack, so
  the surfaces a congregation sees look like one product.
- **A body's two lines.** The new display splits a body into pairs of lines the way the operator
  expects, and a blank line separates what should appear alone.

## Acceptance scenarios

### Scenario: A service order holds all kinds

- **Given** a Tata Ibadah in the reading app
- **When** I add a scripture, a song, a text and a section break to it
- **Then** all four appear in the service order, in the order I added them, and in the sidebar

### Scenario: The scripture modal's dropdowns cascade

- **Given** the scripture modal open with a book, chapter and verse chosen
- **When** I choose a different book
- **Then** the chapter and verse numbers reset to 1 and the verse list follows the new chapter

### Scenario: A song entry excludes verses

- **Given** the song modal for a song with several verses
- **Then** every verse is checked and the label reads "all verses"
- **When** I uncheck one verse
- **Then** the label names the remaining verses, and the displayed entry omits the unchecked one

### Scenario: Reorder holds until saved

- **Given** a service order with several entries
- **When** I drag one to a new position
- **Then** the sidebar's order follows the drag immediately, the add controls are gone, and Save
  and Discard appear at the top
- **When** I press Discard
- **Then** the entries return to the order they had before the drag

### Scenario: Leaving with unsaved order asks first

- **Given** a reordered, unsaved service order
- **When** I open another Tata Ibadah, or run a search, or close the tab
- **Then** a confirmation appears and nothing is left until I answer

### Scenario: The new display renders every kind

- **Given** the new projector and the new overlay open
- **When** the operator shows a scripture entry, then a song entry, then a text entry, then a
  section break
- **Then** each appears with its title and body, split into two lines, with the projector fitting
  the font to the screen and the overlay growing its box to the content
- **And** a blank line in a body holds the screen with one line at a time

### Scenario: Display mode blocks entry edits across that browser's tabs

- **Given** a Tata Ibadah is being displayed from one tab
- **Then** its project button reads Stop projecting and Update the current state
- **When** the same browser opens the app in another tab
- **Then** the display mode is already on there too, and adding, editing, reordering or deleting an
  entry is refused in both, while the Tata Ibadah's own fields stay editable

### Scenario: Two laptops, two screens, two different things

- **Given** one laptop is projecting a Tata Ibadah
- **When** a second laptop opens the app and projects a different Tata Ibadah
- **Then** each shows its own, neither disturbs the other, and neither laptop is locked by the
  other's display mode

### Scenario: Only one Tata Ibadah at a time, per browser

- **Given** one Tata Ibadah is being displayed in this browser
- **When** another Tata Ibadah's project button is used
- **Then** the first stops being displayed and the second takes its place

### Scenario: A song whose lyrics changed while on screen

- **Given** a song entry is on screen
- **When** that song's lyrics are changed and Update the current state is pressed
- **Then** the screen shows the new lyrics

### Scenario: A service entry whose song was deleted

- **Given** a service entry for a song that is later soft-deleted
- **When** the Tata Ibadah is opened
- **Then** the entry still resolves what it can, and says its target was deleted

### Scenario: Jumping to an entry's source

- **Given** a service order with scriptures and songs
- **When** I use the jump control on one
- **Then** that passage or song opens the way a search result does

### Scenario: The production app is untouched

- **Given** the endpoints and pages that exist today
- **When** they are exercised against the same data
- **Then** their responses are unchanged, and the existing Tata Ibadah items, docks, sources and
  projection behave exactly as before

## Traceability

Filled per slice as it lands.

### Slice 1 — the model (landed 2026-10-03)

- Model, rules, citation and per-kind `resolve()`: `multimedia/tatib/models.py`
- Migration: `multimedia/tatib/migrations/0005_serviceentry.py`
- Admin: `multimedia/tatib/admin.py`
- Tests: `multimedia/tatib/tests.py` — `ServiceEntryTests` (14), covering each kind's
  `(title, body)`, the passage range rules, the included-verse list (a verse added to a song
  later is not in a prepared entry; a lyric edit does reach it), ordering, and a service holding
  both legacy items and entries
- Compatibility: no current template, endpoint or model changed; the pre-existing 116 tests pass
  unchanged alongside these

### Slice 2 — the content pane (landed 2026-10-04)

- Endpoints and forms: `multimedia/web/reading/entries.py`, `views.py` and its URLs; the fragments
  `reading/_entry_form.html` and `reading/_entry_song_options.html`
- The pane, the four add controls, the per-entry edit and delete, the empty-service invitation:
  `reading/tatib.html`, `static/web/entries.js`, `static/web/reading.js`
- The modal's chrome and the pickers: `reading/_editor_modal.html`,
  `static/styles/design/components.css`, `tokens.css` (`--danger`)
- App tests: `multimedia/web/tests.py` — the six endpoints per kind, their validation errors, the
  insert-after rule and the pane's controls; `multimedia/tatib/tests.py` — a text entry needs its
  text
- E2E: `tests/e2e/test_entries.py` (10) — each modal, the cascading dropdowns, the to-verse
  disabled state with its hover note, the verse checklist's label and its one-verse case, the
  filter inside each dropdown, the panes refreshing in place
- Verified: 82 tests green across `multimedia.web`, `multimedia.tatib` and the design tokens; the
  entry e2e green (10/10). The rest of the e2e suite runs at the push step, at the owner's request
- Deviations from the mockup, on the owner's instruction: no x-close on the modal, a filter inside
  each picker rather than beside it, and the verse checklist inside a dropdown

### Slice 4 — the new display and display mode (landed 2026-10-04)

- The projector: `multimedia/web/templates/reading/projector.html`,
  `static/styles/design/projector.css`, `static/web/projector.js`; the view and its slide payload
  (`service_projector`, `_projector_slides`) in `multimedia/web/reading/views.py`, routed at
  `/obs/service/<id>/` (`web-service-projector`) so every `/obs/` path the dock uses stays as it is
- The display state and the lock: `static/web/display.js` (localStorage plus its own
  `BroadcastChannel`), the project group in `reading/tatib.html`, the decline in
  `static/web/entries.js`
- App tests: `ServiceProjectorTests` (11) — its own path, the page on the app's tokens, every kind
  with its title and body in the running order, the blank line kept, a section break with no body,
  the legacy rows before the entries, the three controls, the project button and its two states,
  and a lyric edit reaching a fresh projection
- E2E: `tests/e2e/test_projector.py` (4) — one slide at a time with the font fitted to the screen,
  prev/next/toggle, the button's states, the two-tab lock, the Tata Ibadah's own fields staying
  editable, a second browser untouched, and Update re-reading the page while keeping its place
- Two readings taken, marked **to confirm**: (1) the projector shows the service's whole running
  order — the legacy rows before the entries — so a service that predates this spec can be
  displayed too, not only one built from entries; (2) while anything is displaying in a browser,
  entry writes are declined in every one of its tabs (the plan's wording), not only for the
  displaying service
- Deferred, per the plan: the OBS overlay. The projector window is this version's whole display;
  the overlay needs its own answer for reaching inside OBS
- Verified: 93 tests green across the app; the projector e2e green (4/4) and the entry e2e green
  (10/10)

### Slice 4, the display's own round (owner, 2026-10-04, later)

The owner's review of the first projector, taken as the shape of the display:

- **Only the header and the words.** The controls are gone from the screen; the operator drives it
  from the keyboard -- left/right to move, space to turn the display on and off (Home and End
  jump to the ends). Nothing but a header and up to two lines is drawn.
- **White on black, in the current projector's face** (`"CMG Sans", sans-serif`, weight 700,
  line-height 1.37), which is what the screen has always looked like. The display no longer wears
  the reading app's light/dark tokens: it is a display, not a page.
- **A passage is one verse a screen**, headed by that verse's reference and, when the translation
  carries one, its title (`bible.Verse.title`). The verse number stays out of the body: the
  reference already names it.
- **A text is two lines at a time** under its own header, with a blank line ending a screen so a
  line can hold the screen alone.
- **A song is its lyrics alone, two lines at a time** -- no citation on screen.
- **A section break shows nothing at all**: it is the operator's own note.
- **The project button rides with the date** at the top right of the page, in line with it, with an
  icon; its two states are unchanged.
- **The reading pane carries only the reference** for a passage or a song (its citation, still the
  jump link); the words belong on the display. The sidebar's contents rows keep the entry's text
  as their filter key.

Implemented in `_projector_screens`, `_line_pairs` and `_scripture_screens`
(`multimedia/web/reading/views.py`), the display's own stylesheet, the keyboard in
`static/web/projector.js`, the head's action block in `reading/base.html` and
`reading/tatib.html`, and `_entry_blocks` for the pane. Tests: `ServiceProjectorTests` (11) and
`tests/e2e/test_projector.py` (7); 100 app tests green. Verified live on "Pengakuan Iman": 8
screens, two lines each, black on white, `"CMG Sans"` at weight 700, no buttons, keys moving and
blanking, and the pane's entries showing their references alone.

### Slice 4, the display's colours, centring and morphs (owner, 2026-10-04, later still)

- **The product's dark palette, not black and white.** The page links the design tokens and pins
  `data-theme="dark"`: the warm near-black canvas (`#14130F`) and the warm off-white ink
  (`#F5F3EE`). It never follows the operator's light/dark choice -- a display is not a page.
- **The header reads apart from the words**, in the display's own bright warm gold
  (`--display-head`, `#FFD166` -- 13:1 on this canvas). A product token was tried first (the dark
  theme's accent) and sent back for being too close to the words for a heading.
- **The face**: the repo's own code uses exactly two -- `"CMG Sans"` (the current projector) and
  `"Source Sans Pro"` (the songs, bible and service sources and the dock item previews), and it
  ships neither as a file, so both come from the machine. The display stacks
  `"CMG Sans", "Source Sans Pro", sans-serif`: the projector's own face first, the other surfaces'
  behind it.
- **The texts are centred both ways** -- the words' own ink, not just their boxes: the header's gap
  is flex content rather than a margin, and the pages were measured at 0px off centre on both axes.
- **The words always fit the screen, and as large as they can be.** The fitting is the current
  projector's own pair of loops (`resizeTitleFont` / `resizeTextFont`), kept in its shape --
  `do...while`, one pixel at a time, from 50 for the header and 100 for the words, floor 2 -- so it
  settles on the largest size that fits: one pixel more must not. Two deliberate differences: the
  measure is the display's own box rather than the window, and the words' condition also reads the
  **ink's box** (a `Range` rect), because a wrapped block reports a height a few pixels inside the
  words' real extents and the last line then hangs over the edge.
  **The original's `>= window - 72` does not transfer to measuring the element's own parent**: a
  full-width block is always ">= clientWidth - margin", so a faithful port ran to the floor (564
  characters came out at 4px instead of 41px). The port compares strictly against the box. Verified
  live at 1400×800 -- 114 characters at 73px, 564 at 41px, 2,820 at 20px, 14,100 at 9px, each
  fitting with one pixel more failing to.
- **The display's own box has to be inside the window, or the fitting fits words into space that is
  not there.** The projector page is standalone: it loads `tokens.css` and `projector.css`, not the
  product's `components.css`, which is where the design system's `*, *::before, *::after
  { box-sizing: border-box }` lives. On the UA's content-box default,
  `.projector__screen { height: 100%; padding: 64px }` measured 928px on an 800px window with its
  last 64px off screen, and the fitting -- which measures that box -- put a long text's last line
  there. A shorter screen (Ester 8:9, nine wrapped lines) looked perfect in the same build, which is
  exactly how it was reported. The page carries its own reset now, and an e2e pins the invariant:
  the display box inside the window on all four sides, and a page that does not scroll. This is also
  what the current projector's `72` is for -- its loop measures the WINDOW and subtracts the inset,
  so an inflated container cannot fool it.
- **The words' own lines get air between them, and only there.** A screen's lines are separate lines,
  not one wrapped paragraph, so `.screen__line + .screen__line { margin-top: 0.45em }` -- in `em`, so
  the gap travels with the fitted size; a wrapped row keeps the line-height alone. The fitting
  measures it (the ink's box runs from the first line's top to the last line's bottom, gap included),
  and it was measured live: 24.8px at a 55px fit, with the whole text still inside the screen.
- **Closing the projector window ends the display.** Nobody presses Stop on a screen that is no
  longer there. The browser tells the OPENER the moment the window it opened goes (its handle's
  `closed`), which stops the display at once, and the projector also leaves a **beat** behind -- a
  stamp in localStorage plus a channel message every couple of seconds -- covering the tabs that did
  not open it, a shell reloaded since, and a window that died rather than closed. The wait is
  generous (90s) because a hidden tab's timers are throttled to about one a minute, and a state
  written just now counts as alive by its own stamp, so the moment between pressing Project and the
  window's first beat cannot stop the display it just started. The stop releases the lock in every
  tab of that browser and says why; a display left on from an earlier session is stopped as the page
  loads.
- **Short morphs** carry a move or a toggle: the arriving screen fades and rises (from the
  direction of travel), the one it replaces fades out the other way, and space fades the words
  rather than blanking them. Reduced motion makes every move instant.

Two defects this round found and fixed, both invisible to a source read:

- **A shorthand carrying two durations.** `transition: opacity 220ms var(--ease)` looks harmless,
  but `--ease` is `200ms cubic-bezier(...)`: the shorthand takes the first time as the duration and
  the second as the DELAY, so every transition and animation ran 200ms late. The display now
  carries a timing-only `--display-ease`.
- **The fitting never reached the words.** `.screen__line` declared its own `font-size: 100px`, so
  the container's fitted size was overridden: the fitting read a wrapped block that "fitted" while
  the ink ran 24px past the screen's edge. The size lives on the container and the lines inherit it;
  the e2e now measures the ink's own box, not the block's, and asserts it stays inside.

Verified live: background `rgb(20,19,15)`, ink `rgb(245,243,238)`, face
`"CMG Sans", "Source Sans Pro", sans-serif`, 0px off centre on both axes, the arriving screen
animating `screenIn` while the leaving one fades, and the off state fading 1 → 0.25 → 0.05 → 0.

## Open questions for Accept

1. **Name.** I propose a new model **`ServiceEntry`** ("service entry") in the `tatib` app, with
   the glossary gaining that term — one ordered element that may be a text, a scripture, a song
   or a section break — and `TataIbadahItem` left exactly as it is. Extending the existing model
   instead would put the production dock and API on a changing table, so I have not.
2. **The old rows.** Migrating existing `TataIbadahItem` rows into entries is deferred to a
   separate slice after this one lands, as you said. Until then both models exist side by side
   and a Tata Ibadah may be shown by either path.
3. **The verses a song entry shows are stored as the numbers included, not the numbers left
   out** (your correction). A verse added to the song later does not appear in a prepared
   service; the operator adds it deliberately. Resolved. ✔
4. **Leaving with unsaved reordering** asks first, on the in-page switches (contents, another
   Tata Ibadah, search) and on closing the tab (`beforeunload`). Plainly, "expensive to rebuild"
   meant: if you rearrange twelve items and then click away without saving, you do that
   rearranging again by hand. The confirmation exists so that click cannot silently throw the
   work away. If you would rather it never ask, say so and I will drop it.
5. **A running change** to an entry that is currently on screen: the display keeps showing what
   it was told to show until the operator shows something else — the order change alone never
   re-pushes the display.
### Answered

1. **Name:** `ServiceEntry` in the `tatib` app. ✔
2. **Control surface:** a project button on the Tata Ibadah that opens the new projector in a new
   window (a tab if the browser insists); previous, next and an on/off toggle on the projector.
   No new dock in this version; the overlay waits for one, later. ✔
3. **Stack:** hand-written, on the public reading app's design tokens, so the public site and the
   OBS surfaces stop looking like two products. ✔
4. **URLs:** new paths of their own, e.g. `/obs/service/...`, leaving `/obs/...` alone. ✔
5. **Song sync:** see the amended question 3 above — exclusions stored, content live. ✔ (to confirm)
6. **The leave guard:** see the amended question 4 — kept, and here is what I meant. ✔ (to confirm)
7. **Edits while displaying:** refused for entries, allowed for the Tata Ibadah's own fields,
   everywhere, enforced by the server. ✔
