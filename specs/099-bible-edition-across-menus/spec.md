# Spec: Keep the selected Bible Version across menu switches

- **ID:** 099
- **Status:** Accepted
- **Item:** ITEM-099
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Keep the reader's deliberate TB or SIM choice during in-page navigation, even while the reading stage shows a non-Bible section. When the reader returns to a Bible chapter through the Bible sidebar, show the previously selected Version without requiring another toggle.

## Scope

### In scope

- TB/SIM selection on a Bible verse page.
- In-page navigation among the Bible, Kidung, and Tata Ibadah menus, followed by opening a Bible chapter from the Bible sidebar.
- Browser Back/Forward within the same live tab.
- Online and saved-copy Bible pages in the public reading shell.
- Resetting the in-memory choice on a full page load or in a separate tab.

### Out of scope

- Storing the choice in local/session storage, cookies, a URL updated by the in-page toggle, or server-side state.
- Changing the TB default or existing behavior for an explicitly supplied `?ed=` URL.
- Translation choices in editors, service entries, or projector pages.

## Domain rules

- The last deliberately chosen Bible Version is transient state for the currently loaded browser tab.
- Switching to Kidung or Tata Ibadah does not clear that state. Returning to a Bible chapter in the same tab applies it when that chapter contains verses for the selected Version.
- If the selected Version has no verses in an arriving chapter, retain the existing available-Version fallback for that chapter. Do not erase the tab's choice; apply it again on a later chapter that supports it.
- A full page load starts from the route's existing initial edition, which is TB by default. An explicit `?ed=sim` deep link continues to select SIM on initial load.
- A separate new tab does not inherit the live tab's in-memory choice. It starts from its own route's initial edition.
- Verse text, the TB/SIM control, chapter availability, and Bible sidebar labels reflect the active Version.

## Acceptance scenarios

### Scenario: Return to Bible after switching menus

- **Given** a Bible chapter with both Versions is open and the reader has selected SIM
- **When** the reader switches to Kidung or Tata Ibadah, then opens the Bible menu and selects a book and chapter
- **Then** the arriving Bible chapter shows SIM text and marks SIM selected
- **And** the Bible sidebar labels follow SIM while its mini tile keeps the existing TB abbreviation

### Scenario: Keep a deliberate TB choice across menu switches

- **Given** a Bible chapter with both Versions is open and the reader has deliberately selected TB
- **When** the reader switches to another menu and later opens a Bible chapter in the same tab
- **Then** the arriving chapter shows TB text and marks TB selected

### Scenario: Keep the choice through browser history navigation

- **Given** the reader selected SIM and has navigated in-page through another menu to a Bible chapter
- **When** the reader uses Back or Forward within the same tab to return to a Bible chapter
- **Then** each Bible chapter that supports SIM shows SIM

### Scenario: Preserve the preference when SIM is unavailable

- **Given** the reader selected SIM and opens a chapter that contains TB verses but no SIM verses
- **When** that chapter loads and the reader later opens a chapter that contains SIM verses
- **Then** the first chapter uses the existing available-Version fallback
- **And** the later chapter returns to SIM without requiring the reader to select it again

### Scenario: Reset on refresh and isolate a new tab

- **Given** the reader selected SIM in a page whose URL has no explicit `ed=sim` parameter
- **When** the reader refreshes the page or opens that route in a separate new tab
- **Then** the refreshed page or new tab starts with the normal TB default
- **And** the original live tab retains its SIM choice until that tab is refreshed

### Scenario: Apply the same behavior to saved-copy reading

- **Given** the public reading shell is showing Bible data from its saved library and the reader selected SIM
- **When** the reader switches to another menu and returns to a SIM-capable Bible chapter
- **Then** the chapter and sidebar show SIM without requiring a network request

## Traceability

- Domain/app tests: N/A; this is browser-side reading state.
- E2E: `ReadingE2ETests.test_bible_edition_survives_menu_switches_and_history` covers return from Kidung and Tata Ibadah with both TB and SIM, plus Back/Forward. `test_bible_edition_preference_returns_after_unavailable_chapter` covers fallback and later SIM restoration. `test_bible_edition_is_local_to_tab_and_resets_on_reload` covers tab isolation and refresh. `test_bible_sidebar_labels_follow_edition_and_reset_on_refresh` and `test_bible_language_links_keep_keyboard_and_no_js_navigation` cover sidebar labels, explicit `?ed=sim`, and no-JavaScript links. `OfflineLibraryE2ETests.test_offline_bible_edition_survives_menu_round_trip` covers saved-copy reading.
- Implementation: Current `static/web/reading.js` already holds `selectedEdition` in the live reading shell and reapplies it after stage swaps. The targeted E2E cases passed without a runtime change; no offline renderer change was needed.
