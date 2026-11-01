# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- A Tata Ibadah is now a **service or a template**: the type is chosen when it is created, kept paired with its date by the model, a database constraint and every writing endpoint, and never changed by an edit — an existing date-less record is a template and a dated one a service. Templates carry two new entry kinds, a **fill-in** (a title and the kind it will resolve to, holding no content) and a **choice** (a title and ordered options, each a complete entry of that kind added from the choice's own row), and the projector controls give way to **Use template**: settle every slot through that kind's own modal — validated, never written to the template — and the normal name and date form, in two steps, then one atomic create that copies the template's order with each slot replaced in place. Editing any Tata Ibadah offers **Copy as template**, which converts nothing. A template never projects, never appears in the dock, and its media counts as a use without ever being auto-downloaded.
- The OBS overlay now paints by the kind of what is on air: a song keeps its subtitle caption, a passage becomes a quotation card naming its Bible reference and the verse's own title above a hairline, and a liturgy becomes a left-aligned script panel carrying its title and its speaker turns, each mark in a column of its own so wrapped rows hang under the words. The panels arrive and leave with a short motion, a step to the next verse morphs the panel's box instead of re-entering, and a machine asking for reduced motion gets a cut.
- A passage row and a song row on the Tata Ibadah stage now carry a mark of their own — a small grey open book for a passage, a single note for a song — sitting on the media chip's centre line and with the title starting on the media filenames' own column, so the stage holds one left rail and a file is never mistaken for a passage or a song. The mark is decorative, takes no pointer and adds no height; a song title may take one more line at a narrow reading pane, where the media column is 250px.
- The projector's Go To now searches a small index held in the page itself, so its suggestions appear as you type without a request; choosing a passage or a song fetches it — the whole chapter in both editions, or the whole song — while the panel refuses every key, click and dismissal and shows a loading indicator on the chosen row and beside the shortcuts button. A step that leaves the loaded chapter fetches the next one under the same lock, and the page's Update re-reads the index so a song added mid-service is findable.
- The projector's images and PDF pages now fill the stage instead of painting at their own size — a 182×277 photo reads 725×1104 on a 1856×1104 stage — with `T` switching between fit width and fit height and the excess panned by dragging or with the wheel; the shortcut sheet lists the key under Image and PDF.

### Changed

