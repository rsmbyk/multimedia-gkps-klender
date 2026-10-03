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

## Slice 3 — reorder

- [ ] Red: drag and keyboard moves; the sidebar preview; Discard restoring; adds hidden; the leave
      guard on every exit path (contents, another Tata Ibadah, search, tab close)
- [ ] Green: reorder mode, Save/Discard, the confirmation modal, the reorder endpoint

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
- [ ] Deferred, per the plan: the OBS overlay, which needs its own answer for reaching inside OBS.
      The projector window is the whole of this version's display.

## Slice 5 — soft deletion

- [ ] Red: deletion marks rather than removes; normal lists and the current dock/API paths skip a
      deleted row; a service entry referring to a deleted song still resolves and warns
- [ ] Green: the flag on Song, Book and Verse, the admin path, the warning on the entry
- [ ] Audit every current query site for songs, songbooks and verses — the compatibility pass
      before and after

## The compatibility promise

- [ ] A regression pass asserting the current OBS pages, API endpoints and model responses are
      unchanged, run before and after
- [ ] No diff in any current OBS template, script or endpoint

## Done when

- [ ] All acceptance scenarios in ./spec.md hold
- [ ] The tests named above are green, and the compatibility pass is green
- [ ] Traceability in ./spec.md filled; ITEM and board updated in the same PR
- [ ] `VERSION` and the changelog bumped in the same PR
