# Tasks 006: Service entries

- **Status:** Accepted (owner, 2026-10-03)
- **Spec:** [./spec.md](./spec.md) · **Plan:** [./plan.md](./plan.md)

## Before starting

- [x] Spec Accepted by the project owner (2026-10-03)
- [x] The open questions in ./spec.md answered (model name, control surface, stack, URLs)
- [x] Branch from the current base (`feat/006-service-entries`)
- [x] Confirm the compatibility promise's regression pass exists before touching anything —
      `multimedia/web/tests.py` pins that a service with no entries renders exactly as before

## Slice 1 — the model  (done)

- [x] Red: field rules per kind; at least one verse kept; `resolve()` per kind; ordering
      (`multimedia/tatib/tests.py`, `ServiceEntryTests`)
- [x] Green: `tatib.ServiceEntry` + migration `0005_serviceentry` + admin; `TataIbadahItem`
      untouched
- [x] The book/chapter cascade reset to 1 is a form/UI rule: slice 2
- [x] Verified: 130 tests green, the 116 that existed before among them, with no edit to any
      current template, endpoint or model

## Slice 2 — the content pane  (done)

- [x] Red: create/update/delete endpoints per kind; validation errors; what the pickers need
      (`ServiceEntryViewTests`, 17 tests, red before the wiring existed)
- [x] Green: the per-kind forms (`multimedia/web/reading/entries.py`), the six endpoint views,
      their URLs, and the two fragments (`_entry_form.html`, `_entry_song_options.html`)
- [x] Two bugs the tests caught: `editor/<str:kind>/new/` was swallowing `editor/entry/new/`
      (the entry routes must come first), and a second `kind` input shadowed the form's own,
      making every create invalid
- [x] The pane's rendering: a service's entries appear in its stage after its legacy items, in
      its contents list, with a jump control on a passage or a song, and four add controls on
      every item — revealed on hover, and an entry also carries its own **edit** and **delete**
- [x] An empty service shows a centred invitation instead: the message, and the four kinds as
      wide buttons with their icons left of the labels, stacked down the page
- [x] Every active service is listed in the sidebar, empty ones included, so an empty service can
      be opened and filled (the old rule kept only services with a legacy text item)
- [x] Additive: a service with no entries renders exactly as it did before, which one test pins
- [x] A new entry can be inserted behind the item whose control was used (`after`), shifting the
      rest -- the liturgy is built in place, not appended
- [x] The modals' behaviour in the browser: opening the fragment, submitting it, the cascading
      book -> chapter -> verse resets, the song pick's search, and the verse checklist's label
      (`static/web/entries.js`, and the styles for the new controls)
- [x] E2E: each modal, the cascading dropdowns, the verse checklist's label, the panes
      refreshing in place — `tests/e2e/test_entries.py` (10 tests, green)
- [x] The owner's review round of 2026-10-04: each picker's own filter inside the dropdown, books
      grouped by testament, the to-verse list hiding what cannot end a range (disabled, with its
      hover note), the verse checklist inside a dropdown labelled by what is included and shut for
      a one-verse song, the optional-header hints, the empty-text Save guard, the danger-coloured
      Delete with icons, and no x-close on the modal
- [x] Two defects the browser run found and fixed: a slow preload overwriting a newer search answer
      (a stale-response guard), and menus clipped by the modal's own scroll box (each menu is now
      capped to the room its trigger has, opening upward when that side is larger)

## Slice 3 — reorder  (done)

- [x] Red: the endpoint's own rules (`ServiceEntryReorderTests`, 9) and the pane's chrome
      (`ServiceReorderPaneTests`, 4), plus `tests/e2e/test_reorder.py` (7) -- red as a page of
      NoReverseMatch and missing markup before the wiring landed
