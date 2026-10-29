# Specs

Dated slice records. The process is declared in [`docs/PROCESS.md`](../docs/PROCESS.md);
the templates are in [`_templates/`](./_templates/).

## Index

| Spec | Title | Status |
| --- | --- | --- |
| [001](001-public-songs-reading/spec.md) | Public song reading + design foundation | Accepted |
| [002](002-local-docker-compose/spec.md) | Local Docker Compose stack | Accepted |
| [003](003-maintenance-page/spec.md) | Maintenance page at the site root | Accepted |
| [004](004-public-site-revamp/spec.md) | Public site revamp | Accepted |
| [005](005-sidebar-editors/spec.md) | Sidebar editors for Kidung and Tata Ibadah | Accepted |
| [006](006-service-entries/spec.md) | Service entries — one Tata Ibadah holds texts, scriptures and songs | Accepted |
| [007](007-service-order-editor/spec.md) | The old rows — editable, and one running order | Accepted |
| [008](008-sidebar-selection-tint/spec.md) | Softer selected-item tint in the reading sidebars | Accepted |
| [009](009-sidebar-tint-legibility/spec.md) | Higher-legibility selected sidebar tint | Accepted |
| [010](010-fast-pr-feedback-ci/spec.md) | Fast PR feedback and repository CI | Accepted |
| [011](011-hymn-song-order/spec.md) | Sort hymn book songs by number and sub-number | Accepted |
| [012](012-hide-songbook-fields/spec.md) | Hide short name and hymn-book fields in songbook forms | Accepted |
| [013](013-songbook-language-removal/spec.md) | Remove songbook language and merge duplicate songbooks | Accepted |
| [014](014-editor-focus-cleanup/spec.md) | Clear stale row-edit visibility after modal close | Accepted |
| [015](015-tatib-form-fields/spec.md) | Remove first-section and active controls from Tata Ibadah forms | Accepted |
| [016](016-tatib-custom-datepicker/spec.md) | Use a custom date picker for Tata Ibadah forms | Accepted |
| [017](017-tatib-full-month-header/spec.md) | Show a full month name in the Tata Ibadah date header | Accepted |
| [018](018-project-button-styles/spec.md) | Style Project and Stop projecting as primary and danger actions | Accepted |
| [019](019-search-reset-state/spec.md) | Clear remembered search when the home is reset | Accepted |
| [020](020-tatib-date-popover-default/spec.md) | Use a date popover with a Sunday default | Accepted |
| [021](021-hide-projection-lock-note/spec.md) | Hide the projection-lock explanation | Superseded by 026 |
| [022](022-datepicker-over-modal/spec.md) | Let the Tata Ibadah date picker overlap the editor modal | Accepted |
| [023](023-emphasize-sundays/spec.md) | Make Sundays more prominent in the Tata Ibadah date picker | Accepted |
| [024](024-square-date-cells/spec.md) | Make Tata Ibadah calendar date cells square | Accepted |
| [025](025-quiet-modal-focus/spec.md) | Avoid automatic row outlines after modal close | Accepted |
| [026](026-live-projection-editing/spec.md) | Keep editing while projecting, and keep the display in step | Accepted |
| [027](027-remove-projection-note/spec.md) | Remove the projection status note | Accepted |
| [028](028-remove-update-button/spec.md) | Remove the "Update the current state" button | Accepted |
| [029](029-single-screen-text/spec.md) | Single-screen text entry | Accepted |
| [030](030-add-entry-at-start/spec.md) | Add a service entry at the beginning | Accepted |
| [031](031-clamp-pane-text/spec.md) | Clamp a text entry in the Tata Ibadah pane | Accepted |
| [032](032-entry-preview-modal/spec.md) | Entry preview modal | Accepted |
| [033](033-float-entry-controls/spec.md) | Float the entry controls over each item, top-right | Accepted |
| [034](034-item-hover-highlight/spec.md) | Highlight a whole service entry item on hover | Accepted |
| [035](035-section-break-separation/spec.md) | Give the section break a clear separation | Accepted |
| [036](036-add-bar-outside-item-hover/spec.md) | Keep the add bar out of the item hover | Accepted |
| [037](037-add-rows-before-after/spec.md) | Reveal the add rows before and after a hovered item | Accepted |
| [038](038-drop-section-break-label/spec.md) | Remove the label from section-break entries | Accepted |
| [039](039-hymn-song-sidebar-title/spec.md) | Show the short full title for a hymn song in the service sidebar | Accepted |
| [040](040-picker-menus-past-modal/spec.md) | Let the entry modal picker menus extend past the modal | Accepted |
| [041](041-picker-book-names/spec.md) | Show TB/SIM book names in the passage modal's book picker | Accepted |
| [042](042-song-picker-sort-and-label/spec.md) | Sort and label the add-song picker like the hymn books | Accepted |
| [043](043-book-picker-filter/spec.md) | Fix the passage modal book picker's search filter | Superseded by 041 |
| [044](044-passage-translation-toggle/spec.md) | Add a TB/SIM toggle to the passage modal book picker | Accepted |
| [045](045-custom-chapter-verse-dropdowns/spec.md) | Make the passage modal's chapter/verse dropdowns custom | Accepted |
| [046](046-sidebar-text-two-lines/spec.md) | Show the first two text lines for untitled service entries | Accepted |
| [047](047-stabilise-flaky-e2e/spec.md) | Stabilise the flaky E2E tests | Accepted |
| [048](048-book-picker-filter/spec.md) | Make the passage book search hide non-matching books | Accepted |
| [049](049-passage-modal-layout/spec.md) | Center the TB/SIM switch and contain passage number pickers | Accepted |
| [050](050-song-picker-short-name-search/spec.md) | Search and label songs by songbook short name | Accepted |
| [051](051-song-picker-reference-search/spec.md) | Search songs by songbook reference and title | Accepted |
| [057](057-service-entry-quick-actions/spec.md) | Service entry quick fixes: single-screen Save, instant break, no break Edit, sidebar verses | Accepted |
| [059](059-speaker-colors/spec.md) | Color liturgy speakers as a congregation cue | Accepted |