- A media entry ends on the projector's built-in rest now, the blank every text, passage and song entry already draws after itself: a picture, a recording, a video, a PDF page or a slide deck is followed by one blank screen before the next entry, so no step goes from one picture straight to the next and a service that finishes on a picture can be left blank by stepping. The rest belongs to the entry — it is not a row in the order — the dock lists it under the media row and steps onto it, and an entry whose file is gone still keeps its one rest. The media screens themselves do not move: same payloads, same fit, same lock.
- The operator dock fills whatever panel it is given: the page used to cap itself at 560px and centre in the window, leaving a strip of background on both sides of an OBS dock the operator had widened — it now takes the panel's whole width, and the picker's rows run with it (1424px of a 1440px dock, its date on the row's right edge). The picker stays one column at every size, its bucket heads still stick, and nothing below 560px moves: a narrow OBS dock paints exactly as it did.
- A playing recording now owns the projector screen the way a playing video does: its own screen fills the viewport, the corner cue and the mouse zones are off screen, and no arrow, page, home/end, entry jump, mouse zone, cue control or Go To moves the projector until the recording is paused. A stray `ArrowRight` used to jump to the next screen and tear the player down, so a 5:02 recording two seconds in came back at `0:00`. `Space` pauses and returns the normal screen at the position playback had reached, leaving fullscreen by the browser's own gesture pauses it too, the end of the recording returns on its own, and a browser that refuses fullscreen keeps the screen locked while the recording plays.
- The main rail names its sections with the marks the stage already draws: the Bible is an open book
  with a Latin cross above it — in the rail, in the Alkitab panel's empty state, on a passage row and on
  the empty stage's Add Passage tile — the beamed note is one drawing on the rail, on a song row and on
  the Add Song tile, and Tata Ibadah's document is a clipboard. An audio file no longer wears the song's
  note: it draws a five-bar waveform in the stage's chip, the Media Library, the service-media dialog and
  the upload preview, so a media file is never mistaken for a hymn. Every mark keeps its box — 24px in
  the 44px rail button, 20px on a row, 23px in the 42px chip — and its own ink.
- The Transfers dialog's scrollbar is the dialog's own edge now: it runs against the right border and down to the bottom border, where it used to sit 22px inside the panel and stop 23px short of the bottom. The rows, the title, the age headings and the list's top do not move, the last row still keeps 22px above the border at the end of the scroll, and the dialog clips the bar to its rounded corner so nothing paints over it.
- A song's verse tabs in the Preview dialog stand on a row of their own under the title now, so a long title takes the header's whole width before it ellipsizes — 660px at the 704px dialog, where it had 570px — and the header closes with one rule beneath them, 14px under the tabs, the lyrics still starting 22px below it. The dialog opens on its reading body instead of on verse tab `1`, so no tab carries a focus ring; `Tab` moves from the body to the selected tab and `Shift+Tab` back, and every preview without verse tabs — passage, text, image, audio, video, PDF — is unchanged.

- The projector's shortcuts sheet names audio and video in groups of their own: `Audio` and `Video` each head one `Play/Pause` row on the Space chord, and the combined `Audio/Video Play/Pause` row is gone from `Display`, which keeps `Show or Hide Words`, `Show or Hide Corner` and `Keyboard Shortcuts`. The two groups join the sheet's middle column, so its box stays 676px tall at 1080p and 720p and nothing inside it scrolls; Space itself is unchanged — it still plays or pauses the media that is showing and hides or shows the words when none is.
- The Transfers dialog draws the boundary between the transfers that finished while you were not looking and the older ones once: the row above the seam no longer stacks its 1px border under the divider's 2px line, and the seam keeps 9px of space either side. A list taller than the dialog now scrolls inside it — the title stays put, the dialog's bottom padding survives, and no row paints over the page; before, nine rows ran 19px into that padding and fifteen painted 451px outside the dialog.
- The Media Library list groups its files by age now — `Last 30 days`, `Earlier this year`, `Older` — instead of one heading per upload day, and the Transfers dialog groups its history into `Last 24 hours`, `Last 7 days`, `Last 30 days`, `Earlier this year` and `Older`, dated by when each transfer started. Both take the Tata Ibadah list's own windows and words, with the day taken in `Asia/Jakarta`; a size sort draws no heading, an ascending sort reverses the buckets so the list still reads oldest first, and the transfer rail's progress flyout keeps its shape and draws none. Active transfers still come first, inside the bucket their start time gives them.
- A service entry no longer moves when its add row opens: each row keeps a 20px slot in the page and draws its bar on top of it, centred on a faint seam line, so the entry under the pointer stays where it is — it used to drop 31.6px, and a sweep of the pointer down the list accumulated 234.8px of movement. The bar is centred on the column, its hit area stops at its buttons so the entry's own controls stay clickable, and the gap between entries is 20px with the first seam matching it.
- A Tata Ibadah entry draws nothing at rest now: the fill that composited to three of 255 levels off the canvas and the 1px ring that carried all the signal are gone, from every kind — text, scripture, song, media and the section break. The box itself stays (its 56px floor, its padding, the reserved column for the controls), and pointing at an entry, reaching it with the keyboard, or opening its editor still fills it with the rail's own hover tint.
- The Tata Ibadah stage's entry titles read as the page's own ink with no resting underline now, and underline 3px under the text only on hover or when reached by keyboard. The preview, edit and delete controls moved into a column of their own — labelled where the reading pane is 700px or wider, icons below it — so a title is never drawn under them.
- The landing page's search field is centred on the window's middle now, with the logo above it, from a 1920px desktop down to a 320px phone; it used to sit 49px low on a desktop and 85px low on a phone, because the page centred the logo and the field as one block and, below 720px, measured the section against the wrong padding.
- Below 1272px the sidebars no longer squeeze the page: opening one leaves the reading pane's width untouched and floats it over the page as a drawer that slides out from under the main rail. Only one section's stack is open at a time, a service's contents cover their own list exactly instead of sitting beside it, a click on the dimmed page or Escape closes the whole stack, and the rail reopens the level last used. Above 1272px the columns push the page exactly as before.
- A phone gets a top toolbar — the drawer control beside the logo at the left, the light/dark control at the right — and the rail's icon strip becomes a full-width menu drawer that names its destinations. The control opens the menu when nothing is open and closes whatever is, never stepping back one level; choosing a section slides its list over the still-open menu. A service offers no contents drawer there, so its rows open the service and close the drawer, and the Project control is no longer drawn.
- A sidebar row's edit control now shows on a touch screen, where nothing can hover — the exemption the entry controls and the add tiles already carried. At the phone width a row stacks its date under its name instead of clipping it beside that always-visible control, and every toolbar icon is drawn at one size.
- A service-order row in the Tata Ibadah sidebar is three lines now, whatever it holds — a text body's first three lines, a media or passage title, a song's heading above its `Bait …` line, a legacy row — and a row that hides text ends `…`. The 60-character cut is gone, so a 64-character title is shown whole; a song's heading spends at most two lines so its `Bait …` line always shows; and a run wider than the pane, such as a pasted link, wraps inside the row instead of running past its edge with the ellipsis clipped away. The saved copy draws the same rows.
- A text entry now opens in the same large dialog as `+ Media` — 840×760, with the same title band, gutters and action row — on both Create and Edit, and its Text box fills the height the frame leaves instead of sitting in a 131px box. The passage, song and media-edit forms keep their compact dialog. Every editor dialog is now placed against the window rather than the document, so a service scrolled under it no longer opens the dialog above the page's top edge.
- The Tata Ibadah sidebar groups its services by age now — `Upcoming`, `Last 30 days`, `Earlier this year`, `Older` — instead of by calendar month. Today's services come first inside `Upcoming` and carry a `Today` badge, so a service dated today is no longer buried under every future one; the day is the congregation's (`Asia/Jakarta`), so a service does not change group at 07:00. A bucket with no services draws no heading and no divider. The operator dock's picker uses the same four groups and the same badge, in place of its today and upcoming row tints, and a saved page draws them too, so the list does not regroup when it goes offline.
- The Kidung sidebar now reads its hymn songbooks first — Haleluya, Kidung Jemaat, Pelengkap Kidung Jemaat, Nyanyikanlah Kidung Baru — then one divider, then the ordinary songbooks A–Z, with no heading on either side. A group the filter empties takes the divider with it, and a saved Kidung page draws the same two groups, so the list does not reorder when the online page arrives.
- An empty Tata Ibadah's five add actions are now one row of square, icon-only tiles — 52px, 10px apart, the glyph alone on the face, the sentence kept as the tooltip and the accessible name — instead of a stack of full-width labelled buttons. `Add Media`, the one action that never had a glyph, now wears a frame with a play triangle. A reading column too narrow to give five tiles 44px each takes them three and two at full size rather than shrinking them.
- Every reading page's browser tab now names the site `Multimedia GKPS Klender`, the name the rest of the application already uses, and the index's tab stops there: the search-first landing's tab reads `Multimedia GKPS Klender` instead of trailing the tagline the tab strip truncated anyway. A reading page keeps its leading text — `1 Musa 1`, `PKJ 4`, a service's name, `Results for “…”`, `Media Library` — and appends the name; the saved copy and an in-place Bible edition switch write the same titles, so a tab never renames itself mid-session. The page's own heading, the search field's label and the logo's alt text keep the congregation name `GKPS Klender`.

### Removed

- The app no longer keeps a saved copy of the public library: the browser database, the service worker and its page shells, the rail's offline status panel and the saved-copy paint are gone, so reading and projection always show the server's own page. The four `/offline/…` routes and `/service-worker.js` answer 404, and a browser that still holds the old library drops it on its next visit.
- The **Break** service entry kind is retired: no add row, no start bar and no empty-service tile offers one, and the editor endpoints refuse it, so a break cannot be created from any surface — a stale page or a direct request included. The breaks already written still draw their full-width divider on the stage and their row in the sidebar, still contribute their projector screen, and still reorder and delete as before; the stored kind and its rows are untouched. The empty service now offers four tiles, one row of 52px squares that stays centred.

### Fixed

- The template page and its **Use template** dialog now match the preview they were accepted on, and the choice block is one block: its options are drawn inside it, behind one rule with a dot at each option's place, each option a row of its own lines centred against its own controls, capped at three lines of title and two of meta, and the gap between two entries carries one add bar instead of one per option. Every title on the page reads in the entry heading — a choice's serif step is gone — with an option one size below it, and the media meta, the bait line, an option's meta and a choice's count share one meta style. A choice keeps every entry's labelled top-right controls, an option is icon-only and opens only under its own pointer. In the dialog, the rows name the picked option instead of listing every option, an option's file name and verses sit in the quiet column while its type and title stay in the row's ink, a chosen prayer keeps its title and its words apart, **Set** and **Choose** are the filled action and **Change** the outlined one, **Use template** is the page's filled button, the muted rows carry their kind marks and their media glyphs, the date reads in the picker's own long form, and the overlay, Escape and a reopen all behave: a click on the backdrop dismisses it, Escape closes the preview opened above it before the dialog, and a dismissed dialog opens blank again. Four faults behind the surface are fixed with it: the footer counted rows the dialog no longer had and said one entry was left with every row settled, a settled song's verses collapsed to the last of them so creating the service answered that the row was not settled, the confirmation drew its lines over the form instead of on a card of its own, and a file name with no spaces pushed the dialog into a sideways scroll. The sidebar no longer lists an option as a row of its own: a drag could take one out of its choice's block and leave the order numbering two rows under one entry.
- A PowerPoint shown on the projector now lands where the deck draws it. The companion's image carried only Liberation fonts, so Calibri — every table, heading and list in the worship decks — was drawn in Liberation Mono: the cover's title collapsed into a 300 × 275 px column where the deck draws 477 × 199, a schedule table's words moved up to 250 pt, and the offering page's two totals wrapped onto lines of their own and clipped the slide's edge. The converter now runs LibreOffice 25.2 and draws each family the decks name in its metric-compatible face; a build refuses a monospaced fallback; a deck converted by an older renderer is converted again on its next projection instead of serving the old PDF; and fonts that ship only with Office — Britannic Bold, Berlin Sans FB Demi — can be dropped into `~/.local/share/gkps-fonts` and are picked up when the companion restarts.
- Closing the file picker no longer closes the New media dialog: the form keeps its tab, its chosen file, its typed title and its Save button. The picker's own dismissal event was reaching the dialog's Escape handler; Escape on the dialog still closes it.
- Playing or pausing a preview with the space bar no longer draws a focus ring around the dialog. The body that holds focus for arrow-key scrolling was being marked as keyboard-focused by the key press, and in an audio or video preview that body is the whole dialog, so its 2px inset ring read as a border on the modal. The ring still appears for a reader who reaches the body with Tab, and a Tab brings it back after the shortcut has taken it away.
- A song entry now says `This song has no verses` when the picked song carries none, instead of `Pick a song first` — the line it shows when nothing is picked at all — and the field stays shut; a save refusal for that song reads `This song has no verses: pick another song.`, while clearing a song's own boxes still asks for one to be kept.
- The audio projector screen paints its play/pause control: the 48px circle was in the markup but 0×0, because its size and its two marks live in a stylesheet the page does not load. It now sits above the seek bar with a triangle while paused and two bars while playing, hides with the idle chrome — keeping its height so the bar does not move — and takes a click, which no longer spends its first press on fullscreen.
- An image on the projector no longer shows the unavailable-image glyph beside it: the placeholder now appears only when the bytes fail, and nothing is painted while they are still arriving, so the picture alone is centred — it sat 40px left of the middle on a 1920-wide display.
- An audio file's Preview reads its two times as one `current / total` pair now, right-aligned under the seek bar: the played time sits beside the total, 5px either side of a slash, with the total's right edge on the bar's. It used to stand 456.4px away at the bar's left end, and the line's own text was two numbers with nothing between them (`0:000:10`).
- The Media Library's list is drawn once on the page's first refresh again: that refresh wrote its service references before it had the companion's write token, the write was refused, and the list fell back to `Service uses unavailable` on every row until the next action. The token now arrives with the refresh that uses it, so the first draw carries the references.
- The Media Library's file list no longer jolts while it refreshes: every action that re-reads the local library — **Share online**, **Remove**, **Save setting** and the page's own first load — drew the list twice, the first pass without the services each file belongs to, so every row shrank and the list below the first row jumped up 22–68px and back within a frame or two. It is drawn once now, already carrying its service references, and a failed references read still says so in one pass.
- Every row of the Transfers dialog now keeps its icon column: a file name too long for the dialog used to pay for its own overflow by squeezing that 32px column down to the width of its glyph, so those rows' icons sat 5.5px and their names and status labels 11px left of every other row. The column is fixed at 32px and the name ends in an ellipsis inside the space the row reserves, from the 580px dialog down to the 382px one a 420px window gives.
- A Tata Ibadah service that is on air now offers the way back to its projector window: a square control beside **Stop projecting** reopens it on the screen that is on air — or brings an already-open window forward without loading it again — so closing the window no longer forces a release and a restart from the first screen, and a playing video is not restarted by the control that was meant to bring it forward. The control is drawn only while this page's service is the live one, never on a phone, and the group wraps inside a narrow pane rather than crossing its edge.
- The projector page adopts the service and screen the browser left on air again: an undeclared variable left behind when the offline library was removed made the hand-over stop before it painted, so a `/projector` window opened without a service — the way back to a closed projector — came up blank instead of on the screen that was on air.
- A long title or body now wraps inside its pane on every reading page instead of running past it — a 64-character service or song title, a Bible pericope heading or verse, a pasted link in a text entry, a search result and a Preview line — and the page no longer scrolls sideways; the rows that truncate on purpose, the sidebar's service and songbook rows, the media filenames and a contents row's three lines, still end `…`.
- A sidebar edit now reaches every visible reading view at once: renaming a Tata Ibadah, a songbook or a song updates its sidebar row, the stage that shows it, and any open search results and group counts in place — no reload, no reopened sidebar, and no stale result left beside a fresh one. The query, selection, sidebar pane states, filters, scroll and focus stay where they were, an edit made while another section's page is open leaves that page and its route alone, and a rejected save changes nothing.
- The reading sidebars' empty states are one block now — a glyph, a title and a hint, centred on the list's pane — instead of a sentence stranded in the pane's bottom-left, and they say which nothing they are: a list with no rows invites its first (`No sections yet.`, `No songs yet.`, `No songbooks yet.`, `No books yet.`), while a filter that matched nothing says so under a crossed-out magnifier (`No matching sections.`, `No matching songs.`, …) with `Try a different search.` beneath it. Both columns are covered, each naming its own list; the block is announced as a status, does not take the pointer or the wheel, is painted before the first keystroke on a page that arrives empty, is hidden in the collapsed panel and beside the Bible's chapter tiles, and is written the same way by the saved renderer — so an offline Kidung or Tata Ibadah page no longer borrows the Bible's copy.
- An empty service no longer leaves its invitation in the top third of a blank page: the block — heading, hint and tiles — has its centre a quarter of the way down the reading area the header leaves, not at its middle, and it clears the header at every width (measured 132.8px clear at 1440×900, 12px at the tightest). The header's and the body's own margins come off in this state only, so a service that holds items is untouched. The saved copy of the page and the rebuild that follows deleting the last entry paint the same row.
- A song page's header now names its songbook the way the rest of the app does — `PKJ 4` instead of `Pelengkap Kidung Jemaat 4` — and the browser tab follows it, so the header and the sidebar row beside it agree. The saved copy writes the same header for the same route. An ordinary songbook's page keeps its full name, and a hymn songbook with no short name still falls back to it.
- A hymn-book song opened from the reading sidebar no longer flashes the song sort control beside "Filter songs…": the saved copy now follows the server's rule and offers the control only for a songbook that is not a hymn book, so the song filter keeps its width while the page settles. An ordinary songbook's song page still offers it.
- A Tata Ibadah page's date header now reads as the same element as every other reading page's header — the shared size, weight, tracking, and colour a songbook header uses — instead of the 11px left behind when the media controls joined that row. When the stage is too narrow for both, the Project action wraps beneath the date rather than the date shrinking.
- Opening or moving between chapters of a Bible book whose TB and SIM book translations share a name (Rut, Ezra, Nehemia, …) through the reading sidebar keeps the verse text on the stage; the two edition blocks no longer collapse into one hidden block, so a reload is no longer needed.
- A media size now reads in the unit that still shows its number — `512 B`, `2 KB`, `12.3 KB`, `1 MB` — on the New media card, in a Media Library row and in the Media Library Total, drawn by one function; a file under 50 KB used to read `0.0 MB` on the card, one under 500 bytes read `0 KB` in the library, and the library rounded a 12,345-byte file to `12 KB`.
- The projector's empty-service notice no longer sits under a Go To passage or a song: it leaves the stage while a detour is shown — so the words take the full stage, 984px instead of 945.6 — returns when the detour closes, and hides itself when a re-read brings the service its first entries.

## [1.20.1] - 2026-10-21

### Fixed

- Saved Bible, Kidung, and Tata Ibadah pages now show the same route-specific sidebar labels, songbook references, song headings, and empty-service action icons as a direct load, including while offline.
- Saved song sort keys now trim the same leading number and spacing as the server's song list.

## [1.20.0] - 2026-10-20

### Added

- The operator dock at `/obs/dock`: pick a Tata Ibadah (grouped by month), browse its entries, and run it. Entry and screen rows project that screen, the keyboard steps screens, baits, or entries by unit, and the appearance control cycles dark, system, and light with the public site's own glyphs.
- One browser-local display state (`gkps-display`, channel `gkps-service-display`) shared by the dock, the projector, and the caption overlay. Opening any surface catches up to what is on air, tabs agree, and closing every surface keeps the display until it is released.
- The projector at `/projector` follows the dock and adopts `?service=<id>` in place — no navigation, no second window per service. Its screen lines balance their wrapped rows.
- The caption overlay at `/obs/source/overlay`: a control-free OBS browser source that captions the state's current screen in the bundled Source Sans 3 at the measured broadcast proportions. Media screens stay blank there in this slice.
- Bundled display typefaces: CMG Sans Bold and Source Sans 3 (with their licences) under `static/assets/fonts/`, so the surfaces no longer depend on machine installs.

### Changed

- The project button opens `/projector?service=<id>`; on a projecting service it becomes Stop project, which releases the display outright.
- Hide and release are distinct: hiding keeps the service and screen for a resume in place, and nothing ends the display but release.

### Removed

- The projector's heartbeat ("beat") and the shell's reaper, along with the "one Tata Ibadah per browser" step-aside.
- The per-service projector routes `/obs/service/<id>/`, `/lookup/`, and `/detour/` (no redirects; nothing was published to production on them).

## [1.19.2] - 2026-10-20

### Fixed

- Projector Go To checks the online Bible and song library when opened, so changed records appear in suggestions without a page reload while saved suggestions remain available on failed checks.

## [1.19.1] - 2026-10-20

### Fixed

- Online reading navigation now settles on current server rows and search results while retaining the saved fallback when the network fails. Saved Tata Ibadah services follow the server's same-day creation order.

## [1.19.0] - 2026-10-20

### Added

- PowerPoint PPT and PPTX entries can be previewed and projected one static slide at a time. The local companion verifies the original file, converts it with LibreOffice Impress into a private disposable PDF, and keeps the original file as the only Media Library identity. Missing or unreadable slides show a quiet unavailable state.

## [1.18.0] - 2026-10-19

### Added

- PDF entries can be previewed and projected one page at a time from verified local Media Library bytes. The dialog follows each page's size, projector navigation crosses PDF page boundaries within the service, and missing or unreadable files show a quiet unavailable state.

## [1.17.0] - 2026-10-19

### Added

- Audio entries play from verified local Media Library bytes in Tata Ibadah Preview and on the projector. The projector starts paused, supports Space to play or pause, and stops audio on navigation or display-off; unavailable files show a quiet missing state.
- Video entries can be previewed and projected from verified local Media Library bytes. Playback starts manually, requests fullscreen on the projector, returns to the normal view on pause, and stops on navigation; unavailable files show a Video-specific state.

## [1.16.0] - 2026-10-18

### Added

- Image entries can be previewed from Tata Ibadah and displayed directly on the projector from verified local Media Library bytes. Images fit without cropping; missing files have an operator message and a quiet projector icon.

## [1.15.1] - 2026-10-18

### Fixed

- Direct visits to Media Library now set the CSRF cookie required to share files online.

## [1.15.0] - 2026-10-18

### Added

- Media Library files can be temporarily shared through a private Cloudflare R2 bucket for seven days. The local companion owns direct uploads, verified downloads, transfer progress, and history across browser closure.
- Missing online media for today and future Tata Ibadah services downloads automatically with bounded retries; past services provide a manual download action.
- Media Library and Tata Ibadah show online and local availability, and files required by today or future services cannot be removed from the local library.
- Daily cleanup, an R2 configuration/smoke command, and setup guidance for the eight-day bucket lifecycle backstop.

## [1.14.6] - 2026-10-17

### Changed

- The Media Library connection row pairs Connected with a green check-circle and Unavailable with a neutral theme-muted minus icon.

## [1.14.5] - 2026-10-17

### Changed

- Tata Ibadah media entries have more vertical breathing room, with compact insets on narrow screens and long filenames wrapping within the row.

## [1.14.4] - 2026-10-17

### Fixed

- The Media Library sort control keeps its order icon when the selection changes, and the main sidebar uses a folder icon for mixed media. Tata Ibadah media titles align beside their file icons, while the upload hint separates supported formats from the emphasized 200 MB limit and groups PPT/PPTX.

## [1.14.3] - 2026-10-17

### Fixed

- Tata Ibadah media entries and add-media actions remain visible when a saved service opens
  through in-place navigation.

## [1.14.2] - 2026-10-17

### Fixed

- The New media source tabs use a sliding selection surface with reduced-motion support, and the
  Media Library sidebar highlight now follows main-menu selection and in-place page history.

## [1.14.1] - 2026-10-17

### Changed

- The Tata Ibadah New media modal keeps a consistent tall layout across its source tabs, presents a spacious empty Media Library state, and gives the inactive tab the same hover feedback as the app's other switches. The supported-files label now matches the size of its descriptive text.

## [1.14.0] - 2026-10-17

### Added

- A Docker Compose Media Library companion stores verified image, audio, video, PDF, and PowerPoint files in a named volume, shared by Chrome and the OBS dock on that computer.
- Tata Ibadah media entries keep immutable fingerprint references with optional titles. The service page shows a missing-file state, while media Preview and projector content remain blank in this first slice.
- The Media Library page lists local files and their service uses, offers type and unused filters, date and size sorting, local removal, and per-computer unused-file retention.

## [1.13.6] - 2026-10-17

### Changed

- The search page reads a query grammar: symbols separate words, `"quoted phrases"` match as one
  phrase, and `-word` excludes. Results rank by how many tokens they match, then by how many
  appear in the query's order, then by title; partial matches still list below full ones. The
  status line and page title show the purged query, a lone exclusion explains why it lists
  nothing, and the saved copy follows the same grammar. This replaces the score ladder spec 104
  introduced on the page; the field set and the projector Go To are unchanged.

## [1.13.5] - 2026-10-17

### Added

- Service entries are searchable: an entry-only Tata Ibadah is found by its own name, and each
  text entry by its title or body.

### Changed

- The public search page matches only the six listed fields — verse text and title, song title
  and lyrics, service name, row title, and text-entry body. Book and songbook names, Bible and
  songbook references, bare song numbers, dates, and row section labels no longer list anything;
  the saved copy follows the same field set. The page has its own matcher, so the projector Go To
  is untouched.

### Removed

- The home search hint line (`Try Yoh 3:16 or HAL 411`).

## [1.13.4] - 2026-10-17

### Fixed

- A dated Tata Ibadah opened from the sidebar keeps the date above its title; the saved-copy
  header previously read Tata Ibadah until a full page refresh.

## [1.13.3] - 2026-10-16

### Fixed

- The TB/SIM label on a passage opened through the projector's Go To brightens for about one
  second after the flip, matching a service passage cue.

## [1.13.2] - 2026-10-16

### Changed

- Bible book labels follow the active TB/SIM edition, including SIM abbreviations, Simalungun
  testament headings, and the visible translation's chapter title. Both editions' book codes work
  in sidebar, projector, and passage-picker searches; the three main rail popups use Bibel,
  Doding, and Agenda in SIM.

### Fixed

- Existing SIM translation rows receive abbreviations in place, and fresh Bible seeding stores the
  same 66 codes without replacing full names or verse links.

## [1.13.1] - 2026-10-16

### Fixed

- The Bible Version choice stays selected in the Bible sidebar and returns on a compatible Bible
  chapter after switching from Kidung or Tata Ibadah in the same tab. It still resets on refresh
  and remains isolated per tab.

## [1.13.0] - 2026-10-16

### Added

- Edit requests for songbooks, songs, Tata Ibadah, service entries, reorder, and custom screen
  breaks now share per-action progress and result toasts, with modal and duplicate-action guards
  while writes are pending.

### Fixed

- Service-entry deletion stays locked until its updated reading view is applied; a failed readback
  now reconciles the accepted deletion locally. In-page navigation patches changed reading and
  sidebar components while keeping unchanged nodes mounted.
- Sidebar and service-entry Add/Edit forms open a cancellable loading dialog immediately, ignore
  repeated opens, and discard late responses after dismissal.

## [1.12.0] - 2026-10-15

### Added

- The public reading app and service projector can open from saved browser shells and an offline library of Bible, songs, and Tata Ibadah data.
- The offline library syncs changed records in the background, exposes its status, and supports local Go To search in the projector.
- Reading navigation uses the saved shell and retains independent search history state per tab.

### Changed

- Bare-number projector Go To now cycles through every matching song number across hymn books, ordered by exact, prefix, then substring match.

## [1.11.0] - 2026-10-14

### Added

- The mirrored Tata Ibadah projector now has a quiet corner cue, entry list, shortcut sheet, keyboard and mouse navigation, and temporary passage or song detours.

### Changed

- Projected headers stay at the top while text fits the remaining stage; the HUD and pointer fade after inactivity and return on activity unless the HUD was deliberately hidden.

## [1.10.11] - 2026-10-14

### Fixed

- Selecting another Bible book from the mini sidebar keeps the book panel mini while opening that book's chapter list. The selected book can still toggle its chapters, and the expand control still opens the panel.

## [1.10.10] - 2026-10-13

### Fixed

- The Preview header's verse-tabs container is no longer named `preview__tabs-host`, whose name contains the `preview__tab` substring the "a single-verse song shows no tabs" test probes for. Rendering is unchanged; the served markup now says what it means.

## [1.10.9] - 2026-10-13

### Fixed

- Opening a Tata Ibadah service from the first-level panel brings its contents pane with it again. The sidebar state preserved on a stage-only swap is the first-level panel's (`data-nav`), not the contents pane's (`data-ch`) — a regression from 1.10.1.

## [1.10.8] - 2026-10-13

### Fixed

- The scrollbars no longer carry the platform's up/down buttons, and they are slimmer and softer: 5px instead of 6px, with a lighter thumb (and a still-clearly-stronger hover) in both themes. The root cause was the standard properties and the custom pseudo-elements both being set — in Blink the standard ones win, which reinstates the platform's 10px bar with its stepper buttons and ignores every `::-webkit-scrollbar` rule; they are now gated behind `@supports not selector(::-webkit-scrollbar)`.

## [1.10.7] - 2026-10-13

### Changed

- Modals (the entry form and the entry Preview) now separate from the page properly: a deeper scrim behind them, a lift of their own, and a hairline edge, so a dialog reads as a sheet above the page instead of a barely-different panel in it. The confirm layer inside the Preview follows the same scrim.

## [1.10.6] - 2026-10-13

### Added

- The entry Preview dialog names what it is showing: a Text entry's title, a passage's reference, or a song's heading, in a header that stays put while the body scrolls. A song's verse tabs move up beside the heading. An entry with no name still opens the headerless dialog it had before.

## [1.10.5] - 2026-10-13

### Changed

- The search-first home's helper line now reads "Try Yoh 3:16 or HAL 411"; both examples resolve against the corpus.

## [1.10.4] - 2026-10-13

### Changed

- The Bible translation switch (TB/SIM), in the reading header and in the passage picker, now fills the hovered option the way the Text screen-mode switch does, instead of only darkening its label.

## [1.10.3] - 2026-10-13

### Fixed

- The Tata Ibadah sidebar lists only the services of the mode it is showing: a dated order no longer appears under the templates (and the other way round) as a "Currently open" card. The open service is highlighted when it is in the list on screen.

## [1.10.2] - 2026-10-13

### Fixed

- The row being dragged in a Tata Ibadah's contents list now counts up with the order it is taking, instead of showing the number it had when it was picked up.

## [1.10.1] - 2026-10-13

### Fixed

- Opening a page from a second-level sidebar — and saving a service entry — keeps a collapsed or mini first sidebar as it was, instead of springing it open again.

## [1.10.0] - 2026-10-13

### Added

- Tata Ibadah uses one Text entry with Multi-line or Single-screen projection selected on Create and changed from Preview. Custom screen breaks stay editable in Preview, with confirmation before changing back to a default.

### Changed

- Existing Single-screen Text entries now use the unified Text kind while retaining their words, order, custom breaks, and projector screens.

## [1.9.4] - 2026-10-13

### Fixed

- Switching Tata Ibadah between dated orders and templates now keeps the open service and entry sidebar, with its exact service selected and visible in either list.

## [1.9.3] - 2026-10-13

### Fixed

- Switching reading menus now clears both sidebar filters and restores full lists while keeping the home search query.

## [1.9.2] - 2026-10-13

### Fixed

- Home search and both reading sidebar filters now use matching, centered clear controls with enough input space for typed text.

## [1.9.1] - 2026-10-13

### Fixed

- Tata Ibadah service-entry quicklinks can replay the stage flash after it finishes; activations during a flash no longer restart or queue another one.

## [1.9.0] - 2026-10-13

### Changed

- Mouse and pen reordering of Tata Ibadah service entries now starts from the entire sidebar row while preserving quicklink clicks, touch scrolling, and keyboard grip controls.

## [1.8.1] - 2026-10-13

### Fixed

- Song verse tabs in the Tata Ibadah Preview modal now keep equal 30 × 30px circular shapes for single- and double-digit numbers, with horizontal scrolling on narrow screens.

## [1.8.0] - 2026-10-13

### Added

- The first reading sidebar now collapses after 60 seconds without interaction when it matches the open reading page; Bible uses its mini sidebar state.

## [1.7.0] - 2026-10-13

### Added

- Tata Ibadah Text entry previews let editors place and remove projector screen breaks, with automatic two-line grouping until customized.
- Single-screen Text entry previews now use the same break controls, starting with one fitted screen and allowing custom screens across paragraph spacing.

## [1.6.8] - 2026-10-13

### Fixed

- Clicking text in a long Tata Ibadah Preview now lets arrow keys scroll its body without moving the page behind the dialog.

## [1.6.7] - 2026-10-13

### Changed

- Tata Ibadah service entries and section breaks use the approved quiet fill, inset outline, and 8px/8px/8px/12px padding in light and dark themes.

## [1.6.6] - 2026-10-12

### Changed

- Scrollbars in the public reading UI now use a slim, rounded, theme-aware style across pages, sidebars, dialogs, dropdowns, and text fields.

## [1.6.5] - 2026-10-12

### Fixed

- The Tata Ibadah date label now aligns vertically with the Project button without changing other reading headers.

## [1.6.4] - 2026-10-12

### Fixed

- Every song entry on the Tata Ibadah stage states the verses it keeps under its heading (`Bait 1-3`), not only when some verses are left out. The stage line now always matches the sidebar's second line, and a deleted song or verse still shows only its warning.

## [1.6.3] - 2026-10-12

### Fixed

- A Tata Ibadah entry keeps its highlight and its Preview, Edit, and Delete controls while a modal opened from it is showing, so it stays clear which entry the modal is about. The highlight clears only after the modal closes.

## [1.6.2] - 2026-10-12

### Changed

- The public reading rail uses one theme button again. It cycles System, Dark, and Light, with the icon and tooltip showing the selected mode.

## [1.6.1] - 2026-10-12

### Changed

- Entry numbers in the Tata Ibadah contents list sit at the vertical middle of their row, so multi-line entries (a quoted text, or a song with its verse line) read with an even numbering column. Text position, row size, and the songbook song list are unchanged.

## [1.6.0] - 2026-10-12

### Added

- The public reading theme control now offers Light, Dark, and System. System is the default for readers without a saved preference and follows changes to the device theme while the page is open.

## [1.5.1] - 2026-10-12

### Fixed

- Service entries clear their highlight and floating controls after pointer-opened Preview, Edit, or Delete modals close with the pointer elsewhere. Real hover, visible keyboard focus, and touch controls remain available.

### Changed

- Tata Ibadah song rows now distinguish the hymn reference, song title, and selected verses with separate typography. Long titles wrap above the verse line, and dark mode keeps the smaller verse label at readable contrast.

## [1.5.0] - 2026-10-12

### Added

- Liturgy lines in a Tata Ibadah are colored by who speaks them, on the projector, on the reading page in both themes, and in the entry preview. The screen faces the congregation, so their own lines keep the ordinary off-white. A leader line (`L`, `P`, Liturgis, Paragenda, Pendeta, Pdt, Pelayan, Pemimpin, Parambilan) is a quieter warm cue (`#9C8463` on the screen, `#866B50` on the light page). A joined line (`P+K`, `L+J`, `P/J`, `PJ`, and the same joins) is a readable teal (`#8EC2CC`, light `#2B5A64`) that marks it as theirs to say. A line with no speaker keeps the previous voice within the same entry, even onto the next screen. Songs and scripture are unchanged.

### Changed

- The reading page now lifts colon speaker marks (`Paragenda:`, `Jemaat:`, `P+J:`) as well as `L.`/`P.`/`J.`, and shows each mark the way it was written.

## [1.4.0] - 2026-10-12

### Added

- The service projector rests on a blank screen after every content entry, and after every verse of a song. That blank is not a section break, so it is not a row in the order.

## [1.3.23] - 2026-10-11

### Fixed

- The single-screen text editor's Save button now follows its Text field: the client guard attached to the text form alone, so a filled single-screen field kept the button disabled until the next page load. Both text kinds share the guard now, and an empty or whitespace-only field still disables it.
- A section break no longer offers an Edit control, on the stage or in the sidebar — a break has nothing to fill in. Its Delete stays, and every other kind keeps its Edit.

### Changed

- "+ Break" adds the break at once, at its add row's position (or the end of the service from the empty-state button), instead of opening a form with no fields.
- Song entries in the Tata Ibadah sidebar now state the verses they keep on a second line (`Bait 1-3, 5, 6, 8-10`). The stage's `Bait` line uses the same run-collapsing format: three or more consecutive numbers become a range, pairs and singles stay comma-separated.

## [1.3.22] - 2026-10-11

### Changed

- Each Tata Ibadah entry is now a box that contains its floating Preview / Edit / Delete controls — at least 52px tall, its words centred on the box's centreline — replacing the 44px top band. The start bar collapses at rest and reveals with the first block like every other add row, a revealed row keeps equal 8px above and below its buttons in every state, consecutive entries sit on a uniform 12px rhythm, and the section break takes the same box with its rule centred.

## [1.3.21] - 2026-10-11

### Fixed

- The Tata Ibadah stage's entry-title links wear the theme's link colour — forest green `#1C5C3C` in light, lifted royal blue `#7C9CF0` in dark — instead of the browser's default blue, which dropped to 1.98:1 contrast on the dark canvas. The underline stays, and no other link changes.

## [1.3.20] - 2026-10-10

### Changed

- A Tata Ibadah song entry from a hymn book now reads by its short reference and title on the stage and in its preview modal (`HAL 3 — Sai puji Naibata`), like the section sidebar and the pickers; other songs keep their headings.
- A song entry that keeps only some of its song's verses now states them under its heading (`Bait 1, 3`); a full selection shows nothing.

## [1.3.19] - 2026-10-10

### Changed

- Each Tata Ibadah entry now owns the height of its Preview / Edit / Delete controls: a quiet 44px band at the top of the entry holds them, so the title or first line of text always starts below them instead of under them. The section break is unchanged.

## [1.3.18] - 2026-10-10

### Changed

- The Tata Ibadah pane's hidden add rows no longer reserve space: at rest entries sit as close together as with the editors off, and the `+ Passage / + Song / …` row expands in place when its entry is hovered or focused (touch devices see the rows outright). The section break keeps its rule with tighter margins (34px → 16px).

## [1.3.17] - 2026-10-10

### Fixed

- The New song picker searches hymn songbook short/full names and their substrings alongside song titles: `kj`, `kidu`, `maat`, and `kidung jemaat` list songs from matching hymn books within the existing 200-option cap; non-hymn book names remain title-only matches.
- The New song picker resolves a combined book-and-number-prefix reference, with an optional sub-number letter and trailing title: `kj 12` includes KJ/PKJ numbers 12 and 123 (plus sub-number variants), while `kj 12a` selects only that base number/sub-number.

## [1.3.16] - 2026-10-09

### Fixed

- The New song picker now searches songbook abbreviations, and selected hymn labels retain the short reference.

## [1.3.15] - 2026-10-09

### Fixed

- The passage editor now centers TB/SIM above the Book picker and keeps Chapter and verse pickers inside the modal at narrow widths.

## [1.3.14] - 2026-10-09

### Fixed

- Passage book picker search now hides non-matching books while matching both TB and SIM names.

## [1.3.13] - 2026-10-09

### Changed

- Untitled service-entry Text and Single-Screen Text sidebar labels now show up to the first two literal body lines, preserving blank lines, titles and the 60-character cap; the reorder grip stays centered on two-line rows.

## [1.3.12] - 2026-10-09

### Changed

- Replace the passage add/edit modal's chapter and verse selects with custom pickers, preserving dynamic options, submitted values and the disabled to-verse tip.

## [1.3.11] - 2026-10-09

### Added

- Add an in-place TB/SIM toggle to the passage-book picker; switching updates the selected translation without reloading chapter or verse controls.

## [1.3.10] - 2026-10-09

### Changed

- The add-song picker lists hymn books first by book id and in song-number order, then other songbooks by name and title order; hymn options show the short reference and title, unnumbered hymns follow by title, and the closed selection remains title-only.

## [1.3.9] - 2026-10-08

### Changed

- Passage book options now list each book once with the TB name primary and SIM name dimmed on the right; selecting stores the primary translation, filtering matches either name, and editing a saved passage preserves its current translation until another book is chosen.

## [1.3.8] - 2026-10-08

### Fixed

- The entry modal's book and song menus are capped to the viewport rather than the dialog: they may overlap the dialog's edge, never leave the window, flip up when there is no room below, and stay anchored while the dialog scrolls.

## [1.3.7] - 2026-10-08

### Changed

- In the Tata Ibadah sidebar a hymn song reads as its short reference and title (e.g. `KJ 435 Marolopolop Tondingki`); other songbooks keep their label.

## [1.3.6] - 2026-10-08

### Changed

- A section-break entry no longer has a label: the editor offers no label field and the divider shows none. A text entry keeps its title and a legacy end-of-section row keeps its note.

## [1.3.5] - 2026-10-08

### Changed

- Hovering (or focusing) an entry reveals the add row above it and the add row below it, so either side can be inserted into.

## [1.3.4] - 2026-10-08

### Fixed

- Hovering an item's add row no longer counts as hovering the item above: the row starts below the item, so the item is not highlighted and its controls stay hidden.

## [1.3.3] - 2026-10-08

### Changed

- A section break draws one clear full-width divider, the same for a legacy end-of-section row and a section_break entry, with its note beneath it.

## [1.3.2] - 2026-10-08

### Changed

- Hovering a service entry highlights the whole item with the shared hover tint, without moving the text.

## [1.3.1] - 2026-10-08

### Changed

- An entry's controls (preview, Edit, Delete) float at its top-right over the text on a brief backing, shown while the item is hovered or holds keyboard focus.

## [1.3.0] - 2026-10-08

### Added

- A read-only preview for a service entry: a headerless modal with the full text or passage, or a song's selected verses in numbered tabs, dismissed by Esc or a click on the overlay.

## [1.2.2] - 2026-10-08

### Changed

- A text entry's pane shows only its first three lines, hard-truncated with an ellipsis; the hidden remainder is marked so the preview can be offered.

## [1.2.1] - 2026-10-08

### Fixed

- The "add at the beginning" start bar gets its own markup, so it no longer collides with the per-item add controls.

## [1.2.0] - 2026-10-08

### Added

- Add a service entry at the beginning of a Tata Ibadah: a start bar above the first row inserts at order 1, shifting entries and legacy rows together.

## [1.1.0] - 2026-10-08

### Added

- A **Single-Screen Text** service entry kind: the whole body on one projector screen, the font shrinking to fit and only ellipsizing when it cannot shrink further.

## [1.0.2] - 2026-10-08

### Removed

- The projection pane no longer shows the **Update the current state** control; saved changes still reach the display on their own.

## [1.0.1] - 2026-10-08

### Removed

- The projection controls no longer print a status line beneath them; Update and the automatic stop-when-the-window-closes keep working without narrating.

## [1.0.0] - 2026-10-08

### Added

- Tata Ibadah forms use an accessible calendar popover with a default upcoming Sunday, keyboard selection, and a clear action.

### Changed

- **Breaking:** Songbooks no longer have a language field in their model, forms, or API responses. Same-name books are merged, their song references preserved, and names are globally unique.
- Tata Ibadah forms no longer expose first-section or active controls; new services start active and empty, while edits preserve activation.
- Dated Tata Ibadah headers show full Indonesian month names.
- Project and Stop projecting buttons use primary and danger treatments respectively.
- Resetting the reading home clears remembered search while ordinary sidebar browsing preserves it.
- The date picker shows a full, theme-aware Sunday emphasis and square date cells with rounded corners.
- The projection lock is removed: a Tata Ibadah's entries can be added, edited, deleted and reordered while it is being projected, from any tab of the projecting browser.
- A reorder is written as soon as it is dropped, or a keyboard move settles; the Save/Discard strip and the unsaved-order leave prompt are gone.
- The projector follows every saved change: an add, edit, delete or reorder makes the open display re-read by itself, without pressing Update the current state.

### Fixed

- Pointer-closing reading editors no longer leaves stale edit controls visible; automatic modal focus restoration no longer leaves row outlines or idle actions visible, while deliberate keyboard focus indicators remain visible.
- The Tata Ibadah date picker stays anchored above scrollable modal content and within the viewport.

## [0.11.4] - 2026-10-06

### Changed

- Songbook forms hide short name and hymn-book fields; edits preserve existing values, and new songbooks use model defaults.

## [0.11.3] - 2026-10-06

### Fixed

- Public hymn-book song lists now sort numerically by song number and case-insensitively
  by sub-number, with unnumbered legacy songs listed last.

## [0.11.2] - 2026-10-06

### Changed

- Light-theme selected reading-sidebar tint is now pale mint `#B9D7C9` for stronger near-black
  text contrast; dark-theme selection remains unchanged.

## [0.11.1] - 2026-10-06

### Changed

- Softer theme-aware selected-row tint for Bible books and chapters, songbooks, songs,
  and Tata Ibadah services; selected text remains readable in both themes.

## [0.11.0] - 2026-10-06

### Added

- The Tata Ibadah reading pane can edit or delete existing `TataIbadahItem` text and
  end-of-section rows in the shared editor dialog; the old OBS dock sees the same edits.

### Changed

- Old rows and new service entries share a contiguous running order. Existing services
  retain their visible order during migration; adding after either kind and deleting a row
  shift both kinds together. The pane, contents list, and service projector follow it.
- Existing entry reorder keeps old rows in their positions and repairs the shared order
  after a legacy API reorder. Old OBS pages, API routes, and response shapes stay in place.

## [0.10.0] - 2026-10-06

### Added

- Service entries let one Tata Ibadah hold text, scripture, song, and section-break items in
  one ordered list, with add/edit/delete controls in its reading pane.
- A separate service projector at `/obs/service/<id>/` displays the running order and keeps
  its browser-local display state separate from the existing OBS docks and sources.
- The Bible TB/SIM selector now has a persistent selected state and a transform-only moving
  highlight, synchronized on initial load and in-place reading navigation.

### Changed

- Service-entry reorder remains a draft until Save or Discard, and warns before a navigation
  can discard unsaved changes. The existing `TataIbadahItem` rows and API remain compatible.
- Songs, songbooks, and verses are soft-deleted: ordinary browse/search/API paths hide deleted
  targets, saved service entries retain their references and show a warning, and admin deletion
  records the actor and time without removing rows.
- Existing bookmark and song API payloads do not expose soft-delete metadata; writes and reorder
  reject deleted targets.

## [0.9.0] - 2026-10-03

### Added

- Sidebar editors (spec 005): a full-width accent add button below the filter in the
  songbook, song and Tata Ibadah sidebars, and a hover/focus-revealed edit control on every
  row of those lists. Each opens a modal — a native `<dialog>` in the reading design — that
  creates or edits the record through a server-rendered form, refreshes the page's regions
  in place on save, and shows validation errors beside their fields without closing.
- Songbook fields: name, short name, language, hymn flag. Song fields: number, sub-number,
  title, key — with the number required for a hymn. Tata Ibadah fields: name, date, active,
  plus an optional first section on create, because a service used to appear in the public
  lists only once it had one. (Since spec 006 every active service is listed, empty ones
  included, so an empty service can be opened and filled; its page says it is empty.)
- `SIDEBAR_EDITORS_REQUIRE_LOGIN` (default off): set it true to hide every editor control
  from anonymous visitors and refuse their writes with 403, without touching the UI code.

### Changed

- Hymn songbooks and the songs inside them are read-only: they render no edit control at
  all, checked against the data rather than a list of names, and their write endpoints
  refuse the request even when it is hand-crafted. That now includes *adding* a song: a
  hymn book shows no add button, and a hand-crafted create is refused like any other
  hymn-book write (found in review, where the create path had been left open).
- The forms mirror the models' own rules, so a duplicate short name, a duplicate
  `(book, number, sub_number)` and a numberless hymn are refused server-side; CSRF is
  required on every write.
- Song lists sort *last modified* (newest first, the file's own order breaking a tie) or
  *alphabetically*, whose key ignores a title's own leading `435. `. Without that, the two
  orders would be identical: every song in the corpus imports with one `modified` timestamp,
  so all rows tie and the alphabetical order is what the list already shows. The song list's
  add button also moved out of the toolbar to a full-width row below the filter, so the sort
  control keeps the place it has in the accepted mockup.
- Hovering a row's edit control no longer drops the row's hover styling, and the control
  carries a pointer cursor like the rest of the row.
- Escape inside an editor's modal closes only the modal: the page's own Escape handling
  looked through it and closed the sidebar behind it too.
- The Tata Ibadah mode toggle works when it is reached by clicking through from the home. Its
  link was relative (`?mode=template`), which only resolves on `/tatib/`; swapped into the home
  it became `/home/?mode=template` -- the search home -- so the panel closed and Alkitab
  appeared. It is absolute now, and it is synced (or removed) with its section, so it keeps the
  slot the mockup gives it instead of leaving the collapse there.
- Closing a sidebar no longer reveals a row's edit control: the row link kept focus, and
  `:focus-within` counted as hover.
- A rail tile's label no longer appears when a sidebar closes. Closing the panel returns focus
  to its tile on purpose (that is the focus management, and it is right), but the label was
  raised by *any* focus; it now answers keyboard focus only, via `:focus-visible`. Any tooltip
  still up when a sidebar's state changes is cleared at the transition.
- The add buttons are inserted from the page that arrives when the shell swaps a section in
  place. They sit outside the swapped regions, and the search-first home has no such button
  to update, so they used to be missing for anyone who landed on the home and clicked through
  to a section -- the path the site is designed around. Regression-tested on that path.

### Security

- **Accepted risk (owner decision, 2026-10-03): anyone may write through these forms.** The
  corpus of a publicly reachable deployment is editable by anyone who can reach it. The
  login hook above is the documented mitigation and the first thing to switch on before the
  site is exposed beyond the team.

## [0.8.0] - 2026-10-03

### Added

- Search-first public site: an icon rail (Search, Alkitab, Kidung, Tata Ibadah, theme
  toggle) and a landing page whose search spans the whole corpus — Bible books,
  references, and verse text; songbooks, titles, and lyrics; Tata Ibadah titles and
  public contents — with grouped results, counts, excerpts, and exact reference
  resolution (`Matius 5:13`, `Kidung Jemaat 120` ≡ `KJ 120`).
- Public reading views for Bible chapters (verse numbers, TB/SIM translation toggle) and
  Tata Ibadah service orders (year+month groups, Templates view, section quicklinks).
- Song-list sort control on non-hymn songbooks — *recently updated* (default, by a new
  `Song.modified` stamp; migration 0012) ↔ *alphabetical* — applied in place.
- Dark mode by rail toggle, persisted and applied before first paint, with the palette
  AA-safe in light and dark.

### Changed

- Public pages rebuilt on the design language from spec 001: hand-written CSS with no
  framework, a narrow rail with nested sidebars (mini collapse for Bible, wide song list
  for Kidung), keyboard/touch ergonomics, and print that yields reading content only.
- The shell now navigates in place: rail destinations, sidebar picks, search submits,
  result opens and *Show more* swap the affected regions under one URL, so panel
  animations play and the address bar never changes. Switching sections keeps the reading
  stage and returning rebuilds that section's lists from it.
- Sidebar clicks no longer scroll their lists: a row clipped at an edge is nudged only
  enough to become fully visible, and only reveals (opening the sidebar on the page being
  read, or opening a search result) centre a row.
- Reveals do that consistently now: the panel tile and the list row are both centred for
  every section — Tata Ibadah services included, whose rows were never revealed before — and
  the travel is animated so the rows before the target are seen. A Tata Ibadah contents item
  is flashed rather than selected, since quicklinks never carry a current state.
- The rail search icon only ever restores a real result set: a stored URL that is not one (an
  older build could leave a reading page there) is discarded instead of being opened.
- The brand logo now takes the same route as the search icon — back to the last result set
  rather than starting a fresh search.
- Every search and filter field has a clear (×) control, shown while the field holds a value;
  clearing re-runs the filter (or keeps the result set) and returns focus to the field.
- The last result set survives browsing away through the sidebars, and returning to it
  resumes the scroll offset it was left at.
- Search behaviors: any non-empty query searches — the minimum length and its inline
  message are gone — an empty submit is inert and keeps the last result set; the rail
  search icon restores the last result set, the logo starts a fresh search.

## [0.7.0] - 2026-10-01

### Added

- Maintenance mode (`MAINTENANCE_MODE`): the site root `/` serves a short notice
  (HTTP 503) while the reading home stays reachable at `/home/`.
- `[devops]` Local Docker Compose stack (`web` + `db`) on low-conflict ports
  from the IANA dynamic range, overridable via `WEB_PORT` / `DB_PORT` in `.env`.
  Container-internal ports stay conventional (`8000` / `5432`).

### Changed

- The public home moved from `/` to `/home/` while maintenance is on; `/` serves
  the home again when `MAINTENANCE_MODE` is off.

## [0.6.0] - 2026-09-30

### Added

- Public song-reading site at `/`: browse songbooks, read a song's lyrics, search by title or
  book number.
- A design language defined from scratch (`static/styles/design/`), with a palette drawn from
  the GKPS logo; public pages no longer depend on Fomantic UI.

### Changed

- The content editor moved from `/songs/…` to `/manage/…`; legacy paths redirect (301).
