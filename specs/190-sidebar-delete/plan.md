# Implementation Plan: Sidebar Delete Buttons

**Spec**: `specs/190-sidebar-delete/spec.md` (Accepted, Gate 1 2026-11-13)
**Branch**: `feat/190-sidebar-delete`
**Preview**: `specs/190-sidebar-delete/preview/index.html` (static; demonstrates FR-004 date-hidden-on-hover for dated Tata Ibadah row)

## Technical Context

| Field | Value |
| --- | --- |
| Language / stack | Python 3.12, Django 4.0, DRF; server-rendered templates + vanilla JS/jQuery |
| Existing patterns | Sidebar editors spec 005 (`editors.js`, `_editor_modal.html`, `_editor_form.html`), entry delete in `reading/views.py` (`entry_delete`, `old_item_delete`), row edit controls `.row-edit` in `components.css` |
| Storage | Soft-delete via `is_active=False`/existing model delete patterns as used by sidebar-managed records (confirm exact mechanism in implementation against `Book`, `Song`, `TataIbadah` models) |
| UI surfaces | `multimedia/web/templates/reading/_songbooks_panel.html`, `_song_list.html`, `_tatib_panel.html`; `static/styles/design/components.css`; `static/web/editors.js`, `static/web/reading.js` |
| Testing | Django `manage.py test` (targeted apps), Playwright E2E for user-visible acceptance where appropriate; targeted local verification per repo guidance |

## Constitution / Constraints Check

| Constraint | Status | Note |
| --- | --- | --- |
| Hymn/restricted rows render no controls | pass | Preserve existing `not book.hymn` / `not book_is_hymn` guards; templates unchanged for hymn rows |
| Confirm before destructive action | pass | Shared editor modal confirm flow before POST |
| POST + CSRF for deletes | pass | Dedicated delete endpoints, CSRF via existing token/cookie mechanism |
| Template noun must be `template` | pass | `data-editor-kind="template"` on template rows; `nounFor` returns `template` |
| Phone/touch drawer behavior preserved | pass | No gesture-model changes; controls remain accessible |
| Date hidden only on hover/focus reveal (FR-004) | pass | Scoped to Tata Ibadah dated service rows; accessible label/markup retained |

## Design Notes

- **Row actions**: Add `.row-delete` control adjacent to `.row-edit` within the same row context (or `.row-actions` wrapper if needed for layout parity), hidden at rest, revealed on hover/focus like edit. Use trash SVG consistent with product style.
- **FR-004 (date hide)**: Apply CSS so that when a Tata Ibadah row with a displayed date (`.book__s`) is hovered/focused-within for action reveal, `.book__s` is hidden (`visibility: hidden` or equivalent) without removing it from accessible name/markup. Scope to tatib panel rows to avoid affecting songbook short names elsewhere.
- **Endpoints**: `GET editor/<kind>/<pk>/delete/confirm/` (render confirm fragment with noun/name/hint) and `POST editor/<kind>/<pk>/delete/` for kinds `songbook`, `song`, `tatib`, `template` (validate kind/record eligibility). Return JSON `{ok: true}` on success.
- **Client flow**: `openDeleteConfirm(kind, id, noun)` fetches confirm HTML into shared modal; confirm button POSTs delete; on success `applyDelete` removes `<li>` from `#chList` (songs) or `#panelBody` (others). If deleted record was on stage, call navigation with history replace (not append) via `window.gkpsNavigate` / existing mechanism.
- **Kind/noun**: `nounFor(kind)` returns `template` for template, `Tata Ibadah` for service/tatib, else kind name as appropriate.
- **Template rows**: Ensure tatib panel template rows carry `data-editor-kind="template"` (and service rows `tatib`/service kind as needed) so client noun selection is correct.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/FR-001,002,003 (songbook delete control) | `_songbooks_panel.html`, `components.css` | `inspection` + `test` (targeted view/template/e2e as feasible) | non-hymn only |
| US2/FR-001,002,003 (song delete control) | `_song_list.html`, `components.css` | `inspection` + `test` | non-hymn book only |
| US3/FR-001,003,004 (tatib/template controls, date hide) | `_tatib_panel.html`, `components.css` | `inspection` + preview state | FR-004 hover/focus |
| FR-005,006,007,012 (confirm, noun, template kind) | `editors.js`, `_editor_delete_confirm.html`, modal/markup | `inspection` + `test` | `Delete template` for templates |
| FR-008,009 (GET confirm + POST delete, CSRF) | `views.py`, `urls.py` | `test` (Django view tests) | kinds validated |
| FR-010,011 (remove row, stage/history replace) | `editors.js`, `reading.js` exports | `inspection` + targeted behavior test | `#chList` vs `#panelBody` |
| FR-013 (responsive/touch) | `components.css` media rules | `inspection` | no drawer regression |
| SC-001–SC-005 | all above | mixed | see tasks/checklist |

**Verification split (planned)**: test for endpoints/critical behavior where practical; inspection/manual preview for hover/layout states and touch parity.

## Project Structure (changes)

```
multimedia/web/templates/reading/_songbooks_panel.html
multimedia/web/templates/reading/_song_list.html
multimedia/web/templates/reading/_tatib_panel.html
multimedia/web/templates/reading/_editor_delete_confirm.html (new)
multimedia/web/reading/views.py
multimedia/web/urls.py
static/styles/design/components.css
static/web/editors.js
static/web/reading.js
specs/190-sidebar-delete/{spec,plan,checklists,tasks,analysis,converge,...}
```