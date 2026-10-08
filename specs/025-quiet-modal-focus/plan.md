# Plan 025: Avoid automatic row outlines after modal close

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-027
- **Bump:** patch

## Why

Closing a song/songbook editor with Enter or Escape now leaves the row link outlined. The owner also requests checking the other modal families and sidebars for the same issue.

## Findings

- Live Escape cancellation reproduced a restored row link with browser `outline: auto 1px` for songbooks, songs, and Tata Ibadah.
- Live Enter cancellation reproduced the same outline on a songbook link.
- Existing focus tests pass because they check hidden edit buttons and focus targets, not the unwanted row outline.
- `static/web/editors.js` restores focus to a row's primary link; moving focus there alone does not prevent a browser focus ring after keyboard use.
- `static/web/reading.js` post-save refresh looks up an unqualified `data-editor-id` and focuses that node; sidebar IDs live on edit buttons. This path needs an isolated actual-save regression, not a production-data write.
- Service-entry/legacy editors share the dialog but have separate open/delete code; the unsaved-order confirmation is a separate native dialog and must be audited too.

## Scope / edges

**In:** Visually quiet automatic focus restoration after editor close/save, correct focus targets after replaced DOM, and an audit/fix of the same symptom across reading-shell modal families. Keep real keyboard focus visible and Tab/Shift+Tab usable.

**Out:** Disabling focus outlines globally, blurring to the document body/hidden dummy, changing selection tints, removing genuine hover controls, changes to forms/permissions or legacy admin UI.

## Approach

Keep a valid, predictable DOM focus target but distinguish automatic restoration from intentional keyboard navigation. Apply any suppression only to the restoration target, ending on blur or deliberate keyboard navigation. Coordinate close and refresh paths so no later focus operation reintroduces the ring or strands focus on an edit action. Match saved records by kind as well as ID where needed and reveal/flash the primary row rather than its edit button.

Audit sidebar create/edit, service-entry create/edit/delete, legacy-item edit/delete, and unsaved-order confirmation. Use one shared policy for affected paths, not per-songbook CSS exceptions. Preserve native keyboard focus and existing sidebar behavior outside restoration.

## TDD

- Domain/app tests: N/A unless save response metadata needs coverage.
- E2E: `tests/e2e/test_editor.py`, `tests/e2e/test_entries.py`, `tests/e2e/test_old_rows.py`, and focused modal cases in `tests/e2e/test_reorder.py`.
- Start from home and navigate in-page. Cover Escape, Enter on Cancel, Enter submission on valid single-line forms, and pointer save/cancel. Use isolated test records for writes.
- Assert focus target, computed outlines after settled close/refresh, hidden idle controls, and visible focus after Tab/Shift+Tab.
- Full browser suite deferred to push.

## Risks

A global outline rule would damage accessibility. Close events and asynchronous refresh can replace the target; suppression must not become permanent or match a different record with the same numeric ID. Preserve unsaved-order guards and keyboard continuation when entry controls are replaced/deleted.
