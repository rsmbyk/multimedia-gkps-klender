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
