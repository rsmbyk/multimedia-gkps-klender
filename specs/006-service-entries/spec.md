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
4. **The display contract keeps its shape.** Whatever an entry is, what the new dock publishes
   for the new display is a title and a body — the same pair of strings the current Tata Ibadah
   source renders. My projector owns the font sizing, my overlay owns the container growth, and
   the split into two lines lives on the display side, exactly as it does today.

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
- **A way for the operator to drive them**: showing an entry, moving to the previous or next
  entry, and clearing the display — see the open question on whether that control surface is the
  reading app's Tata Ibadah page or a new dock beside the old one.

### Out of scope

- Any change to the current OBS dock, source, projection or settings pages, their templates,
  scripts or endpoints. They are read as a reference for the display rules and otherwise left
  alone.
- Any change to how the *current* display splits text into two lines, sizes its font, or grows
  its box. The new display implements those rules in new code.
- Reworking the Bible or Songs docks' own bookmark/workflow behaviour.
- Editing entries from a sidebar, and any public (anonymous) editing of entries: the sidebar
  editors of spec 005 keep their scope (songbooks, songs as records, Tata Ibadah headers).
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
- **All verses by default.** A new song entry includes every verse; at least one must stay
  included. The label reads "all verses" when nothing is excluded, otherwise the chosen numbers.
- **Reorder is transactional in the UI.** While entries are being reordered, nothing else is
  added, edited or reordered; the pending order lives in the page until Save or Discard. Leaving
  — switching what is open, opening another Tata Ibadah, running a search, or closing the tab —
  asks first, in a modal, and the answer decides: keep editing, discard, or save.
- **Rendering is per kind, into one shape.** Each kind resolves to the title + body pair the
  Tata Ibadah source already renders: a text entry is its own text; a scripture entry is the
  passage as the app already cites it; a song entry is the selected verses as the app already
  formats lyrics; a section break is its label with no body.
- **The display is only pushed when the operator shows it.** The new display publishes only what
  the operator shows it, on its own channel, with its own idea of being active — so the old
  docks' toggles and the new one never contend.
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
3. **The song entry's verses** are stored as the explicit list of included verse numbers (so a
   later insert of a verse cannot silently change a prepared service).
4. **Leaving** covers the in-page switches (contents, another Tata Ibadah, search) *and* closing
   the tab (`beforeunload`), since a prepared service is expensive to rebuild.
5. **A running change** to an entry that is currently on screen: the display keeps showing what
   it was told to show until the operator shows something else — the order change alone never
   re-pushes the display.
6. **What drives the new display, and how it is built.** Two linked choices. (a) The control
   surface: the reading app's Tata Ibadah page, with a Show action per entry, or a new OBS dock
   built beside the old one — I lean to a new dock, since the operator works inside OBS and the
   old dock must keep working untouched. (b) The stack for the new projector and overlay: the
   same one the docks use today (Fomantic/jQuery/RxJS), so the operator's habits carry over, or
   hand-written like the public site. My default is a new dock plus the docks' stack, both on a
   new sync channel; tell me if you want it otherwise.
7. **Where the new pages live.** I propose new URLs of their own (for example
   `/obs/service/project/source` and `/obs/service/tatib/source`) rather than reusing the
   current `/obs/...` paths, so nothing about the current pages can be reached, redirected or
   mistaken for them.