| [060](060-song-label-typography/spec.md) | Give the song reference, title, and selected verses distinct styles | Accepted |
| [061](061-entry-modal-highlight/spec.md) | Clear stale service entry highlight after modal dismissal | Accepted |
| [063](063-toc-number-centering/spec.md) | Center entry numbers vertically in the Tata Ibadah contents list | Accepted |
| [065](065-entry-modal-origin-highlight/spec.md) | Hold the service entry highlight while its modal is open | Accepted |
| [066](066-stage-song-verse-line/spec.md) | Always show a song entry's verses on the Tata Ibadah stage | Accepted |
| [100](100-sim-translation-abbreviations/spec.md) | Use the requested SIM book abbreviations | Accepted; Go To amendment implemented |
| [101](101-goto-translation-flash/spec.md) | Brighten the translation label after flipping a Go To passage | Accepted |
| [122](122-saved-reading-parity/spec.md) | Saved reading page parity | Accepted |
| [123](123-tatib-date-header-parity/spec.md) | Match the Tata Ibadah date header to the songbook header | Accepted |
| [124](124-bible-edition-block-identity/spec.md) | Keep a chapter's verse text when the reading page updates in place | Accepted |
| [125](125-saved-song-sort-parity/spec.md) | A saved hymn song page never shows the song sort control | Accepted |
| [126](126-songbook-short-header/spec.md) | A song page cites its songbook by its short name | Accepted |
| [127](127-site-name-tab/spec.md) | The tab names the site, and the index's tab stops at the name | Accepted |
| [128](128-songbook-hymn-separator/spec.md) | Hymn songbooks above one separator, the rest A–Z | Accepted |
| [129](129-sidebar-empty-states/spec.md) | The sidebars say which nothing they show | Accepted |
| [130](130-empty-service-tiles/spec.md) | An empty Tata Ibadah quarter-centres its five add tiles | Accepted |
| [131](131-retire-break-entry/spec.md) | The Break kind retires, and the breaks already written stay | Accepted |
| [141](141-projector-window-reopen/spec.md) | A closed projector window can be reopened at the screen that is on air | Accepted |
| [142](142-entry-surface/spec.md) | A service entry draws no box until it is pointed at | Accepted |
| [143](143-add-bar/spec.md) | The add bar opens over the seam, and nothing moves | Accepted |
| [144](144-passage-song-icons/spec.md) | A passage and a song carry their own kind mark | Accepted |
| [145](145-media-size-precision/spec.md) | A media size reads in the unit that still shows its number | Accepted |
| [146](146-media-and-transfer-age-buckets/spec.md) | The Media Library and the transfer history group by age | Accepted |
| [147](147-transfer-icon-column/spec.md) | A long transfer name ellipsizes instead of moving the row | Accepted |
| [148](148-media-library-refresh-flicker/spec.md) | The Media Library list holds still while it refreshes | Accepted |
| [149](149-transfer-separator-seam/spec.md) | The Transfers list draws each boundary once | Accepted |
| [150](150-references-token-order/spec.md) | The first refresh authenticates its references write | Accepted |
| [153](153-preview-tabs-row/spec.md) | The preview's verse tabs get their own row | Accepted |
