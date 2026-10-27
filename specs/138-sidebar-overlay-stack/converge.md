# Converge: on a small screen the sidebars are a drawer stack over the page

**Slice**: `specs/138-sidebar-overlay-stack` · **Date**: 2026-10-27
**Method**: the nine spec rows read against the code as built, then each finding proved or refuted
with a run. Four checks, no acceptance row: the harness rewrote nine times before the suite went
green, and every rewrite is a finding about either the spec's wording or the code's assumption.

## Checks

- **S1 Security** — clean: no new endpoint, no payload, no credential; the toolbar and backdrop are
  markup with no data.
- **S2 Architecture** — clean after C4: one media query owns the layout, one attribute pair owns the
  state, and no second layout exists to drift.
- **S3 Ops** — clean: `collectstatic` and a restart are all the deploy adds; the stylesheet is one
  block appended to the file the deploy already ships.
- **S4 Backup / recovery** — n/a: nothing stored.

## Baseline (T001)

`tests.e2e.test_navigation_freshness` + `tests.e2e.test_song_label_typography`: **4 tests, OK**, before
any edit. `tests.e2e.test_reading` was **not** baselined before the edits — a gap: it is the module
this slice changes most, and the only known-red row in it (`test_the_panel_shows_its_empty_view_when_no_songbook_exists`)
was carried over from the 137 session's reading of `develop` rather than re-proved here.

## Findings

| # | Class | Finding | Disposition |
| --- | --- | --- | --- |
| C1 | resolved | **The product's own CSS would have hidden the drawer twice.** The panel's base rules wipe with `clip-path` and hold `visibility: hidden` until `[data-nav="open"]`; a translated box under those rules is invisible for a different reason than the spec describes, and the first render kept a closed drawer at its pushed position (right edge 496 at 1024). Fixed by overriding both (clip-path none, visibility keyed on the same states) in the overlay block — measured after: closed at `-417 → -1`, open at `80 → 496`. | fixed in T004/T006 |
| C2 | spec gap | **The spec never says what a phone shows on arrival.** The server renders the desktop's open panel; at 425px that is a drawer over a page nobody opened. The implementation closes the stack on boot and whenever the width crosses into the phone range. Not a requirement — recorded here and in `fold.md` as the one sentence `R14` is missing. | recorded |
| C3 | resolved | **Escape reached only one level.** The filter field's own keydown handler swallowed Escape (`stopPropagation`) to clear itself; with an empty field it called `closePanel()`, so a two-level stack left its contents open — measured `('closed','closed','open')`. Both filter handlers now close the whole stack when the field is empty, and the document handler does the same. | fixed |
| C4 | resolved | **The phone's "child replaces parent" rule contradicted the stack.** `openChaptersInPlace()` set `nav = closed` whenever the child opened under 720px, a relic of the pushing model. In the drawer model the child covers the parent, so the parent must stay — otherwise the chevron returns to nothing and the state breaks its own prefix rule (`ch=open` implies `nav=open`). The branch is gone. | fixed |
| C5 | resolved | **A phone would have opened two drawers at once.** `restoreCurrentPath()` runs after the panel opens; on a phone it opened the contents level straight over the list the operator had just asked for, and for Tata Ibadah it opened a level that does not exist there. It now runs above the phone width only, and refuses Tata Ibadah outright. | fixed |
| C6 | resolved | **A rail switch closed the menu it was chosen from.** On a phone the section click navigated and the arriving page's own `ch` was adopted, so `ch` came back open while the menu had closed — the opposite of the one-stack rule. `applyPage()` now sets `rail=open`, `ch=closed` for a rail switch at the phone width, and closes all three when a stage page arrives. | fixed |
| C7 | test gap | **Two tests measured the wrong rectangle.** The theme button holds three glyphs; two are transparent and scaled `.65`, so `#themeBtn svg` measured 22 against the control's 24 and read as a size mismatch the product does not have. The test now measures the drawn glyph. The closed-drawer test also measured the drawer before closing it, because the server boots it open. | fixed (tests) |
| C8 | test gap | **Three tests asserted behaviour the product does not have.** A section switch keeps the stage and the URL by design (`kind: 'rail'` never pushes history); a service opened from the list brings its own contents; and a row cannot be clicked through the drawer that covers it. Each test now asserts the invariant that exists and reaches the row the way a person would. | fixed (tests) |
| C9 | accepted | **The scrim is a flat 34% wash**, not a blur: `backdrop-filter` at this size is a repaint per frame on the machines this runs on, and the owner's mockups never asked for one. | accepted |
| C10 | accepted | **The phone's drawers start below the toolbar** (`top: 58px`), so the toolbar stays usable while a drawer is open — the alternative, covering it, would hide the only control that closes the stack. | accepted |

| C11 | resolved | **The neighbouring suite encoded the model this slice replaces.** `tests/e2e/test_reading`
 reaches a sidebar at 720px and below with `.rail [data-panel=…]`, expects a pushed column, a boot
 state that is already open, a mini panel at 390px and a Project control on a phone — all four of
 which R14 changes. One module-level `click_section()` opens the drawer's control first; five tests
 were then re-read against R14: the idle-timer test opens the drawer it is about, the header test
 pins 40px only above 720, the Project-control test skips its geometry where the control is not
 drawn, the collapsed-panel test moved to the desktop width where a closed panel still has a state
 to keep, and the mode-switch test moved to the overlay width where its toggle exists. | fixed (T018) |
| C12 | resolved | **A helper inserted between a class's decorators and its class** silently stole
 `@override_settings(STATICFILES_STORAGE=StaticFilesStorage)`, so two E2E classes ran against
 `ManifestStaticFilesStorage` and read a page with no stylesheet at all — 59 reds that looked like
 a product regression. The helper now sits above the decorators. | fixed |

No CRITICAL finding. Every F-row in `analysis.md` was re-read against the code: F1–F7 hold as
written, and F3 (the touch exemption keyed on the pointer) is confirmed by the test that emulates a
touch pointer at 1024px, where the edit control measures opacity 1.
