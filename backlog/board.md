# Backlog board

In-repo Kanban. Each card is an `ITEM-XXX`. Details live in [`items/`](./items/).

**Backlog column only:** sort by Priority (P0 first, then P1, P2, P3; ties by ID). Other columns stay in workflow order.

See [`README.md`](./README.md) for column meanings and owner phrases.

## Backlog

| ID | Title | Summary | Type | Priority | Effort | Spec | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [ITEM-002](./items/ITEM-002-projection-controls.md) | Projection source as display + controls | Drive the service from the projection window without switching to the dock | feat | P1 | L | — | 2026-09-30 |

## Speccing

| ID | Title | Summary | Type | Priority | Effort | Spec | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [ITEM-056](./items/ITEM-056-song-entry-label-and-verses.md) | Label song entries by their short hymn reference and show the selected verses | `HAL 3 — Sai puji Naibata` on the stage and in the preview modal; `Bait 1, 3` under an entry that keeps only some verses | chore | P2 | S | [054](../specs/054-song-entry-label-and-verses/spec.md) | 2026-10-10 |

## Ready

| ID | Title | Summary | Type | Priority | Effort | Spec | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- |

## In progress

| ID | Title | Summary | Type | Priority | Effort | Spec | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- |

## In review

| ID | Title | Summary | Type | Priority | Effort | Spec | PR | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [ITEM-015](./items/ITEM-015-songbook-language-removal.md) | Remove songbook language and merge duplicates | Remove language from the songbook model/API and merge same-name books without losing songs or references | feat | P1 | L | [013](../specs/013-songbook-language-removal/spec.md) | [#275](https://github.com/rsmbyk/multimedia-gkps-klender/pull/275) | 2026-10-08 |
| [ITEM-016](./items/ITEM-016-editor-focus-cleanup.md) | Clear stale row-edit visibility after modal close | Fix pointer-close focus/hover state across reading modals and sidebars | fix | P1 | M | [014](../specs/014-editor-focus-cleanup/spec.md) | [#275](https://github.com/rsmbyk/multimedia-gkps-klender/pull/275) | 2026-10-08 |
| [ITEM-017](./items/ITEM-017-tatib-form-fields.md) | Remove first-section and active controls from Tata Ibadah forms | Create empty active services and preserve activation on edit | fix | P1 | S | [015](../specs/015-tatib-form-fields/spec.md) | [#275](https://github.com/rsmbyk/multimedia-gkps-klender/pull/275) | 2026-10-08 |
| [ITEM-018](./items/ITEM-018-tatib-custom-datepicker.md) | Use a custom date picker for Tata Ibadah forms | Replace native date input with an accessible calendar | feat | P1 | M | [016](../specs/016-tatib-custom-datepicker/spec.md) | [#275](https://github.com/rsmbyk/multimedia-gkps-klender/pull/275) | 2026-10-08 |
| [ITEM-019](./items/ITEM-019-tatib-full-month-header.md) | Show a full month name in the Tata Ibadah date header | Use the full Indonesian month name above dated service titles | fix | P2 | S | [017](../specs/017-tatib-full-month-header/spec.md) | [#275](https://github.com/rsmbyk/multimedia-gkps-klender/pull/275) | 2026-10-08 |
| [ITEM-020](./items/ITEM-020-project-button-styles.md) | Style Project and Stop projecting as primary and danger actions | Style projection start/stop according to action state | chore | P2 | S | [018](../specs/018-project-button-styles/spec.md) | [#275](https://github.com/rsmbyk/multimedia-gkps-klender/pull/275) | 2026-10-08 |
| [ITEM-021](./items/ITEM-021-search-reset-state.md) | Clear remembered search when the home is reset | Reset stale query/scroll state while preserving results during sidebar browsing | fix | P1 | S | [019](../specs/019-search-reset-state/spec.md) | [#275](https://github.com/rsmbyk/multimedia-gkps-klender/pull/275) | 2026-10-08 |
| [ITEM-022](./items/ITEM-022-tatib-date-popover-default.md) | Use a date popover with a Sunday default | Show calendar beneath the field and preselect the nearest Sunday for a new service | feat | P1 | S | [020](../specs/020-tatib-date-popover-default/spec.md) | [#275](https://github.com/rsmbyk/multimedia-gkps-klender/pull/275) | 2026-10-08 |
| [ITEM-024](./items/ITEM-024-calendar-over-modal.md) | Let the Tata Ibadah date picker overlap the editor modal | Keep the open calendar visible over the scrollable modal content and within the viewport | fix | P1 | S | [022](../specs/022-datepicker-over-modal/spec.md) | [#275](https://github.com/rsmbyk/multimedia-gkps-klender/pull/275) | 2026-10-08 |
| [ITEM-025](./items/ITEM-025-emphasize-sundays.md) | Make Sundays more prominent in the Tata Ibadah date picker | Add a theme-aware Sunday cue while preserving selected and today states | chore | P2 | S | [023](../specs/023-emphasize-sundays/spec.md) | [#275](https://github.com/rsmbyk/multimedia-gkps-klender/pull/275) | 2026-10-08 |
| [ITEM-026](./items/ITEM-026-square-date-cells.md) | Make Tata Ibadah calendar date cells square | Equal-width/height date cells while preserving Sunday accents and popover behavior | chore | P2 | S | [024](../specs/024-square-date-cells/spec.md) | [#275](https://github.com/rsmbyk/multimedia-gkps-klender/pull/275) | 2026-10-08 |
| [ITEM-027](./items/ITEM-027-quiet-modal-focus.md) | Avoid automatic row outlines after modal close | Quiet automatic restoration across modals without removing deliberate keyboard focus | fix | P1 | M | [025](../specs/025-quiet-modal-focus/spec.md) | [#275](https://github.com/rsmbyk/multimedia-gkps-klender/pull/275) | 2026-10-08 |
| [ITEM-028](./items/ITEM-028-live-projection-editing.md) | Keep editing while projecting, and follow every change | Allow add/edit/delete/reorder during projection; reorder persists on drop; the display follows every change | feat | P1 | M | [026](../specs/026-live-projection-editing/spec.md) | [#275](https://github.com/rsmbyk/multimedia-gkps-klender/pull/275) | 2026-10-08 |

## Done

| ID | Title | Summary | Type | Priority | Effort | Spec | Merged | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [ITEM-055](./items/ITEM-055-entry-controls-height.md) | Give each entry the height of its floating controls | Reserve a top band for Preview/Edit/Delete so they never sit on the words | chore | P2 | S | [053](../specs/053-entry-controls-height/spec.md) | develop | 2026-10-10 |
| [ITEM-054](./items/ITEM-054-collapse-hidden-add-rows.md) | Collapse the hidden add rows and tighten the section break | Hidden add rows reserve no space at rest; break margins 34px → 16px | chore | P2 | S | [052](../specs/052-collapse-hidden-add-rows/spec.md) | develop | 2026-10-10 |
| [ITEM-053](./items/ITEM-053-song-picker-reference-search.md) | Search songs by songbook reference and title | Filter by hymn-book name substring; references match book substring + number prefix, optional sub-number/title | fix | P2 | S | [051](../specs/051-song-picker-reference-search/spec.md) | develop | 2026-10-10 |
| [ITEM-052](./items/ITEM-052-song-picker-short-name-search.md) | Search and label songs by songbook abbreviation | Match short name; keep hymn reference visible after selection | fix | P2 | S | [050](../specs/050-song-picker-short-name-search/spec.md) | develop | 2026-10-09 |
| [ITEM-051](./items/ITEM-051-passage-modal-layout.md) | Fix passage modal control placement and overflow | Center TB/SIM above the book picker; keep chapter/verse dropdowns inside the modal | fix | P2 | S | [049](../specs/049-passage-modal-layout/spec.md) | develop | 2026-10-09 |
| [ITEM-050](./items/ITEM-050-book-picker-filter.md) | Make passage book filtering hide non-matches | Hide non-matching book options; match TB/SIM names; restore all on clear | fix | P2 | S | [048](../specs/048-book-picker-filter/spec.md) | develop | 2026-10-09 |
| [ITEM-048](./items/ITEM-048-sidebar-text-two-lines.md) | Show the first two text lines for untitled service entries | Quote the first two literal body lines for untitled Text and Single-Screen Text entries; preserve titles and center the grip | chore | P2 | S | [046](../specs/046-sidebar-text-two-lines/spec.md) | develop | 2026-10-09 |
| [ITEM-047](./items/ITEM-047-custom-chapter-verse-dropdowns.md) | Make the passage modal's chapter/verse dropdowns custom | Replace the native chapter/verse selects with the custom picker for consistency | refactor | P2 | M | [045](../specs/045-custom-chapter-verse-dropdowns/spec.md) | develop | 2026-10-09 |
| [ITEM-046](./items/ITEM-046-passage-translation-toggle.md) | Add a TB/SIM toggle to the passage modal book picker | Flip the picker's translation in place; names swap, the choice is stored, no new field | feat | P2 | M | [044](../specs/044-passage-translation-toggle/spec.md) | develop | 2026-10-09 |
| [ITEM-044](./items/ITEM-044-song-picker-sort-and-label.md) | Sort and label the add-song picker like the hymn books | Hymns by number, others by title; hymn groups first by id; hymn options use short references | chore | P2 | S | [042](../specs/042-song-picker-sort-and-label/spec.md) | develop | 2026-10-09 |
| [ITEM-043](./items/ITEM-043-picker-book-names.md) | Show TB/SIM book names in the passage modal's book picker | One item per book: TB name main, SIM name dimmed on the right, like the sidebar | feat | P2 | M | [041](../specs/041-picker-book-names/spec.md) | develop | 2026-10-08 |
| [ITEM-042](./items/ITEM-042-picker-menus-past-modal.md) | Let the entry modal book/song menus extend past the modal | Cap the picker menus to the viewport, not the dialog, like the date picker | fix | P2 | M | [040](../specs/040-picker-menus-past-modal/spec.md) | develop | 2026-10-08 |
| [ITEM-041](./items/ITEM-041-hymn-song-sidebar-title.md) | Show the short full title for a hymn song in the service sidebar | Label a hymn song entry with its short reference and title, e.g. KJ 435 Marolopolop Tondingki | chore | P2 | S | [039](../specs/039-hymn-song-sidebar-title/spec.md) | develop | 2026-10-08 |
| [ITEM-040](./items/ITEM-040-drop-section-break-label.md) | Remove the label from section-break entries | Drop the title/label control and usage for the section_break kind | chore | P2 | S | [038](../specs/038-drop-section-break-label/spec.md) | develop | 2026-10-08 |
| [ITEM-039](./items/ITEM-039-add-rows-before-after.md) | Reveal the add rows before and after a hovered item | Hovering an item shows the add row above it and the one below it | chore | P2 | M | [037](../specs/037-add-rows-before-after/spec.md) | develop | 2026-10-08 |
| [ITEM-038](./items/ITEM-038-add-bar-not-item-hover.md) | Keep the add bar out of the item hover | Hovering the add buttons must not highlight the item above or reveal its controls | chore | P2 | S | [036](../specs/036-add-bar-outside-item-hover/spec.md) | develop | 2026-10-08 |
| [ITEM-037](./items/ITEM-037-section-break-separation.md) | Give the section break a clear separation in the Tata Ibadah pane | One clear divider, consistent between the legacy rule and the section_break entry | chore | P2 | S | [035](../specs/035-section-break-separation/spec.md) | develop | 2026-10-08 |
| [ITEM-036](./items/ITEM-036-highlight-item-on-hover.md) | Highlight a whole service entry item on hover | Give the hovered entry a theme-aware row highlight without shifting text | chore | P2 | S | [034](../specs/034-item-hover-highlight/spec.md) | develop | 2026-10-08 |
| [ITEM-035](./items/ITEM-035-float-entry-controls.md) | Float the entry controls over each item, top-right | Preview/Edit/Delete over the text with a brief backing, shown on hover | chore | P2 | S | [033](../specs/033-float-entry-controls/spec.md) | develop | 2026-10-08 |
| [ITEM-049](./items/ITEM-049-stabilise-flaky-e2e.md) | Stabilise the flaky E2E tests | Wait for the date-picker re-anchor and the search-offset restore to settle before asserting | test | P2 | S | [047](../specs/047-stabilise-flaky-e2e/spec.md) | develop | 2026-10-08 |
| [ITEM-034](./items/ITEM-034-entry-preview-modal.md) | Preview a service entry's full content in a modal | View-only, headerless modal with the full text/passage/lyrics; sticky close; Esc/overlay dismiss | feat | P2 | L | [032](../specs/032-entry-preview-modal/spec.md) | develop | 2026-10-08 |
| [ITEM-033](./items/ITEM-033-clamp-pane-text.md) | Show only the first lines of a text in the Tata Ibadah pane | Clamp a long text entry to a few lines so the running order stays readable | chore | P2 | S | [031](../specs/031-clamp-pane-text/spec.md) | develop | 2026-10-08 |
| [ITEM-032](./items/ITEM-032-add-entry-at-start.md) | Add a service entry at the beginning of a Tata Ibadah | Insert at order 1 instead of only after a row, across entries and legacy rows | feat | P2 | M | [030](../specs/030-add-entry-at-start/spec.md) | develop | 2026-10-08 |
| [ITEM-031](./items/ITEM-031-one-screen-fitted-text.md) | One-screen text entry that auto-fits its font | A text kind that shows its whole body on one screen, shrinking the font to fit, then ellipsizing | feat | P2 | M | [029](../specs/029-single-screen-text/spec.md) | develop | 2026-10-08 |
| [ITEM-030](./items/ITEM-030-remove-update-button.md) | Remove the Update the current state button | Drop the manual re-read control now that saved changes reach the display on their own | chore | P2 | S | [028](../specs/028-remove-update-button/spec.md) | develop | 2026-10-08 |
| [ITEM-029](./items/ITEM-029-remove-projection-note.md) | Remove the projection status note | Drop the status line under the Project / Stop projecting controls | fix | P2 | S | [027](../specs/027-remove-projection-note/spec.md) | develop | 2026-10-08 |
| [ITEM-014](./items/ITEM-014-hide-songbook-fields.md) | Hide short name and hymn-book fields in songbook forms | Remove the short-name and hymn-book controls from songbook create/edit forms while preserving stored values | chore | P2 | S | [012](../specs/012-hide-songbook-fields/spec.md) | develop | 2026-10-07 |
| [ITEM-012](./items/ITEM-012-hymn-song-order.md) | Sort hymn book songs by number and sub-number | Restore numeric number and sub-number order in public hymn-book lists | fix | P1 | S | [011](../specs/011-hymn-song-order/spec.md) | develop | 2026-10-06 |
| [ITEM-013](./items/ITEM-013-ci-e2e-harness.md) | Restore reliable CI and E2E execution | Restore the safe Playwright lifecycle and fail-closed CI test-scope detection | fix | P1 | M | [010](../specs/010-fast-pr-feedback-ci/spec.md) | develop | 2026-10-06 |
| [ITEM-011](./items/ITEM-011-fast-pr-feedback-ci.md) | Fast PR feedback and repository CI | Fast checks for draft PR updates; parallel full browser E2E on ready-for-review PRs | chore | P1 | M | [010](../specs/010-fast-pr-feedback-ci/spec.md) | develop | 2026-10-06 |
| [ITEM-010](./items/ITEM-010-sidebar-tint-legibility.md) | Higher-legibility selected sidebar tint | Light-theme selected fill updated to `#B9D7C9`; dark theme unchanged | chore | P2 | S | [009](../specs/009-sidebar-tint-legibility/spec.md) | develop | 2026-10-06 |
| [ITEM-009](./items/ITEM-009-sidebar-selection-tint.md) | Softer selected-item tint in reading sidebars | Softer selected highlight for Bible books and chapters, songbooks, songs, and Tata Ibadah services | chore | P2 | S | [008](../specs/008-sidebar-selection-tint/spec.md) | develop | 2026-10-06 |
| [ITEM-008](./items/ITEM-008-old-rows.md) | The old rows — editable, and one running order | Edit/Delete on old TataIbadahItem rows from the pane, and one running order so an insertion lands after the clicked row | feat | P1 | L | [007](../specs/007-service-order-editor/spec.md) | develop | 2026-10-06 |
| [ITEM-007](./items/ITEM-007-service-entries.md) | Service entries | One Tata Ibadah holds texts, scriptures, songs and section breaks; drag reorder with save/discard; its own projector, current OBS untouched | feat | P1 | L | [006](../specs/006-service-entries/spec.md) | develop | 2026-10-06 |
| [ITEM-006](./items/ITEM-006-sidebar-editors.md) | Sidebar editors for Kidung and Tata Ibadah | Add/edit modals for songbooks, songs and Tata Ibadah from the reading sidebars; hymn books stay read-only; no login by owner decision | feat | P1 | L | [005](../specs/005-sidebar-editors/spec.md) | develop | 2026-10-06 |
| [ITEM-005](./items/ITEM-005-public-site-revamp.md) | Public site revamp | Search-first home, icon rail with nested sidebars, full-corpus search (Bible, Kidung, Tata Ibadah), EN chrome + Indonesian terms, AA palette | chore | P1 | L | [004](../specs/004-public-site-revamp/spec.md) | develop | 2026-10-06 |
| [ITEM-004](./items/ITEM-004-maintenance-page.md) | Maintenance page at the site root | `/` shows a maintenance notice; home moves to a temporary URL behind a switch | feat | P1 | M | [003](../specs/003-maintenance-page/spec.md) | develop | 2026-10-01 |
| [ITEM-003](./items/ITEM-003-local-docker-compose.md) | Local Docker Compose stack on low-conflict ports | `web` + `db` via `docker compose`, published on random high ports | chore | P1 | S | [002](../specs/002-local-docker-compose/spec.md) | develop | 2026-10-01 |
| [ITEM-001](./items/ITEM-001-public-songs-reading.md) | Public song reading + design foundation | Design foundation + public song pages; editor to /manage | feat | P0 | M | [001](../specs/001-public-songs-reading/spec.md) | main | 2026-09-30 |
| [ITEM-000](./items/ITEM-000-adopt-vexbook.md) | Adopt vexbook process at v0.4.0 | Process file set + adoption ADR + board/specs stubs | chore | P0 | M | — | main | 2026-09-30 |
