# Plan 102: Show the Tata Ibadah date header in the saved-copy reading path

- **Status:** Accepted (owner, 2026-10-17)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-102
- **Bump:** patch

## Why

The owner reports that a dated Tata Ibadah opened from the sidebar shows `TATA IBADAH` above
the title instead of its date, and that a full page refresh then shows the date.

The reading shell has two renderers of the same page. A click navigates in place: because the
saved offline library syncs on every page load and reports `ready`, `static/web/reading.js`
renders the destination locally (`GKPSOfflineRender.render`) and then — while online — refreshes
it from the server's chunk payload. A full reload never takes that path; it renders the Django
template.

`static/web/offline-render.js` sets the eyebrow once, in `common()`, as a hardcoded section
label (`'Tata Ibadah'` for tatib; `songPage()` overrides it with its citation). `servicePage()`
never writes the date, although the same file already parses `service.date` for the panel's month
groups (`dateParts`, `MONTHS_LONG`) and the server's chunk carries `date`. So both the local
render and the background refresh show the fallback label, and only the full reload matches
accepted spec 017.

The current suite misses it because the tests that click through to a dated service
(`tests/e2e/test_reading.py`) never make the offline library ready, and the offline E2E class
(`tests/e2e/test_offline_library.py`), which does wait for readiness, has only an undated service
fixture.

## Scope / edges

**In:**

- The saved-copy service page's eyebrow: long Indonesian date when the service is dated, the
  literal `Tata Ibadah` when it is not — identical to the server's rule.
- The same value for the saved copy, the online background refresh, history traversal, and a
  service opened from a search result (all re-render through the same function).
- One E2E regression case proving the header on the library-ready path, with the undated and
  `?mode=template` legs.

**Out:**

- The server view, template, and the chunk payload shape (the date is already sent).
- Song and Bible eyebrows, the SIM rail labels (`Agenda`), the Project button, panel labels,
  CSS, and the eyebrow's position or spacing.
- Any new date format, month table, or pre-formatted chunk field.
- The page title, contents pane, and editor paths of a service page.

## Approach

1. In `servicePage()`, directly after the `common(doc, 'tatib', …)` call, write the eyebrow from
   `service.date` through the file's existing `dateParts()` and `MONTHS_LONG`, falling back to
   `'Tata Ibadah'` when there is no date or it does not parse:

   ```js
   var serviceDate = dateParts(service.date);
   doc.querySelector('#readEyebrow').textContent = serviceDate
     ? serviceDate.day + ' ' + MONTHS_LONG[serviceDate.month - 1] + ' ' + serviceDate.year
     : 'Tata Ibadah';
   ```

   Key it on `service.date` alone — never on the dated/template `mode`, which the server also
   ignores for this string.
2. Keep the formatting inline. There is exactly one caller; `songPage()`'s eyebrow is a citation,
   not a date, and the panel's group head (`MONTHS_LONG[m] + ' ' + year`) is a different string.
   A named helper would abstract a single three-line write, so it waits until a second caller
   exists. The alternative — sending the formatted string in the service chunk — was rejected:
   it changes the payload contract, and every already-synced library would keep the old field
   until its next full re-sync, whereas the client-side format works with the stored chunks as
   they are.
3. Pin the result with the same literal the server tests already use (`23 Agustus 2026`), so the
   Python `format_date_long` and this JavaScript agree by test, not by hope.

## TDD

- Domain/app tests: none new. The server rule is already pinned by
  `multimedia/web/tests.py::test_tatib_service_header_uses_full_indonesian_month_name`
  (dated header) and `::test_undated_tatib_header_keeps_its_label`.
- E2E: `tests/e2e/test_offline_library.py::OfflineLibraryE2ETests::
  test_saved_dated_tatib_reading_keeps_its_date_header` — a dated service created in the test,
  the library made ready (`wait_for_offline_ready`), then (a) the saved-copy render's eyebrow
  text, (b) the sidebar click path, (c) the undated leg, and (d) the dated service under
  `?mode=template`.

## Risks

- Two implementations of one visible string (Python `format_date_long`, JavaScript in
  `offline-render.js`). The shared literal in both tests is the only thing holding them together;
  a future format change must touch both, and the spec says so.
- A saved chunk with a missing or malformed `date` degrades to the label rather than printing
  `undefined`/`null`; the next library sync heals it.
- The background chunk refresh applies a second render shortly after the first. After this fix
  both renders produce the same string, so nothing is seen to change; before the fix the E2E
  assertion must not depend on which of the two renders won (Playwright's auto-waiting `expect`
  polls, and both are wrong in the same way).
- Scope creep is the real risk here: this is a three-line label fix that looks like a good excuse
  to unify the shell's label strings. It is not part of this spec.
