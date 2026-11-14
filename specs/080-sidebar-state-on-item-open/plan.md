# Plan 080: Keep the first-level sidebar state when a page opens from a second-level list

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-083
- **Bump:** patch

## Why

Opening a page from a second-level list rebuilds the whole shell from the arriving page, and every
reading page is rendered server-side with `nav="open"` (`_shell('alkitab'|'kidung'|'tatib', 'open', …)`
in `multimedia/web/reading/views.py`). `applyPage` copies that value over the live one for every
stage-swapping navigation:

```js
if (swapsStage) {
  root.dataset.nav = fresh.nav;      /* static/web/reading.js */
  root.dataset.ch = fresh.ch;
}
```

So the operator's deliberate collapse of the first panel is undone by the next chapter, song, or
service they open — and by the refresh that follows adding a service entry (the reported Tata Ibadah
case). The same line is why the songbook panel springs open when a song is opened, and why the Bible
book panel does.

## Scope / edges

**In:**

- `static/web/reading.js`: which navigations may change `root.dataset.nav` / `root.dataset.ch`.
- The four navigation kinds that swap only the reading stage: `chapter`, `song`, `service`, and the
  post-save `refresh`.
- All three sections (Alkitab chapters, Kidung songs, Tata Ibadah services) at every width.

**Out:**

- Main-menu (rail) switches, the search / results / more-results paths, and the `sync` / `lists` /
  `mode` kinds — they keep today's state behaviour.
- The 60-second idle collapse (spec 072), panel geometry, filters, and any server-rendered copy.

## Approach

Preserve the live sidebar state across a stage-only swap: keep `root.dataset.nav` and
`root.dataset.ch` as they are for `chapter` / `song` / `service` / `refresh`, and keep taking the
arriving page's stage-side facts (`read`, `home`, `section`) and its list contents. Build the
preserved set from the navigation kinds rather than from a section check, so the fix covers every
section at once and cannot regress one of them silently.

## TDD

- Domain/app tests: N/A — no server rule changes (the panels' contents and copy are unchanged).
- E2E (Playwright): `tests/e2e/test_reading.py`, a new class covering the three reported sections
  plus the add-entry refresh and the surviving main-menu switch.

## Risks

- The narrow layout hides the first panel when the second list is open (`closeChapters` /
  `openChaptersInPlace`); preserving `nav` must not resurrect a panel the layout deliberately hid.
  The preserved value is the operator's own state, so a panel closed by the layout cannot be reopened
  by this change — but the e2e must assert it at 390px as well as at desktop width.
- `refresh` also fires after a sidebar editor saves, where `nav` is normally `open`; preserving it is
  a no-op there, which the existing editor e2e covers.