- [x] Green: `entry_reorder` (one POST of {entry, order_number} pairs, answering with the order
      it left, following the current item API's shape), the toolbar and per-entry handle in
      `reading/tatib.html`, the styles, and `static/web/reorder.js`
- [x] Drag with pointer events, and arrow buttons for the keyboard (focus stays on the same
      arrow so a run of presses works); the grip is decoration, the whole entry is a handle
- [x] The pending order previewed at once in the pane AND in the sidebar's contents list, whose
      own numbers are renumbered to match; Discard restores both
- [x] Leaving with an unsaved order asks first: the shell's in-page navigation hands over
      (`navigate()`, reading.js) and `beforeunload` covers a tab close. Keep editing / Discard /
      Save, and Save carries the person on to where they were going
- [x] The CSRF cookie the JSON POST needs: `ensure_csrf_cookie` on the Tata Ibadah view (there is
      no form on the page to render a token)
- [x] Two defects the browser run found: the mode's state attribute sat on the toolbar, which is
      the entries' SIBLING, so no selector could reach them (it is on the pane now), and the
      dialog's buttons reused the entry modal's `.editor__save` / `.editor__cancel` classes,
      which made the entry tests' selectors ambiguous -- they have their own names, drawing the
      same geometry
- [x] Verified: 113 in `multimedia/web/tests.py`, 17 e2e for the entries and the reorder, and the
      live page measured (the adds go, three arrows appear, the arrow moves the entry, the
      sidebar follows and renumbers, Discard restores, the question shows and closes)

## Accepted amendment to slice 3 — pointer-following ghost (owner, 2026-10-04)

- [x] Red browser test: after threshold, a visual copy follows pointer deltas with no lag;
      it is inert/aria-hidden outside `#chList`, with no extra active handle, link, or id
- [x] Red browser test: the real row remains one invisible layout slot while the list height
      stays constant, the other rows morph, and release keeps the previewed order
- [x] Red browser test: pointer cancellation restores the pre-gesture order without losing
      earlier unsaved moves; release/cancel/blur/page swap leaves no visual copy
- [x] Red browser test: section breaks have the same preview and keyboard moves are unchanged
- [x] Green: implement the pointer-following preview and its cleanup in `static/web/reorder.js`
      and `static/styles/design/components.css`; 14 targeted reorder e2e and 119 app/token tests pass

## Accepted amendment to slice 3 — suppress hover while grabbing (owner, 2026-10-05)

- [x] Red browser test: normal hover before drag, no hover background on entry rows or ghost
      while actively grabbed, selected style unchanged, normal hover restored on release/cancel
- [x] Green: scope hover suppression to active pointer drag, preserve focus and keyboard moves;
      15 targeted reorder browser tests passed; confirm served CSS

## Accepted amendment — empty Bible header row (owner, 2026-10-05)

- [x] Red browser test: from home to a Bible chapter, empty header row has zero height and
      title/TB-SIM move up by 34px at desktop and phone widths; song citation and Tata Ibadah
      date/project button remain visible with their intentional spacing (failed at 34px)
- [x] Green: collapse the empty `.read__head-top` in `components.css`, keep the stage's
      40px top padding and selected title/control layout; populated rows retain their height
- [x] Two targeted reader browser tests passed; collectstatic --clear completed and served CSS confirmed

## Accepted amendment — visible destination slot (owner, 2026-10-05)

- [x] Red browser test: the existing dragged row's slot highlights at its live destination
      (first, middle, last, and across section breaks) without extra rows or list height;
      ghost follows the pointer, hover/selection/focus and keyboard moves stay intact
- [x] Green: style the existing row as a destination slot without duplicating its content;
      release, cancel, blur, and page swap clear the highlight
- [x] 16 targeted reorder browser tests passed; static assets collected and served CSS confirmed

## Accepted amendment — remove the destination slot ring (owner, 2026-10-05)

- [x] Red: assert the tinted destination slot has no computed outline or box shadow
- [x] Green: remove only the slot's inset ring, preserving ghost and focus styles
- [x] 16 targeted reorder browser tests passed; static assets collected and served CSS confirmed

## Accepted amendment — Bible language switch motion (owner, 2026-10-05)

- [x] Red: browser test the TB/SIM highlight's mid- and end-travel in both directions,
      translation and pressed state, header geometry, unavailable choice, reduced motion
- [x] Green: persistent selected background with transform-only travel and initial-state
      synchronization; retain links, keyboard focus, and no-JS navigation
- [x] Targeted reading browser tests: all 4 language-switch E2E tests passed; collectstatic and
      live home-to-reader path verified, including the saved SIM edition restoring without travel

## Slice 4 — the new display and display mode  (done, bar the deferred overlay)

- [x] Red: each kind rendered on the new projector; the body's own two lines; the blank-line
      pause; prev/next/toggle (`multimedia/web/tests.py`, `ServiceProjectorTests`, red before the
      page existed)
- [x] Red: entry writes refused while the Tata Ibadah is displaying in this browser, in its other
      tabs too, while the Tata Ibadah's own fields stay writable; one Tata Ibadah at a time in this
      browser; a second browser unaffected (`tests/e2e/test_projector.py`)
- [x] Red: the project button becomes Stop projecting and Update the current state; Update
      re-reads what is on screen — a lyric edit reaches a fresh projection
      (`test_a_lyric_change_reaches_a_fresh_projection`)
- [x] Green: the display state in the browser on its own channel (`static/web/display.js`), the
      projector page on the reading app's tokens (`reading/projector.html`,
      `static/styles/design/projector.css`, `static/web/projector.js`), the project group
      (`reading/tatib.html`), the decline in `static/web/entries.js`, and the endpoints untouched:
      the lock is the shell refusing, exactly as the compatibility promise requires
