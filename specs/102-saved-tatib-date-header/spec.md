# Spec 102: Show the Tata Ibadah date header in the saved-copy reading path

- **ID:** 102
- **Status:** Accepted (owner, 2026-10-17)
- **Item:** ITEM-102
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

A Tata Ibadah opened by a click keeps the same date eyebrow the server renders above its title;
today the saved-copy renderer replaces it with the section label `Tata Ibadah`.

## Scope

### In scope

- The saved-copy service page's date eyebrow: its long Indonesian date when the service is dated.
- The same value on the online background refresh, history traversal, and a service opened from a
  search result — every path that renders through the saved-copy renderer.

### Out of scope

- The server view and template, the chunk payload shape, and the offline library's own data.
- Song and Bible eyebrows, SIM rail labels, the Project button, panel labels, CSS, and the
  eyebrow's size, spacing, and position.
- New date formats, month tables, or a pre-formatted eyebrow field in the chunk.
- The service page's title, contents pane, and editor paths.

## Domain rules

- A dated service's eyebrow is its long Indonesian date, byte-identical to the server's
  `format_date_long`: `23 Agustus 2026`. The Python and JavaScript implementations stay pinned to
  the same literal by their tests.
- An undated service keeps the literal `Tata Ibadah`, in every edition — the SIM rail popup reads
  `Agenda`, but the server's eyebrow fallback stays `Tata Ibadah`, and the saved copy must match.
- The eyebrow follows the service, not the panel's dated/template choice: a dated service opened
  with `?mode=template` still leads with its date, exactly as the server renders it.
- When the service has no usable date value, the eyebrow falls back to `Tata Ibadah` rather than
  showing an empty or malformed string.

## UI details

The look does not change, so no new preview is presented: this restores the header accepted in
spec 017 above a service title.

- **Size / spacing:** unchanged — `.read__eyebrow` per `static/styles/design/components.css`
  (16.5px / 1.65, weight 600, letter-spacing .12em, uppercase, ink at .78 opacity; `margin-bottom:
  0` inside a Tata Ibadah head).
- **Position / layout:** unchanged — the eyebrow stays first in `.read__head-top`, sharing that
  row with the Project button on a dated service. Nothing here moves because the text changed.
- **States / responsive behavior:** unchanged.

## Acceptance scenarios

### Scenario: A dated service opened in place keeps its date

- **Given** the offline library is ready and a service dated 23 August 2026
- **When** I open it from the Tata Ibadah panel, and again when the background refresh lands
- **Then** the eyebrow above the title reads `23 Agustus 2026` in both states

### Scenario: The same page from a full refresh

- **Given** the same dated service
- **When** I open its reading page with a normal page load
- **Then** the eyebrow reads `23 Agustus 2026`, unchanged from today

### Scenario: An undated service keeps its label

- **Given** the offline library is ready and an undated service
- **When** I open it from the Tata Ibadah panel
- **Then** the eyebrow reads `Tata Ibadah`

### Scenario: A dated service in the templates filter

- **Given** the offline library is ready and a service dated 23 August 2026
- **When** I open it with the panel showing templates (`?mode=template`)
- **Then** the eyebrow still reads `23 Agustus 2026`

## Traceability

- Domain/app tests: none new; the server rule stays pinned by
  `multimedia/web/tests.py::test_tatib_service_header_uses_full_indonesian_month_name` and
  `::test_undated_tatib_header_keeps_its_label`.
- E2E: `tests/e2e/test_offline_library.py::OfflineLibraryE2ETests::
  test_saved_dated_tatib_reading_keeps_its_date_header` — the dated-service case covers the
  saved-copy render, the sidebar click path, the undated leg, and the `?mode=template` leg. The
  server path stays covered by
  `tests/e2e/test_reading.py::test_tatib_date_and_project_button_are_vertically_centered`.
- Implementation: `static/web/offline-render.js` (`servicePage()`).
