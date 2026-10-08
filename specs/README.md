# Specs

Living behavior contracts. Layout and gates: [`docs/PROCESS.md`](../docs/PROCESS.md).

## Rules

1. Spec **before** implementation. Plan (manual notes or any AI agent plan mode) **stops at Drafts**.
2. Use [`_template/`](./_template/) — `{plan,spec,tasks}.md` in every Draft.
3. Number specs `000`, `001`, … consecutively. Folder: `NNN-slug/`.
4. **Spec 000** is reserved for scaffolding and is **one spec**.
5. Keep acceptance in Given / When / Then.
6. Link tests under Traceability; tasks name those paths for TDD.
7. Update the spec in the same PR as behavior changes.
8. **One concern per spec.** CSS and copy still get a numbered spec.
9. Every spec comes from one or more `ITEM-XXX` on [`backlog/board.md`](../backlog/board.md).

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
| [030](030-add-entry-at-start/spec.md) | Add a service entry at the beginning | Draft |
| [031](031-clamp-pane-text/spec.md) | Clamp a text entry in the Tata Ibadah pane | Draft |
| [032](032-entry-preview-modal/spec.md) | Entry preview modal | Draft |
| [033](033-float-entry-controls/spec.md) | Float the entry controls over each item, top-right | Draft |
| [034](034-item-hover-highlight/spec.md) | Highlight a whole service entry item on hover | Draft |
| [035](035-section-break-separation/spec.md) | Give the section break a clear separation | Draft |
| [036](036-add-bar-outside-item-hover/spec.md) | Keep the add bar out of the item hover | Draft |
| [037](037-add-rows-before-after/spec.md) | Reveal the add rows before and after a hovered item | Draft |
| [038](038-drop-section-break-label/spec.md) | Remove the label from section-break entries | Draft |
| [039](039-hymn-song-sidebar-title/spec.md) | Show the short full title for a hymn song in the service sidebar | Draft |
| [040](040-picker-menus-past-modal/spec.md) | Let the entry modal picker menus extend past the modal | Draft |
| [041](041-picker-book-names/spec.md) | Show TB/SIM book names in the passage modal's book picker | Draft |
| [042](042-song-picker-sort-and-label/spec.md) | Sort and label the add-song picker like the hymn books | Draft |
| [043](043-book-picker-filter/spec.md) | Fix the passage modal book picker's search filter | Draft |
| [044](044-passage-translation-toggle/spec.md) | Add a TB/SIM toggle to the passage modal book picker | Draft |
| [045](045-custom-chapter-verse-dropdowns/spec.md) | Make the passage modal's chapter/verse dropdowns custom | Draft |
| [046](046-sidebar-text-two-lines/spec.md) | Show the first two text lines in the service sidebar | Draft |

`000` is reserved for the project scaffold baseline. As an adopter, this repo has no scaffold
spec yet — the as-built baseline backfill is a separate, owner-accepted slice.
