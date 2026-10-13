# Spec 089: Name the preview's tabs container so it cannot be mistaken for a tab

- **ID:** 089
- **Status:** Accepted
- **Item:** ITEM-092
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Spec 085 (PR #339) gave the Preview dialog a header and, with it, a container for the verse tabs whose
class name — `preview__tabs-host` — contains `preview__tab`. Two unit tests that have guarded "a song
preview shows verse tabs only when there is more than one verse" assert on that substring:

```python
self.assertIn('preview__tab', html)        # two verses → tabs
self.assertNotIn('preview__tab', html)     # one verse  → no tabs
```

The second one now fails: the container is part of the dialog shell, so the string is present even when
no tab is rendered. The markup is right and the behaviour is right; the name is what collides. Rename
the container rather than weaken the assertion.

## Scope

### In scope

- The container element's class name in the preview header, in the template and the two stylesheet rules
  that style it.

### Out of scope

- The tabs themselves (`.preview__tabs`), the tab buttons (`.preview__tab`), their ARIA, and their
  behaviour: unchanged.
- `static/web/preview.js`, which reaches the container by its `data-preview-tabs-host` attribute, not by
  class.
- The pre-existing tests: they stay exactly as they are.

## UI details

- **Name:** `preview__tabs-host` becomes `preview__versetabs`.
- **Rendering:** identical. The element is empty until a song's tabs are lifted into it, and its
  `[hidden]` behaviour is unchanged.

## Acceptance scenarios

### Scenario: A single-verse song

- **Given** a Tata Ibadah with a song entry that has one verse
- **When** the service page is served
- **Then** the served markup contains no `preview__tab` string, and the pre-existing unit test passes
  unchanged.

### Scenario: A song with several verses

- **Given** a song entry with two or more verses
- **When** the preview is opened
- **Then** the tabs appear in the header and swap the verses, as they did before (spec 085).

## Traceability

- Domain/app tests: `multimedia/web/tests.py::ServiceEntryViewTests`
  (`test_a_song_preview_has_no_tabs_for_a_single_verse`,
  `test_a_song_preview_lists_its_short_reference_and_verse_tabs`) — unchanged, and red before this slice.
- E2E: `tests/e2e/test_entry_preview.py` — the header and tab cases from spec 085, unchanged.
- Implementation: `multimedia/web/templates/reading/_preview_modal.html`,
  `static/styles/design/components.css`.
