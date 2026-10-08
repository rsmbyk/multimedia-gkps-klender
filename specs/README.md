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

`000` is reserved for the project scaffold baseline. As an adopter, this repo has no scaffold
spec yet — the as-built baseline backfill is a separate, owner-accepted slice.