- [x] e2e: a whole service driven through the new projector, the two-tab lock, a second browser
      left alone, and Update keeping its place (4 tests)
- [x] The display's own round (owner, 2026-10-04): only the header and the words, white on black in
      the current projector's face, one verse a screen for a passage, two lines at a time for texts
      and songs, a break showing nothing, the keyboard instead of controls, the project button with
      its icon in line with the date, and the pane carrying only the reference
      (`ServiceProjectorTests`, 11; `tests/e2e/test_projector.py`, 7)
- [x] The display's colours, centring and morphs (owner, 2026-10-04): the product's dark palette
      with the accent for the header, the projector-then-Source-Sans face stack, the ink centred on
      both axes, short arrive/leave morphs and a fade on the toggle, and reduced motion respected
      (`tests/e2e/test_projector.py`, 10)
- [x] The header brighter still (the display's own warm gold, sent back as too close to the words
      when it was the app's accent), and the fitting brought down until the words fit the screen --
      measured on the ink, floored at the current projector's 2px, so a body longer than the screen
      is never cut off (`tests/e2e/test_projector.py`, 11)
- [x] The words' own lines get a little air between them (0.45em, in the fitted size), and closing
      the projector window ends the display by itself -- the opener's handle at once, the projector's
      beat for every other tab -- releasing the write lock everywhere (`tests/e2e/test_projector.py`,
      14)
- [ ] Deferred, per the plan: the OBS overlay, which needs its own answer for reaching inside OBS.
      The projector window is the whole of this version's display.

## Slice 5 — soft deletion

- [x] Red: deletion marks rather than removes; normal lists and the current dock/API paths skip a
      deleted row; a service entry referring to a deleted song still resolves and warns
- [x] Green: the flag on Song, Book and Verse, the admin path, the warning on the entry
- [x] Audit every current query site for songs, songbooks and verses — the compatibility pass
      before and after; the 162-test app/API regression pass is green

## The compatibility promise

- [x] A regression pass asserting the current OBS page paths render, the legacy Tata Ibadah list,
      item list and reorder routes keep their response shape, and songs/bookmarks APIs keep their
      response fields; app/API regression pass green
- [x] No diff in any current OBS template, script or endpoint

## Done when

- [x] All acceptance scenarios in ./spec.md hold; the overlay remains explicitly deferred
- [x] The tests named above are green, and the compatibility pass is green
- [x] Traceability in ./spec.md filled
- [x] Final verification: Django system check, migration consistency check, and the complete
      suite passed (270 tests)
- [x] ITEM and board, `VERSION` 0.10.0, and the changelog entry included together in draft PR #263
