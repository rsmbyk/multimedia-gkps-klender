# Spec 006: Service entries — one Tata Ibadah holds texts, scriptures and songs

- **Status:** Draft — needs the owner's Accept (SDD gate; no implementation before that)
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
- **A project button** on a Tata Ibadah in the reading app that opens the new projector in a new
  tab, showing that Tata Ibadah. On the projector: previous, next, and a toggle for on and off —
  nothing more for this first version.
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
- **A song entry follows its song.** A new song entry shows every verse, and what it shows is
  resolved from the song when it is displayed: change a song's lyrics and the entry follows.
  What the operator can set is which verses to *leave out*, and that is what is stored — so a
  verse added to the song later appears in the service, and an excluded one stays excluded. At
  least one verse must remain included. The control's label reads "all verses" when nothing is
  excluded, otherwise the verses it will show.
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
- **One Tata Ibadah on screen at a time.** The display state lives on the server — which Tata
  Ibadah, which entry, and whether it is on — so every tab and the projector agree, and a second
  tab is in the same mode as the first. Starting another Tata Ibadah's projection replaces the
  first. While a Tata Ibadah is being displayed, entry writes against it are refused by the
  server, not merely hidden in the page.
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

### Scenario: Display mode blocks entry edits everywhere

- **Given** a Tata Ibadah is being displayed from one tab
- **Then** its project button reads Stop projecting and Update the current state
- **When** another tab is opened, or the same Tata Ibadah is opened elsewhere
- **Then** the display mode is already on for it, and adding, editing, reordering or deleting an
  entry is refused in every tab, while the Tata Ibadah's own fields stay editable

### Scenario: Only one Tata Ibadah at a time

- **Given** one Tata Ibadah is being displayed
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

## Open questions for Accept

1. **Name.** I propose a new model **`ServiceEntry`** ("service entry") in the `tatib` app, with
   the glossary gaining that term — one ordered element that may be a text, a scripture, a song
   or a section break — and `TataIbadahItem` left exactly as it is. Extending the existing model
   instead would put the production dock and API on a changing table, so I have not.
2. **The old rows.** Migrating existing `TataIbadahItem` rows into entries is deferred to a
   separate slice after this one lands, as you said. Until then both models exist side by side
   and a Tata Ibadah may be shown by either path.
3. **Read your "always sync" as: exclusions are stored, not inclusions.** A new verse in the song
   appears in the service; a verse the operator unchecked stays out. If you meant the opposite (a
   frozen list of verses, so changing a song never changes a prepared service), say so — it is a
   one-field difference, but it decides whether stored services follow live edits.
4. **Leaving with unsaved reordering** asks first, on the in-page switches (contents, another
   Tata Ibadah, search) and on closing the tab (`beforeunload`). By "expensive to rebuild" I mean
   the operator's work in assembling and ordering a service by hand, not anything the app
   computes — if a service order is cheap to recreate, say so and I will drop the guard.
5. **A running change** to an entry that is currently on screen: the display keeps showing what
   it was told to show until the operator shows something else — the order change alone never
   re-pushes the display.
### Answered

1. **Name:** `ServiceEntry` in the `tatib` app. ✔
2. **Control surface:** a project button on the Tata Ibadah that opens the new projector in a new
   tab; previous, next and an on/off toggle on the projector. No new dock in this version. ✔
3. **Stack:** hand-written, on the public reading app's design tokens, so the public site and the
   OBS surfaces stop looking like two products. ✔
4. **URLs:** new paths of their own, e.g. `/obs/service/...`, leaving `/obs/...` alone. ✔
5. **Song sync:** see the amended question 3 above — exclusions stored, content live. ✔ (to confirm)
6. **The leave guard:** see the amended question 4 — kept, and here is what I meant. ✔ (to confirm)
7. **Edits while displaying:** refused for entries, allowed for the Tata Ibadah's own fields,
   everywhere, enforced by the server. ✔
