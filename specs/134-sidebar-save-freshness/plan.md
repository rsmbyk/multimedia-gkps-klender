# Implementation Plan: Keep reading views current after sidebar edits

**Spec**: `specs/134-sidebar-save-freshness/spec.md`
**Branch**: `feat/134-sidebar-save-freshness`
**Bump**: `patch`
**Preview**: `specs/134-sidebar-save-freshness/preview/` — live Django reading shell with disposable data
**Board**: ITEM-143 is Ready; anchor issue [#397](https://github.com/rsmbyk/multimedia-gkps-klender/issues/397)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 server; vanilla JavaScript in the reading shell |
| Primary dependencies | Existing Django 4.0.1 routes and templates; existing `static/web/reading.js` DOM reconciliation and `static/web/editors.js` save event; no new dependency |
| Storage | Existing server database is authoritative (`DATABASE_URL`; SQLite in development/preview); no schema change. IndexedDB remains a later presentation snapshot, not the editor-write store. |
| Testing | Django test runner with Playwright Python `StaticLiveServerTestCase` E2E under `tests/e2e/` |
| Target platform | Desktop and mobile browsers using the shared public reading shell |
| Project type | Server-rendered Django pages with in-place vanilla-JS navigation and updates |
| Performance goals | After a successful editor save, request the current server state and update visible representations in place; no additional user navigation or full document reload |
| Constraints | Preserve route, query, selection, sidebar modes, filters, scroll, and focus; retain existing server validation and service-entry save behavior; exclude separate management/media/projector/OBS flows |
| Scale / scope | One reading-shell slice; one shared client refresh path and focused E2E coverage; no database, public API, package, or visual-style changes |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| Repository constitution | n/a | `CONSTITUTION.md` is absent. SDD-01 makes it optional and says never to create it automatically; there are no repo principles to evaluate for this Plan. |

Re-checked after Phase 1: n/a — `CONSTITUTION.md` remains absent; no new principle or design violation was introduced.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — existing saved records plus transient reading-shell state and visible representations; no persistent model changes.
- `contracts/README.md` — explicit `none`; existing same-origin routes and `editor:saved` event are reused internally.
- `quickstart.md` — disposable live-preview command, review URLs, and the planned E2E verification command with its current runnability limit.

## Implementation Approach

The successful save event remains the refresh trigger. The reader will choose a fresh server URL from the visible shell context, then reconcile every relevant region from that response:

1. For an active Tata Ibadah, song, or songbook representation, update the shared first-column row, relevant second-column contents where applicable, stage heading/content, and document title.
2. For a sidebar edit while an unrelated stage is open, update the sidebar regions while retaining the unrelated stage and current route.
3. For open search results, refresh using the existing query, update result membership and group counts, and refresh the active tab-local search snapshot so restoration cannot put stale result HTML back.
4. Keep filters, selected records, pane modes, scroll positions, and focus stable through the in-place reconciliation; apply existing filters to the saved values.
5. Keep editor error handling and in-place Tata Ibadah entry saves on their existing paths.

These are design boundaries; implementation begins only after Gate 2.

## Traceability

| Requirement / scenario | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001, FR-004, US1/AC1–AC3, Edge — active records and preserved shell state | `static/web/reading.js` | `test` → `tests/e2e/test_sidebar_save_freshness.py::test_tatib_sidebar_save_refreshes_row_and_active_stage`, `::test_song_sidebar_save_refreshes_row_stage_and_title`, `::test_songbook_sidebar_save_refreshes_row_heading_and_title`, `::test_sidebar_save_preserves_filter_pane_scroll_and_focus` | Covers all three record kinds and verifies filtering, pane modes, scroll, and focus during row reconciliation. |
| FR-002, US1/AC4 — Kidung edit with Bible stage | `static/web/reading.js` | `manual` — keep a Bible chapter open, edit a Kidung songbook, and check the row, stage, and route in the live preview | The unrelated stage and route remain in place. |
| FR-003, US2/AC1–AC2 — matching and non-matching search result | `static/web/reading.js` | `test` → `tests/e2e/test_sidebar_save_freshness.py::test_search_result_edit_keeps_matching_song_and_updates_counts`, `::test_search_result_edit_removes_nonmatching_song_and_updates_counts` | Two cases assert result membership, text, group counts, and retained query. |
| FR-005, Edge — rejected save | `static/web/editors.js`, `static/web/reading.js` | `inspection` — verify the success event dispatch remains after a valid response and the error path does not dispatch it or alter reading values | Keeps the current editor error behavior and saved reading values. |
| FR-006, Edge — service-entry edit in an open Tata Ibadah | `static/web/reading.js` | `manual` — edit a service entry in the open Tata Ibadah preview and confirm the stage and contents list update in place | Protects the existing in-place entry-refresh path. |
| SC-001 | Live preview at `/tatib/1/` and `/songs/1/` | `manual` — edit each record type and compare the sidebar row, active stage heading, and tab title immediately after save, without reload or reopening a pane | Use the disposable preview data. |
| SC-002 | Live preview at `/search?q=Preview` | `manual` — run the still-matching and no-longer-matching song edits; inspect result text, result/group counts, and the unchanged query | Search snapshot restoration must not restore old content. |
| SC-003 | Live preview at `/bible/1/1/` | `manual` — keep a Bible chapter open, edit a Kidung row, then inspect stage, route, pane mode, filter, scroll, and focus | Confirms unrelated stage and browsing state. |

**Verification split**: 2 test · 1 inspection · 5 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| None | No constitution or architecture constraint is violated. | The fix stays within the existing reading shell, server routes, and DOM reconciler. |

## Project Structure

### Documentation

```text
specs/134-sidebar-save-freshness/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/README.md  checklists/  preview/
```

No `tasks.md` is created during Plan; SDD-14 reserves that artifact for Tasks after this Plan's exit checks.

### Source

```text
static/web/reading.js                         existing shared reading-shell refresh path
tests/e2e/test_sidebar_save_freshness.py      planned Playwright save-freshness scenarios
backlog/items/ITEM-143-sidebar-save-freshness.md  Ready demand card anchored to issue #397
```

### Structure Decision

Keep the behavior in the existing shared reader because `/`, `/home/`, `/search`, `/bible/`, `/songs/`, and `/tatib/` use the same reading shell and `editor:saved` handler. Put user-visible acceptance in a focused Django/Playwright E2E module under the existing `tests/e2e/` convention. The separate management, admin, Media Library, projector, and OBS paths need no files in this slice.
